from whoosh.qparser import QueryParser
import searching.result as r
from whoosh.qparser import MultifieldParser
from query.expander import thesaurus_expand, lca_expand
import logging
from whoosh import scoring
from whoosh.classify import Expander, ExpansionModel
from whoosh import qparser
import whoosh.query as wq
import time

logger = logging.getLogger()


class Searcher:
    def __init__(self, wikimedia):
        self.wikimedia = wikimedia
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
            searcher = self.wikimedia.index.searcher()
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
            logger.error(e)
