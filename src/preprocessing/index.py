import sys
import logging
import sys
from lxml import etree
from whoosh.fields import TEXT, ID, SchemaClass, KEYWORD
from whoosh import index
from parsing.combinators import ParseError
from pagerank.pagerank import normalize_title
from .analyzer import WikimediaAnalyzer
import config
from parsing.compiler import Compiler, ParseTypes
import shutil
from parsing.utils import MalformedTag
from parsing.lexer import RedirectFound

logger = logging.getLogger('preprocessing')

WAnalyzer = WikimediaAnalyzer(cachesize=-1)


class WikiSchema(SchemaClass):
    id = ID(stored=True)
    title = TEXT(stored=True, analyzer=WAnalyzer, field_boost=2.0)
    text = TEXT(stored=True, analyzer=WAnalyzer)
    categories = KEYWORD(stored=True, analyzer=WAnalyzer, scorable=True, lowercase=True, commas=True)


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

        writer = self.index.writer(limitmb=1024, procs=4)

        compiler = Compiler()

        categories = []

        all_articles = []
        link_graph = {}

        def output_file(link_graph_in):
            lines = []
            f = open("graph.txt", "w")
            for article_title in link_graph_in:
                if len(link_graph_in[article_title]):
                    lines.append("{} {}".format(article_title, " ".join(link_graph_in[article_title])))
            f.write("\n".join(lines))
            f.close()

        def apply_filters(link_graph_in):
            link_graph_clean = {}
            for article_title in all_articles:
                link_graph_clean[article_title] = link_graph_in.get(article_title, [])
            return link_graph_clean

        def parse_link(node, article):
            category = node.value.category()

            if category:
                categories.append(category.group())
            else:
                article_title = normalize_title(article)
                article_link = normalize_title(node.value.text)
                article_graph = link_graph.get(article_link, [])

                if article_title not in article_graph:
                    article_graph.append(article_title)
                    link_graph[article_link] = article_graph

        miss = 0
        for wiki in directory.iterdir():
            if wiki.is_file() and wiki.stem.startswith('enwiki'):
                for root in self.xml_parser.from_xml(str(wiki)):
                    listener = None
                    try:
                        id, title, text = self.xml_parser.get(root)
                        listener = compiler.on(lambda node: parse_link(node, title.text), ParseTypes.LINK)
                        logger.info(f'{title.text} compiling')
                        article = compiler.compile(text.text)
                        writer.add_document(title=title.text, text=article, categories=','.join(categories), id=f'{id}')
                        logger.info(f'{title.text} indexed')
                        listener and listener() # Remove listeners
                        categories.clear()
                        all_articles.append(normalize_title(title.text))
                    except (ParseError, MalformedTag, RedirectFound) as e:
                        miss += 1
                        listener and listener() # Remove listeners
                        logger.warning(f'{title.text} {e.type}, skipping')
                        continue

        if miss > 0:
            logger.warning(f'{miss} articles ignored')

        output_file(apply_filters(link_graph))

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
