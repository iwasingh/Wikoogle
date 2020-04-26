import sys
import logging
from pathlib import Path
# from preprocessing import index
from preprocessing.index import WikiIndex
from searching.searcher import Searcher
from flask import Flask, request


wikimedia_ix = WikiIndex().get('__index')

searcher = Searcher(wikimedia_ix)

app = Flask(__name__)

@app.route('/search')
def search_results():
    print(searcher.search('anar'))
    return 'Ok'

