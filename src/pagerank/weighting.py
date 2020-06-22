from whoosh import scoring
from pagerank.pagerank import normalize_title


class PageRankBM25(scoring.WeightingModel):
    __name__ = 'PageRankBM25'

    use_final = True

    def __init__(self, pagerank, alpha):
        self.pagerank = pagerank
        self.alpha = alpha

    def scorer(self, searcher, fieldname, text, qf=1):
        return scoring.BM25FScorer(searcher, fieldname, text, B=0.75, K1=1.2, qf=qf)

    def final(self, searcher, doc_id, score):
        doc = searcher.stored_fields(doc_id)
        doc_title = normalize_title(doc.get("title", ""))
        rank = self.pagerank.get(doc_title, 0)
        return self.alpha * score + (1 - self.alpha) * rank * score
