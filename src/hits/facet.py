from pagerank.pagerank import normalize_title


def hits_rank_facet(auths, hubs):
    def hits_rank_sort(result):
        doc_title = normalize_title(result.get("title", ""))
        score = result.score
        rank = max([auths.get(doc_title, 0), hubs.get(doc_title, 0)])
        return rank * score

    return hits_rank_sort
