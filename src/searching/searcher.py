from whoosh.qparser import QueryParser
import searching.result as r
from pagerank.pagerank import normalize_title
from whoosh.qparser import MultifieldParser
from query.expander import thesaurus_expand, lca_expand
import logging
from whoosh import scoring, searching
from whoosh.classify import Expander, ExpansionModel
from whoosh import qparser
import whoosh.query as wq
import time

logger = logging.getLogger()

ALPHA = 0.65

def page_rank_weighting(idf, tf, fl, avgfl, B, K1, r):
    s = scoring.bm25(idf, tf, fl, avgfl, B, K1)
    return ALPHA * s + (1 - ALPHA) * r

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
        s = page_rank_weighting(self.idf, weight, length, self.avgfl, self.B, self.K1, self.ranking)
        k = ["dna", "dna_virus", "genome", "mutation", "chromatin", "nucleic_acid", "base_pair", "genetic_code", "nucleotide", "brazil"]
        if self.doc_title in k: print(self.doc_title, s)
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
        self.parser = QueryParser('text', schema=self.wikimedia.index.schema)

    def search(self, text):
        results = []
        # TODO expand query
        query = MultifieldParser(['title', 'text'], fieldboosts={'title': 2.0, 'text': 2.0},
                                 schema=self.wikimedia.index.schema).parse(text)
        # QueryParser("text", schema=self.wikimedia.index.schema).parse(text)

        try:
            searcher = self.wikimedia.index.searcher(weighting=CustomWeighting(self.pagerank))
            t0 = time.time()
            results = searcher.search(query, limit=self._query_expansion_limit)
            t1 = time.time()
            print('whoosh search time: ', t1 - t0)

            if len(results) >= self._query_expansion_limit:
                t0 = time.time()
                terms = " OR ".join(['(' + i + ')' for i in lca_expand(query, results, size=self._query_expansion_terms)])
                t1 = time.time()
                print(terms, 'query expansion time:', t1 - t0)
                expanded_query = query | self.parser.parse(terms).with_boost(0.30)
                # TODO To each concept assign a weight given by 1-0.9  i/m to not stress user query term
                results = searcher.search(expanded_query, limit=30)

            return [r.Result(i, query) for i in results]

        except Exception as e:
            breakpoint()
            logger.error(e)
