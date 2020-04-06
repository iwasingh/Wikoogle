import sys
import logging
from lxml import etree


# huge_tree: disable security restrictions and support very deep trees
# and very long text content (only affects libxml2 2.7+)

# @functools.lru_cache(user_function)¶
class Parser:
    """XML dump wikipedia parser"""

    def __init__(self, path, namespace='http://www.mediawiki.org/xml/export-0.10/'):
        self._path = path
        self._namespace = namespace

    def _iterate(self):
        page = f'{{{self._namespace}}}' + 'page'
        context = etree.iterparse(self. _path, events=('end',), tag=page, huge_tree=True)
        # TODO improve with iterchildren/iterdescendants instead of xpath
        for _, root in context:
            namespaces = {'n': self._namespace}
            title = root.xpath('n:title', namespaces=namespaces)[0]
            body = root.xpath('n:revision/n:text', namespaces=namespaces)[0]

            print(body.text)
            while root.getprevious() is not None:
                del root.getparent()[0]
            root.clear()

    def parse(self):
        try:
            self._iterate()
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
