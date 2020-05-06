from whoosh import highlight
from whoosh.analysis import StandardAnalyzer, RegexAnalyzer, KeywordAnalyzer, SimpleAnalyzer, LowercaseFilter
from preprocessing.index import WikiIndex
from preprocessing.analyzer import HighlightAnalyzer
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


def StandardScorer(fragment):
    analyzer  = StandardAnalyzer()
    paragraph = fragment.text[fragment.startchar:fragment.endchar]
    tokens    = [token.text for token in analyzer(paragraph)]

    anarchism = wn.synsets('anarchism')[0]
    synsets = [wn.synsets(token) for token in tokens]
    synsets = [(tokens[idx], syn[0]) for idx, syn in enumerate(synsets) if len(syn) > 0]
    wup_print = [(tar[0], anarchism.wup_similarity(tar[1])) for tar in synsets]
    wup_similarity = [tar[1] for tar in wup_print]
    score = sum(filter(lambda wup: wup is not None and wup > 0.25 and wup < 1, wup_similarity)) / len(paragraph)

    # relative to sentence length
    # try speed up parsing synsets
    # remove == 1 matches

    print(wup_print)
    print("_______________________________________", score)

    return score * 100000

def map_result_to_temp(item, query):
    title = item["title"]
    analyzer = StandardAnalyzer(stoplist=None)
    
    text = highlight.highlight(
        item["text"],
        query,
        analyzer,
        highlight.SentenceFragmenter(maxchars=2**15),
        highlight.HtmlFormatter(),
        top=1,
        scorer=StandardScorer
    )
    
    return dict(title=item["title"], text=text)

@app.route('/')
def show_index():
    return render_template('homepage.html')
    
@app.route('/search')
def search_results():
    queryAllFields = request.args.get("q", "")

    queryByTitle = request.args.get("title", "")
    queryByAuthor = request.args.get("author", "")
    queryByCategory = request.args.get("category", "")

    query = [t.text for t in StandardAnalyzer()(queryAllFields)]

    results = get_searcher().search(queryAllFields)
    results = [map_result_to_temp(r, query) for r in results]

    return render_template(
        'resultpage.html',
        results=results
    )

if __name__ == 'src.main':
    get_logger()
    get_wikimedia_ix()
    get_searcher()
