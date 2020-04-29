from whoosh.qparser import QueryParser
from whoosh.qparser import MultifieldParser


class Searcher:
    def __init__(self, wikimedia):
        self.wikimedia = wikimedia

    def search(self, text):
        results = []
        query = MultifieldParser(['title', 'text'], schema=self.wikimedia.index.schema).parse(text)
        # QueryParser(text, schema=self.wikimedia.index.schema).parse()

        try:
            searcher = self.wikimedia.index.searcher()
            results = searcher.search(query)

        except:
            pass
            
        # finally:
        #     searcher.close()

        return results
