from pathlib import Path
import os
ROOT = Path(__file__).parent.parent.resolve()
DUMP_FOLDER = ROOT / 'dumps'
LOGZ = ROOT / 'logz.yaml'
ASSETS_DATA = ROOT / '__assets'


def lazy_loading(f):
    # https://stackoverflow.com/questions/25504149/why-does-running-the-flask-dev-server-run-itself-twice/25504196
    if os.environ.get('FLASK_ENV') == 'development':
        if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
            f()
    else:
        f()