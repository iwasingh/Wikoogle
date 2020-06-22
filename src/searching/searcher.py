import time
import logging
import searching.result as r
from whoosh import scoring, searching, sorting
from whoosh.searching import Searcher as ws
from whoosh.qparser import QueryParser, MultifieldParser
from query.expander import thesaurus_expand, lca_expand
from hits.hits import Hits
from pagerank.facet import page_rank_facet
from hits.facet import hits_rank_facet

logger = logging.getLogger()

MODELS = {
    'bm25': scoring.BM25F,
    'pl2': scoring.PL2
}

EXPANSION = {
    'none': False,
    'lca': lca_expand,
    'thesaurus': thesaurus_expand
}


class Searcher:
    def __init__(self, wikimedia, pagerank):
        self.wikimedia = wikimedia
        self.pagerank = pagerank
        self.hitsrank = Hits()
        
        self.hitsrank.load_graphml()

        self.parser = MultifieldParser(['title', 'text'], fieldboosts={'title': 2.5, 'text': 1.0}, schema=self.wikimedia.index.schema)
        self.parser_base = QueryParser('text', schema=self.wikimedia.index.schema)

        self.searcher = {
            'bm25': ws(reader=self.wikimedia.reader, weighting=scoring.BM25F),
            'pl2': ws(reader=self.wikimedia.reader, weighting=scoring.PL2)
        }
        
        self._query_expansion_relevant_limit = 10
        self._query_expansion_terms = 5
        self._page_rank_relevant_window = 30
        self._hits_rank_relevant_window = 10

    @staticmethod
    def parse_query_from_terms(terms):
        return " OR ".join(['(' + i + ')' for i in terms])

    def search(self, text, configuration):
        # Default query object
        query = self.parser.parse(text)

        # Default results object
        results = []

        # Default query limit
        limit = 10

        if 'results_limit' in configuration and int(configuration['results_limit']) > 0:
            limit = int(configuration['results_limit'])

        # Default Query Expansion
        expansion = 'lca'
        expansion_threshold = 1.4
        expansion_terms = self._query_expansion_terms

        if 'query_expansion' in configuration:
            expansion = configuration['query_expansion']

        # Default Ranking
        model = MODELS['bm25']
        searcher = self.searcher['bm25']

        if 'ranking' in configuration and configuration['ranking'] and MODELS[configuration['ranking']]:
            model = MODELS[configuration['ranking']]
            searcher = self.searcher[configuration['ranking']]
        
        # Default Link Analysis
        link_analysis = False
        facet = lambda result: result.score

        if 'link_analysis' in configuration and configuration['link_analysis'] != 'none':
            link_analysis = configuration['link_analysis']

            if link_analysis == 'hits_rank':
                results = searcher.search(query, limit=self._hits_rank_relevant_window)
                auths, hubs = self.hitsrank.rank_from_results(results)
                facet = hits_rank_facet(auths, hubs)
            
            if link_analysis == 'page_rank':
                facet = page_rank_facet(self.pagerank)

        try:
            results = []
            print('* limit ', limit)
            print('* model: ', model.__name__)
            print('* expansion model: ', expansion)
            print('* link analysis: ', link_analysis)

            if expansion != 'none' and expansion is not False:
                if expansion == 'lca':
                    if link_analysis:
                        results = searcher.search(query, limit=self._page_rank_relevant_window)
                        results = sorted(results, key=facet, reverse=True)[:self._query_expansion_relevant_limit]
                        expansion_threshold = 1.005
                    else:
                        results = searcher.search(query, limit=self._query_expansion_relevant_limit)

                    if len(results) >= self._query_expansion_relevant_limit:
                        terms = lca_expand(query, results, size=expansion_terms, threshold=expansion_threshold)
                        weights = [1 - (0.9 * (i + 1) / len(terms)) for i, t in enumerate(terms)]
                        expanded_query = query
                        for i, w in enumerate(weights):
                            q = self.parser_base.parse(terms[i]).with_boost(w)
                            expanded_query = expanded_query | q
                        results = searcher.search(expanded_query, limit=limit)
                elif expansion == 'thesaurus':
                    terms = Searcher.parse_query_from_terms(thesaurus_expand(text, self.wikimedia, size=10))
                    expanded_query = query | self.parser.parse(terms).with_boost(0.30)
                    results = searcher.search(expanded_query, limit=limit)
            else:
                results = searcher.search(query, limit=limit)

            results = sorted(results, key=facet, reverse=True)
            return [r.Result(i, query) for i in results]

        except Exception as e:
            logger.error(e)
            return []
