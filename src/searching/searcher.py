from whoosh.qparser import QueryParser
import searching.result as r
from pagerank.pagerank import normalize_title
from whoosh.qparser import MultifieldParser
from query.expander import thesaurus_expand, lca_expand
import logging
from whoosh import scoring, searching, sorting
import time

logger = logging.getLogger()

MODELS = {
    'bm25': scoring.BM25F,
    'pl2': scoring.PL2
}

EXPANSION = {
    'none': False
}

# LINK_ANALYSIS = {
#     'page_rank':
# }

ALPHA = 0.5


def page_rank_facet(pagerank):
    def page_rank_sort(result):
        doc_title = normalize_title(result.get("title", ""))
        score = result.score
        rank = pagerank.graph.get(doc_title, 0)
        rlength = len(pagerank.graph)
        return rank * score

    return page_rank_sort


# def expand_from(results, type='lca'):
#     if type == 'lca':
#         if len(results) >= self._query_expansion_limit:
#             t0 = time.time()
#             terms = " OR ".join(
#                 ['(' + i + ')' for i in lca_expand(query, results, size=self._query_expansion_terms)])
#             t1 = time.time()
#             print(terms, 'query expansion time:', t1 - t0)
#             expanded_query = query | self.parser.parse(terms).with_boost(0.30)
#             # TODO To each concept assign a weight given by 1-0.9  i/m to not stress user query term
#             results = searcher.search(expanded_query, limit=10)


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
            # return ALPHA * score + (1 - ALPHA) * (rank)


def page_rank_weighting(idf, tf, fl, avgfl, B, K1, r, rlength):
    s = scoring.bm25(idf, tf, fl, avgfl, B, K1)
    b = 1.5
    return s
    # return ALPHA * s + (1 - ALPHA) * (r * rlength)
    #     e_measure = (1 - ((1 + b**2)/(((b**2)/r) + (1/s))))
    #     print(r, s, e_measure)
    # print(s, r, r*rlength)


class CustomFunctionScorer(scoring.WeightLengthScorer):
    def __init__(self, searcher, fieldname, text, pagerank, B=0.75, K1=1.2):
        parent = searcher.get_parent()

        # fai come lambda dello scorer per non dover passare rearcher e pagerank

        self.searcher = parent
        self.pagerank = pagerank

        self.ranking = 0
        self.doc_title = ""
        self.idf = parent.idf(fieldname, text)
        self.avgfl = parent.avg_field_length(fieldname) or 1
        self.B = B
        self.K1 = K1

        self.setup(searcher, fieldname, text)

    def score(self, matcher):
        document = self.searcher.stored_fields(matcher.id())
        self.doc_title = normalize_title(document.get("title", ""))
        self.ranking = self.pagerank.graph.get(self.doc_title, 0)
        return self._score(matcher.weight(), self.dfl(matcher.id()))

    def _score(self, weight, length):
        s = page_rank_weighting(self.idf, weight, length, self.avgfl, self.B, self.K1, self.ranking,
                                len(self.pagerank.graph))

        # k = ["dna", "dna_virus", "genome", "mutation", "chromatin", "nucleic_acid", "base_pair", "genetic_code",
        #      "nucleotide", "brazil"]
        # if self.doc_title in k: print(self.doc_title, s)
        return s


class CustomWeighting(scoring.WeightingModel):
    def __init__(self, pagerank):
        self.pagerank = pagerank

    def scorer(self, searcher, fieldname, text, qf=1):
        return CustomFunctionScorer(searcher, fieldname, text, self.pagerank)


class Searcher:
    def __init__(self, wikimedia, pagerank):
        self.wikimedia = wikimedia
        self.pagerank = pagerank
        self._query_expansion_limit = 10
        self._query_expansion_terms = 5
        self._page_rank_limit = 30
        self.parser_base = QueryParser('text', schema=self.wikimedia.index.schema)
        self.parser = MultifieldParser(['title', 'text'], fieldboosts={'title': 2.5, 'text': 1.0},
                                       schema=self.wikimedia.index.schema)

    def search(self, text, configuration):
        results = []

        query = self.parser.parse(text)

        # query_base = self.parser_base.parse(text)

        # return []

        expansion = 'lca'
        expansion_threshold = 1.4
        expansion_terms = self._query_expansion_terms

        link_analysis = False

        limit = self._query_expansion_limit

        facet = lambda result: result.score

        if 'query_expansion' in configuration:
            expansion = configuration['query_expansion']

        model = MODELS['bm25']

        if 'ranking' in configuration and configuration['ranking'] and MODELS[configuration['ranking']]:
            model = MODELS[configuration['ranking']]

        if 'link_analysis' in configuration and configuration['link_analysis'] != 'none':
            facet = page_rank_facet(self.pagerank)
            limit = self._page_rank_limit
            link_analysis = 'page_rank'

        try:
            # TODO only 1 instance per model
            searcher = self.wikimedia.index.searcher(weighting=model)

            t0 = time.time()

            results = searcher.search(query, limit=limit)

            t1 = time.time()

            print('* whoosh search time: ', t1 - t0)
            print('* limit ', limit)
            print('* model: ', model.__name__)
            print('* expansion model: ', expansion)
            print('* result retrieved: ', len(results))
            print('* link analysis: ', link_analysis)

            if expansion == 'lca':
                if link_analysis:
                    results = sorted(results, key=facet, reverse=True)[:self._query_expansion_limit]
                    # results = results[:self._query_expansion_limit]
                    # expansion_threshold = 1.1
                if len(results) >= self._query_expansion_limit:
                    t0 = time.time()
                    terms = " OR ".join(
                        ['(' + i + ')' for i in
                         lca_expand(query, results, size=expansion_terms, threshold=expansion_threshold)])
                    t1 = time.time()
                    print(terms, 'query expansion time:', t1 - t0)
                    expanded_query = query | self.parser.parse(terms).with_boost(0.30)
                    # TODO To each concept assign a weight given by 1-0.9  i/m to not stress user query term
                    results = searcher.search(expanded_query, limit=limit)

            results = sorted(results, key=facet, reverse=True)[:10]
            return [r.Result(i, query) for i in results]

        except Exception as e:
            logger.error(e)
            return []
