from searching.fragmenter import Fragmenter
import logging
import time

logger = logging.getLogger()


class Result:
    def __init__(self, result, query):
        self._value = result
        self._query = query
        # self._query_text =
        self.fragmenter = Fragmenter()

    @property
    def value(self):
        return self._value

    @property
    def title(self):
        return self._value["title"]

    @property
    def text(self):
        return self._value["text"]

    def snippet(self):
        title = self._value["title"]
        text = self._value["text"]
        # t0 = time.time()
        snippet = self.fragmenter.frag(text, [i.text for i in self._query.all_tokens()])
        # t1 = time.time()
        # print('snippet generation time:', t1-t0)
        return snippet
