from whoosh import highlight
from whoosh.analysis import StandardAnalyzer, RegexAnalyzer, KeywordAnalyzer, SimpleAnalyzer, LowercaseFilter
from preprocessing.index import WikiIndex
from searching.searcher import Searcher
from flask import Flask, request, render_template

import yaml
import config
import logging
import logging.config

import nltk
from nltk.corpus import wordnet as wn
import re

__logger = None
__wikimedia_ix = None
__searcher = None


def get_logger():
    global __logger

    if __logger is not None:
        return __logger

    print(' * Bootstrap logger')

    with open(config.LOGZ, 'r') as file:
        try:
            log_config = yaml.load(file, Loader=yaml.SafeLoader)
            logging.config.dictConfig(log_config)
        except yaml.YAMLError as e:
            print('Error loading logger, using default config', e)

    __logger = logging.getLogger(__name__)

    return __logger


def get_wikimedia_ix():
    global __wikimedia_ix

    if __wikimedia_ix is not None:
        return __wikimedia_ix

    print(' * Bootstrap WikiIndex')

    __wikimedia_ix = WikiIndex().get('__index')

    return __wikimedia_ix


def get_searcher():
    global __searcher

    if __searcher is not None:
        return __searcher

    print(' * Bootstrap Searcher')

    __searcher = Searcher(get_wikimedia_ix())

    return __searcher


app = Flask(__name__, template_folder="layouts")


@app.route('/')
def show_index():
    return render_template('homepage.html')


@app.route('/search')
def search_results():
    queryAllFields = request.args.get("q", "")

    queryByTitle = request.args.get("title", "")
    queryByAuthor = request.args.get("author", "")
    queryByCategory = request.args.get("category", "")

    # query = [t.text for t in StandardAnalyzer()(queryAllFields)]

    results = get_searcher().search(queryAllFields)
    # results = [map_result_to_temp(r, query) for r in results]

    return render_template(
        'resultpage.html',
        results=results
    )


if __name__ == 'src.main':
    get_logger()
    get_wikimedia_ix()
    get_searcher()
