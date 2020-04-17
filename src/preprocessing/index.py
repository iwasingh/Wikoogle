import sys
import logging
import sys
from lxml import etree
from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED, SchemaClass
from whoosh import index
from parsing.combinators import ParseError
from .analyzer import WikimediaAnalyzer
import config
import json
from parsing.compiler import Compiler
import shutil
from whoosh.analysis import StandardAnalyzer

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
logger.addHandler(
    logging.FileHandler(filename=str((config.ROOT / 'logs' / 'preprocessing.index.log').absolute()), delay=True))


# huge_tree: disable security restrictions and support very deep trees
# and very long text content (only affects libxml2 2.7+)

# @functools.lru_cache(user_function)

class WikiSchema(SchemaClass):
    title = ID(stored=True)
    text = TEXT(stored=True, analyzer=WikimediaAnalyzer())


# TODO singleton
class WikiIndex:
    def __init__(self):
        self.schema = WikiSchema
        self.xml_parser = WikiXML(namespace='http://www.mediawiki.org/xml/export-0.10/')
        # self.index_path = None
        self.index = None
        # self.name = '__indexir'

    def clear(self):
        pass

    def get(self, name='__indexdir', destructive=True):
        index_path = config.ROOT.joinpath(name)
        path = str(index_path)
        # self.index_path = index_path

        if destructive and index_path.exists():
            shutil.rmtree(path)

        if destructive or (not index_path.exists() or not index.exists_in(path)):
            try:
                index_path.mkdir()
                self.index = index.create_in(path, WikiSchema())
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
                logger.info('Processing: ', wiki.name)
                for root in self.xml_parser.from_xml(str(wiki)):
                    try:
                        # title = self.xml_parser.title(root)
                        id, title, text = self.xml_parser.get(root)
                        article = compiler.compile(text.text)
                        writer.add_document(title=title.text, text=article)
                    except ParseError as e:
                        miss += 1
                        logger.warning(f'Article {title.text} parse error, skipping, count: {miss}')
                        continue

        writer.commit()


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
