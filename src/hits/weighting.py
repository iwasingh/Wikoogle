from whoosh import scoring
from pagerank.pagerank import normalize_title

def hits_weighting(idf, tf, fl, avgfl, B, K1, a, r_a, r_h):
    r = (r_a * 10) + (r_h * 10) 
    
    r = r if r < 1.0 else 1.0
    r = r if r > 0 else 0.001
    
    s = scoring.bm25(idf, tf, fl, avgfl, B, K1)
    return a * s + (1 - a) * r * s

class HitsBM25Scorer(scoring.WeightLengthScorer):
    def __init__(self, searcher, fieldname, text, auth, hubs, a, B=0.75, K1=1.2):
        parent = searcher.get_parent()

        self.searcher = parent

        self.auth = auth
        self.hubs = hubs

        self.r_a = 0
        self.r_h = 0
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
        self.r_a = auth.get(self.doc_title, 0)
        self.r_h = hubs.get(self.doc_title, 0)
        return self._score(matcher.weight(), self.dfl(matcher.id()))

    def _score(self, weight, length):
        return hits_weighting(self.idf, weight, length, self.avgfl, self.B, self.K1, self.a, self.r_a, self.r_h)

class HitsBM25(scoring.WeightingModel):
    __name__ = 'HitsBM25'

    def __init__(self, auth, hubs, alpha):
        self.auth = auth
        self.hubs = hubs
        self.alpha = alpha

    def scorer(self, searcher, fieldname, text, qf=1):
        return HitsBM25Scorer(searcher, fieldname, text, self.auth, self.hubs, self.alpha)
