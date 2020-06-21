from whoosh.qparser import QueryParser
import searching.result as r
from pagerank.pagerank import normalize_title
from whoosh.qparser import MultifieldParser
from query.expander import thesaurus_expand, lca_expand
import logging
from whoosh import scoring, searching, sorting
import time

logger = logging.getLogger()


def page_rank_facet(pagerank):
    def page_rank_sort(result):
        doc_title = normalize_title(result.get("title", ""))
        score = result.score
        rank = pagerank.graph.get(doc_title, 0)
        rlength = len(pagerank.graph)
        return rank * score

    return page_rank_sort


class PageRankFacet(sorting.FacetType):
    def __init__(self, pagerank, maptype=None):
        self.pagerank = pagerank
        self.maptype = maptype

    def categorizer(self, global_searcher):
        return self.PageRankCategorizer(self.pagerank, global_searcher)

    class PageRankCategorizer(sorting.Categorizer):
        def __init__(self, pagerank, global_searcher):
            self.pagerank = pagerank
            w = global_searcher.weighting
            self.use_final = w.use_final
            if w.use_final:
                self.final = w.final

        def set_searcher(self, segment_searcher, offset):
            self.segment_searcher = segment_searcher

        def key_for(self, matcher, docid):
            doc = self.segment_searcher.stored_fields(docid)
            doc_title = normalize_title(doc.get("title", ""))
            score = matcher.score()
            rank = self.pagerank.graph.get(doc_title, 0)
            return rank * len(self.pagerank.graph)


def page_rank_weighting(idf, tf, fl, avgfl, B, K1, a, r):
    s = scoring.bm25(idf, tf, fl, avgfl, B, K1)
    return a * s + (1 - a) * r * 1000


class PageRankBM25Scorer(scoring.WeightLengthScorer):
    def __init__(self, searcher, fieldname, text, pagerank, a, B=0.75, K1=1.2):
        parent = searcher.get_parent()

        # fai come lambda dello scorer per non dover passare rearcher e pagerank

        self.searcher = parent
        self.pagerank = pagerank

        self.r = 0
        self.doc_title = ""
        self.idf = parent.idf(fieldname, text)
        self.avgfl = parent.avg_field_length(fieldname) or 1
        self.B = B
        self.K1 = K1
        self.a = a

        self.setup(searcher, fieldname, text)

    def score(self, matcher):
        document = self.searcher.stored_fields(matcher.id())
        self.doc_title = normalize_title(document.get("title", ""))
        self.r = self.pagerank.get(self.doc_title, 0)
        return self._score(matcher.weight(), self.dfl(matcher.id()))

    def _score(self, weight, length):
        return page_rank_weighting(self.idf, weight, length, self.avgfl, self.B, self.K1, self.a, self.r)


class PageRankBM25(scoring.WeightingModel):
    __name__ = 'PageRankBM25'

    def __init__(self, pagerank, alpha):
        self.pagerank = pagerank
        self.alpha = alpha

    def scorer(self, searcher, fieldname, text, qf=1):
        return PageRankBM25Scorer(searcher, fieldname, text, self.pagerank, self.alpha)

class HitsBM25(scoring.WeightingModel):
    __name__ = 'HitsBM25'

    def __init__(self, pagerank, alpha):
        self.pagerank = pagerank
        self.alpha = alpha

    def scorer(self, searcher, fieldname, text, qf=1):
        return PageRankBM25Scorer(searcher, fieldname, text, self.pagerank, self.alpha)


MODELS = {
    'bm25': scoring.BM25F,
    'pl2': scoring.PL2,
    'pr_bm25': PageRankBM25,
    'hits': HitsBM25,
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

        self._page_rank_bm25_alpha = 0.8
        _pr_bm25_mod = PageRankBM25(self.pagerank.graph, self._page_rank_bm25_alpha)

        self.searcher = {
            'bm25': self.wikimedia.index.searcher(weighting=scoring.BM25F),
            'pl2': self.wikimedia.index.searcher(weighting=scoring.PL2),
            'pr_bm25': self.wikimedia.index.searcher(weighting=_pr_bm25_mod),
            'hits': self.wikimedia.index.searcher(weighting=_pr_bm25_mod)
        }
        
        self._query_expansion_relevant_limit = 10
        self._query_expansion_terms = 5
        self._page_rank_relevant_window = 30
        self.parser_base = QueryParser('text', schema=self.wikimedia.index.schema)
        self.parser = MultifieldParser(['title', 'text'], fieldboosts={'title': 2.5, 'text': 1.0},
                                       schema=self.wikimedia.index.schema)

    @staticmethod
    def parse_query_from_terms(terms):
        # self.parser.parse(terms).with_boost(0.30)
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

        # Defeault PageRank graph
        # graph = self.pagerank.graph

        # if model.__name__ == 'HitsBM25':
        #     if expansion == 'lca':
                

        # Default PageRank relevance
        alpha = self._page_rank_bm25_alpha

        if 'page_rank_lvl' in configuration and int(configuration['page_rank_lvl']) > 0:
            alpha = int(configuration['page_rank_lvl']) / 10
            _pr_bm25_mod = PageRankBM25(self.pagerank.graph, alpha)
            searcher = self.wikimedia.index.searcher(weighting=_pr_bm25_mod)

        # Default Link Analysis
        link_analysis = False
        facet = lambda result: result.score

        if model.__name__ != 'PageRankBM25':
            if 'link_analysis' in configuration and configuration['link_analysis'] != 'none':
                facet = page_rank_facet(self.pagerank)
                link_analysis = 'page_rank'

        try:
            results = []
            print('* limit ', limit)
            print('* alpha ', alpha)
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
