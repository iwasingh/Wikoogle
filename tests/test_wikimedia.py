import unittest
import logging
from src.parsing.wikimedia import Lexer, Parser
from pathlib import Path
import re

DATA_FOLDER = Path(__file__).parent / 'data'

logging.basicConfig(level=logging.INFO)

class TestPars(unittest.TestCase):
    def test_template(self):
        print(match_template())
        # self.test_tokenize(name='template')

    def test_tokenize(self, name='wikitext'):
        """
        Test tokenizer

        """
        with (DATA_FOLDER / name).open(encoding="utf8") as f:
            text = f.read()
            lexer = Lexer()
            tokens = lexer.tokenize(text)
            logging.info(tokens)
            logging.info('TEXT_LENGTH: {0}'.format(len(text)))
            self.assertGreater(len(tokens), 0)

    # def test_parse(self):
    #     """
    #     Test parser
    #     """
    #     # tokens = ['{{', ]
    #     print(tokens)
    #     parser = Parser(tokens)
    #     ast = parser.parse()
    #     print(ast)


if __name__ == '__main__':
    unittest.main()
