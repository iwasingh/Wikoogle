import sys
import logging
from pathlib import Path
# from preprocessing import index
from preprocessing.index import WikiIndex
from searching.searcher import Searcher


def main():
    wikimedia_ix = WikiIndex().get('__index')
    # wikimedia_ix.build()

    searcher = Searcher(wikimedia_ix)

    while True:
        query = input('Insert query \n')
        if query == 'exit':
            break

        results = searcher.search(query)


if __name__ == '__main__':
    main()
