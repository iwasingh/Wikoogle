import unittest
import logging
from pathlib import Path
from preprocessing.analyzer import WikiNormalizer, WikimediaAnalyzer
from whoosh.analysis import RegexTokenizer
from parsing.compiler import Compiler
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


if __name__ == '__main__':
    unittest.main()