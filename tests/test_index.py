import unittest
import logging
from pathlib import Path
from preprocessing.analyzer import WikiNormalizer, WikimediaAnalyzer
from whoosh.analysis import RegexTokenizer
from parsing.compiler import Compiler
from preprocessing.utils import clean
from preprocessing.index import WikiIndex
logging.basicConfig(level=logging.INFO)

DATA_FOLDER = Path(__file__).parent / 'data'


class TestIndex(unittest.TestCase):
    def test_wikinormalizer(self):
        tokenizer = RegexTokenizer(r"\w+(\.?\w+)*")
        normalizer = WikiNormalizer()
        # tokens = tokenizer(u'Hello world')
        # breakpoint()
        # tokens = [t.text for t in tokenizer()

        # logging.info(tokens)
        self.assertGreater(1, 0)

    def test_compile(self, file='wikitext'):
        with (DATA_FOLDER / file).open(encoding="utf8") as f:
            text = f.read()
            result = Compiler().compile(text)
            tokens = WikimediaAnalyzer()(result)
            print([i.text for i in tokens])

    def test_clean(self, file='wikitext'):
        with (DATA_FOLDER / file).open(encoding="utf8") as f:
            text = f.read()
            print(clean(text))

    def test_index(self):
        with (DATA_FOLDER / 'enwiki_test.xml').open(encoding="utf8") as f:
            text = f.read()
            index = WikiIndex().get('__test_index',  dump=DATA_FOLDER)


if __name__ == '__main__':
    unittest.main()
