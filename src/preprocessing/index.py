import sys
import logging
import sys
from lxml import etree
from whoosh.fields import TEXT, ID, SchemaClass
from whoosh import index
from parsing.combinators import ParseError
from .analyzer import WikimediaAnalyzer
import config
from parsing.compiler import Compiler
import shutil

logger = logging.getLogger()


class WikiSchema(SchemaClass):
    id = ID(stored=True)
    title = TEXT(stored=True, analyzer=WikimediaAnalyzer(), field_boost=2.0)
    text = TEXT(stored=True, analyzer=WikimediaAnalyzer())


# TODO singleton
class WikiIndex:
    def __init__(self):
        self.schema = WikiSchema
        self.xml_parser = WikiXML(namespace='http://www.mediawiki.org/xml/export-0.10/')
        self.index = None

    def clear(self):
        pass

    def get(self, name='__indexdir', destructive=False):
        index_path = config.ROOT.joinpath(name)
        path = str(index_path)

        if destructive and index_path.exists():
            shutil.rmtree(path)
            while index_path.exists():
                pass

        if destructive or (not index_path.exists() or not index.exists_in(path)):
            try:
                index_path.mkdir()
                self.index = index.create_in(path, WikiSchema())
                logging.info('Index newly created, adding documents')
                self.build()
            except (FileExistsError, FileNotFoundError) as e:
                logger.error('Index already exist or parent not found')
                sys.exit(0)
        self.index = index.open_dir(path)

        return self

    def build(self, directory=config.DUMP_FOLDER):
        if not self.index:
            raise FileNotFoundError('Index not initialized')

        writer = self.index.writer()
        compiler = Compiler()
        miss = 0
        for wiki in directory.iterdir():
            if wiki.is_file() and wiki.stem.startswith('enwiki'):
                for root in self.xml_parser.from_xml(str(wiki)):
                    try:
                        # title = self.xml_parser.title(root)
                        id, title, text = self.xml_parser.get(root)
                        article = compiler.compile(text.text)
                        writer.add_document(title=title.text, text=article, id=f'{id}')
                        logger.info(f'{title.text} indexed')
                    except ParseError as e:
                        miss += 1
                        logger.warning(f'{title.text} parse error, skipping')
                        continue

        if miss > 0:
            logger.warning(f'{miss} articles ignored')

        writer.commit()

# huge_tree: disable security restrictions and support very deep trees
# and very long text content (only affects libxml2 2.7+)

# @functools.lru_cache(user_function)


class WikiXML:
    """XML dump wikipedia parser"""

    def __init__(self, namespace):
        self._prefix = 'W'
        self.TITLE = '{0}:title'.format(self._prefix)
        self.TEXT = '{0}:revision/{0}:text'.format(self._prefix)
        self.ID = '{0}:id'.format(self._prefix)

        self.namespaces = {self._prefix: namespace}
        self._base_tag = f'{{{namespace}}}' + 'page'

    def from_xml(self, path):
        context = etree.iterparse(path, events=('end',), tag=self._base_tag, huge_tree=True)
        # TODO improve with iterchildren/iterdescendants instead of xpath
        for _, root in context:
            yield root
            while root.getprevious() is not None:
                del root.getparent()[0]
            root.clear()

    def title(self, root):
        return root.xpath(self.TITLE, namespaces=self.namespaces)[0]

    def text(self, root):
        return root.xpath(self.TEXT, namespaces=self.namespaces)[0]

    def id(self, root):
        return root.xpath(self.ID, namespaces=self.namespaces)[0]

    def get(self, root):
        # TODO use a high order func
        return self.id(root), self.title(root), self.text(root)
