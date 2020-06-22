from whoosh import scoring
from pagerank.pagerank import normalize_title


class HitsBM25(scoring.WeightingModel):
    __name__ = 'HitsBM25'

    use_final = True

    def __init__(self, auth, hubs, alpha):
        self.auth = auth
        self.hubs = hubs
        self.alpha = alpha
    
    def scorer(self, searcher, fieldname, text, qf=1):
        return scoring.BM25FScorer(searcher, fieldname, text, B=0.75, K1=1.2, qf=qf)
    
    def final(self, searcher, doc_id, score):
        doc = searcher.stored_fields(doc_id)
        doc_title = normalize_title(doc.get("title", ""))
        r_auth = self.auth.get(doc_title, 0)
        r_hubs = self.hubs.get(doc_title, 0)
        rank = (r_auth / 2) + (r_hubs / 2)
        return self.alpha * score + (1 - self.alpha) * rank * score
