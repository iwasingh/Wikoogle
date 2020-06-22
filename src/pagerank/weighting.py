from whoosh import scoring
from pagerank.pagerank import normalize_title


def page_rank_weighting(idf, tf, fl, avgfl, B, K1, a, r):
    s = scoring.bm25(idf, tf, fl, avgfl, B, K1)
    return a * s + (1 - a) * r * s


class PageRankBM25Scorer(scoring.WeightLengthScorer):
    def __init__(self, searcher, fieldname, text, pagerank, a, B=0.75, K1=1.2):
        parent = searcher.get_parent()

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
