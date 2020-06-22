import sys
import logging
import sys
from lxml import etree
from whoosh.fields import TEXT, ID, SchemaClass, KEYWORD
from whoosh import index
from parsing.combinators import ParseError
from pagerank.pagerank import PageRank, Adjacency, normalize_title
from .analyzer import WikimediaAnalyzer
import config
from parsing.compiler import Compiler, ParseTypes
import shutil
from parsing.utils import MalformedTag
from parsing.lexer import RedirectFound
from config import ASSETS_DATA, N_PROC
import networkx as nx

logger = logging.getLogger('preprocessing')

WAnalyzer = WikimediaAnalyzer(cachesize=-1)


class WikiSchema(SchemaClass):
    id = ID(stored=True)
    title = TEXT(stored=True, analyzer=WAnalyzer, field_boost=2.0)
    text = TEXT(stored=True, analyzer=WAnalyzer)
    categories = KEYWORD(stored=True, analyzer=WAnalyzer, scorable=True, lowercase=True, commas=True)


# TODO singleton
class WikiIndex:
    def __init__(self, namespace='http://www.mediawiki.org/xml/export-0.10/'):
        self.schema = WikiSchema
        self.xml_parser = WikiXML(namespace=namespace)
        self.index = None
        self.reader = None

    def clear(self):
        pass

    def get(self, name='__indexdir', dump=config.DUMP_FOLDER, destructive=False):
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
                self.build(directory=dump)
            except (FileExistsError, FileNotFoundError) as e:
                logger.error('Index already exist or parent not found')
                sys.exit(0)
        self.index = index.open_dir(path)
        print(' * Bootstrap index reader')
        self.reader = self.index.reader()

        return self

    def build(self, directory=config.DUMP_FOLDER):
        if not self.index:
            raise FileNotFoundError('Index not initialized')

        writer = self.index.writer(limitmb=2048, procs=N_PROC, multisegment=True)

        compiler = Compiler()

        categories = []
        reverse_graph = []

        file_adjlist = open(ASSETS_DATA / 'graphs' / 'graph.adjlist.tmp', "w")

        def parse_link(node, article):
            category = node.value.category()

            if category:
                categories.append(category.group())
            else:
                article_link = normalize_title(node.value.text)
                if article_link not in reverse_graph:
                    reverse_graph.append(article_link)

        miss = 0
        count = 0
        for wiki in directory.iterdir():
            if wiki.is_file() and wiki.stem.startswith('enwiki'):
                for root in self.xml_parser.from_xml(str(wiki)):
                    count += 1

                    if count > 20000:
                        writer.commit()
                        writer = self.index.writer(limitmb=2048, procs=N_PROC, multisegment=True)
                        count = 0

                    listener = None
                    try:
                        id, title, text = self.xml_parser.get(root)
                        listener = compiler.on(lambda node: parse_link(node, title.text), ParseTypes.LINK)
                        logger.info(f'{title.text} compiling')
                        article = compiler.compile(text.text)
                        writer.add_document(title=title.text, text=article, categories=','.join(categories), id=f'{id}')
                        logger.info(f'{title.text} indexed')
                        listener and listener()  # Remove listeners
                        article_title = normalize_title(title.text)
                        adj_graph_str = " ".join(reverse_graph)
                        file_adjlist.write(article_title + " " + adj_graph_str + "\n")
                        categories.clear()
                        reverse_graph.clear()
                    except (ParseError, MalformedTag, RedirectFound) as e:
                        miss += 1
                        listener and listener()  # Remove listeners
                        logger.warning(f'{title.text} {e.type}, skipping')
                        continue

        if miss > 0:
            logger.warning(f'{miss} articles ignored')

        writer.commit()

        file_adjlist.close()

        adj = Adjacency()

        adj.load_from_index()

        adj.write_adjlist_clean()

        pr = PageRank()

        pr.load_adjlist()

        pr.load_graphml()

        pr.generate_rank()


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
