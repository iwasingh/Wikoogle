import unittest
import logging
import time
from pathlib import Path
from src.parsing.lexer import Lexer
from src.parsing.parser import TemplateP, Parser
from src.parsing.grammar import Grammar
logging.basicConfig(level=logging.INFO)

DATA_FOLDER = Path(__file__).parent / 'data'


class TestParser(unittest.TestCase):
    lexer = Lexer()
    grammar = Grammar()
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
            t0 = time.time()
            lexer = Lexer()
            tokens = lexer.tokenize(text)
            parser = Parser(tokens)
            expression = Grammar().expression()
            ast = parser.parse(expression)
            t1 = time.time()
            print(ast)
            print('Ast built in: ', t1 - t0)

    def test_template(self):
        parser = Parser(self.lexer.tokenize('{{asd}}'))
        ast = parser.parse(Grammar.template)
        print(ast)
        # Todo assert

    def test_link(self):
        txt   = '[[File:Nearest_stars_rotating_red-green.gif|alt=Rotating 3D image of the nearest stars|thumb|Animated 3D map of the nearest stars, centered on the Sun. {{3d glasses|color=red green}}]]'
        txt2  = '[[File:William Shea.jpg|thumb|upright|[[William Shea]] was instrumental in returning [[National League|National League baseball| [[asd|{{asd}}]]]] to [[New York City]] after five years of absence.]]'
        txt3 = '[[asd]]'
        parser = Parser(self.lexer.tokenize(txt2))
        ast = parser.parse(Grammar.link)
        print(ast)

    def test_heading(self):
        txt = '==asd=='
        parser = Parser(self.lexer.tokenize(txt))
        ast = parser.parse(Grammar.heading_2)
        print(ast)