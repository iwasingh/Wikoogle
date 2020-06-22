from whoosh import sorting
from pagerank.pagerank import normalize_title


def page_rank_facet(pagerank):
    def page_rank_sort(result):
        doc_title = normalize_title(result.get("title", ""))
        score = result.score
        rank = pagerank.graph.get(doc_title, 0)
        rlength = len(pagerank.graph)
        return rank * score

    return page_rank_sort

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

class PageRankFacet(sorting.FacetType):
    def __init__(self, pagerank, maptype=None):
        self.pagerank = pagerank
        self.maptype = maptype

    def categorizer(self, global_searcher):
        return PageRankCategorizer(self.pagerank, global_searcher)
    