from whoosh.qparser import QueryParser
import searching.result as r
from whoosh.qparser import MultifieldParser
from query.expander import expand


class Searcher:
    def __init__(self, wikimedia):
        self.wikimedia = wikimedia

    def search(self, text):
        results = []
        # TODO expand query
        query = MultifieldParser(['title', 'text'], schema=self.wikimedia.index.schema).parse(text)
        # QueryParser("text", schema=self.wikimedia.index.schema).parse(text)

        try:
            searcher = self.wikimedia.index.searcher()
            results = searcher.search(query)
        except:
            pass

        return [r.Result(i, text) for i in results]
