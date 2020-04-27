from preprocessing.index import WikiIndex
from searching.searcher import Searcher
from flask import Flask, request, render_template

import yaml
import config
import logging
import logging.config


def setup_logz():
    with open(config.LOGZ, 'r') as file:
        try:
            log_config = yaml.load(file, Loader=yaml.SafeLoader)
            logging.config.dictConfig(log_config)
        except yaml.YAMLError as e:
            print('Error loading logger, using default config', e)


setup_logz()

logger = logging.getLogger(__name__)

wikimedia_ix = WikiIndex().get('__index')

searcher = Searcher(wikimedia_ix)

app = Flask(__name__, template_folder="layouts")

@app.route('/')
def show_index():
    return render_template('base.html')
    
@app.route('/search')
def search_results():
    print(searcher.search('anar'))
    return 'Ok'

