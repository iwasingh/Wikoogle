from pagerank.pagerank import normalize_title


def page_rank_facet(pagerank):
    def page_rank_sort(result):
        doc_title = normalize_title(result.get("title", ""))
        score = result.score
        rank = pagerank.graph.get(doc_title, 0)
        return rank * score

    return page_rank_sort
