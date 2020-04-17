import sys
import logging
from pathlib import Path
# from preprocessing import index
from preprocessing.index import WikiIndex

DUMP_FOLDER = Path('./dumps')


# DUMP = '../dumps/'
# 'enwiki-20200120-pages-articles-multistream1.xml'
# 'wiki_test.xml'


def main():
    wikimedia = WikiIndex().get('__index')
    wikimedia.build()

    # w_parser = index.Parser(str(DUMP_FOLDER / 'enwiki-20200120-pages-articles-multistream1.xml'))
    # w_parser.parse()

    # schema = Schema(id=ID(stored=True),
    #                 title=TEXT(stored=True),
    #                 body=TEXT(),)
    #
    # if not Path('indexdir').exists():
    #     Path('indexdir').mkdir(exist_ok=True)
    # ix = index.create_in("indexdir", schema)
    # writer = ix.writer()
    # writer.add_document(title="Anarchism", id="12", body="""This is a example test about Anarchism""")
    # writer.add_document(title="Anarchic", id="13", body="""This is another about Anarchism anarchic""")
    # writer.commit()
    # try:
    #     searcher = ix.searcher()
    #     results = searcher.search(QueryParser("body", schema=ix.schema).parse(u'example about'))
    #     breakpoint()
    # finally:
    #     searcher.close()


if __name__ == '__main__':
    main()
