import unittest
import logging
from pathlib import Path
from preprocessing.analyzer import WikimediaAnalyzer
from whoosh.analysis import RegexTokenizer
from parsing.compiler import Compiler

logging.basicConfig(level=logging.INFO)

DATA_FOLDER = Path(__file__).parent / 'data'


class TestIndex(unittest.TestCase):

    def test_compile(self, file='wikitext'):
        with (DATA_FOLDER / file).open(encoding="utf8") as f:
            text = f.read()
            result = Compiler().compile(text)
            tokens = WikimediaAnalyzer()(result)
            print(" ".join([i.text for i in tokens]))


if __name__ == '__main__':
    unittest.main()
