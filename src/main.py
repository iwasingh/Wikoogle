from preprocessing.index import WikiIndex
from searching.searcher import Searcher
import yaml
import config
import logging
import logging.config
from query import expander


def setup_logz():
    with open(config.LOGZ, 'r') as file:
        try:
            log_config = yaml.load(file, Loader=yaml.SafeLoader)
            logging.config.dictConfig(log_config)
        except yaml.YAMLError as e:
            print('Error loading logger, using default config', e)


def main():
    # setup_logz()

    # logger = logging.getLogger(__name__)

    # wikimedia_ix = WikiIndex().get('__index')
    # wikimedia_ix.build()

    # searcher = Searcher(wikimedia_ix)

    while True:
        query = input('Insert query \n')

        if query == 'exit':
            break

        # results = searcher.search(query)
        result = expander.expand(query)

        print(result)


if __name__ == '__main__':
    main()
    # test()
