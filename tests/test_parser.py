import unittest
import logging
import time
from pathlib import Path
from src.parsing.lexer import Lexer
from src.parsing.parser import TemplateP, Parser

logging.basicConfig(level=logging.INFO)

DATA_FOLDER = Path(__file__).parent / 'data'


class TestParser(unittest.TestCase):
    # def test_template(self, name='wikitext'):
    #     """
    #     Test tokenizer
    #
    #     """
    #     with (DATA_FOLDER / name).open(encoding="utf8") as f:
    #         text = f.read()
    #         lexer = Lexer()
    #         tokens = lexer.tokenize(text)
    #         parser = Parser(tokens)
    #
    #         TemplateP().parse(parser)

    def test_parse(self, name='wikitext'):
        with (DATA_FOLDER / name).open(encoding="utf8") as f:
            text = f.read()
            lexer = Lexer()
            tokens = lexer.tokenize('{{asd}}')
            parser = Parser(tokens)
            parser.parse()
