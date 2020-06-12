from searching.fragmenter import Fragmenter, truncate
import logging
import time

logger = logging.getLogger()


class Result:
    def __init__(self, result, query, max_size=300, top=2):
        self._value = result
        self._query = query
        self.fragmenter = Fragmenter(max_size=max_size, top=top)

    @property
    def value(self):
        return self._value

    @property
    def resource(self):
        return f'https://en.wikipedia.org/wiki/{self.title.replace(" ", "_")}'

    @property
    def title(self) -> str:
        return self._value["title"]

    @property
    def text(self):
        return self._value["text"]

    def snippet(self):
        title = self._value["title"]
        text = self._value["text"]
        # t0 = time.time()
        snippet = self.fragmenter.frag(text, [i.text for i in self._query.all_tokens()])
        return Fragmenter.highlight(snippet)
        # if self.resource == 'https://en.wikipedia.org/wiki/Index_of_philosophy_articles_(A–C)':
        #     breakpoint()
        # t1 = time.time()
        # print('snippet generation time:', t1-t0)
