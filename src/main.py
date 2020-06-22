from flask import Flask, request, render_template, session, redirect, url_for
from preprocessing.index import WikiIndex
from pagerank.pagerank import PageRank
from searching.searcher import Searcher
import yaml
import config
import logging
import logging.config
import os

__logger = None
__wikimedia_ix = None
__page_rank = None
__searcher = None

"""
TODO stats and content compression,
"""


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


def get_page_rank():
    global __page_rank

    if __page_rank is not None:
        return __page_rank

    print(' * Bootstrap PageRank')

    __page_rank = PageRank()
    __page_rank.get()

    return __page_rank


def get_searcher():
    global __searcher

    if __searcher is not None:
        return __searcher

    print(' * Bootstrap Searcher')

    __searcher = Searcher(get_wikimedia_ix(), get_page_rank())

    return __searcher


app = Flask(__name__, template_folder="layouts")

# TODO move from here
app.secret_key = "b_W]qG>[ \xe1)\xea\xe8H\xf9\xc0\xa0"


@app.route('/')
def show_index():
    return render_template('homepage.html', session=session)


@app.route('/search')
def search_results():
    # return render_template(
    #     'resultpage.html',
    #     results=[]
    # )
    queryAllFields = request.args.get("q", "")

    # query = [t.text for t in StandardAnalyzer()(queryAllFields)]
    results = get_searcher().search(queryAllFields, session)
    # results = [map_result_to_temp(r, query) for r in results]

    return render_template(
        'resultpage.html',
        results=results
    )


@app.route('/settings', methods=['GET', 'POST'])
def settings():

    if request.method == 'POST':
        session['results_limit'] = request.form['results_limit']
        session['page_rank_lvl'] = request.form['page_rank_lvl']
        session['query_expansion'] = request.form['query_expansion']
        session['ranking'] = request.form['ranking']
        session['link_analysis'] = request.form['link_analysis']
        # if 'page_rank' in request.form:
        #     session['page_rank'] = request.form['page_rank']
        return redirect('/')

    return session


def warm_modules():
    get_logger()
    get_wikimedia_ix()
    get_page_rank()
    get_searcher()


if __name__ == 'src.main':
    # # https://stackoverflow.com/questions/25504149/why-does-running-the-flask-dev-server-run-itself-twice/25504196
    # lazy_loading(warm_modules)
    warm_modules()
