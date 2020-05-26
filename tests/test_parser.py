import unittest
import logging
import time
from pathlib import Path
from parsing.lexer import Lexer
from parsing.parser import TemplateP, Parser
from parsing.compiler import Compiler, ParseTypes
from parsing.grammar import Grammar

logging.basicConfig(level=logging.INFO)

DATA_FOLDER = Path(__file__).parent / 'data'


class TestParser(unittest.TestCase):
    lexer = Lexer()
    grammar = Grammar()

    def test_parse(self, name='wikitext'):
        with (DATA_FOLDER / name).open(encoding="utf8") as f:
            text = f.read()
            t0 = time.time()
            # lexer = Lexer()
            # tokens = lexer.tokenize(text)
            parser = Parser()
            ast = parser.parse(text)
            t1 = time.time()
            # print(ast)
            print('Ast built in: ', t1 - t0)
            return ast

    def test_template(self):
        parser = Parser()
        ast = parser.parse('{{asd}}', Grammar.template)
        print(ast)
        return ast
        # Todo assert

    def test_link(self):
        txt = '[[File:Nearest_stars_rotating_red-green.gif|alt=Rotating 3D image of the nearest stars|thumb|Animated 3D map of the nearest stars, centered on the Sun. {{3d glasses|color=red green}}]]'
        txt2 = '[[File:William Shea.jpg|thumb|upright|[[William Shea]] was instrumental in returning [[National League|National League baseball| [[asd|{{asd}}]]]] to [[New York City]] after five years of absence.]]'
        txt3 = '[[asd]]'
        parser = Parser()
        ast = parser.parse(txt2, Grammar.link)

        print(ast)
        return ast

    def test_headings(self):
        txt = '==asd=='
        txt3 = '===asd==='
        txt4 = '====asd===='
        txt5 = '=====asd====='
        txt6 = '======asd======'
        parser = Parser()
        ast = parser.parse(txt, expression=Grammar.headings)
        print(ast)
        return ast

    def test_compile(self, file='wikitext'):
        with (DATA_FOLDER / file).open(encoding="utf8") as f:
            text = f.read()
            result = Compiler().render(self.test_parse(name=file))
            print(result)
            print('---STATS---')
            print('Wikimedia length', len(text))
            print('Wikoogle length', len(result))
            print('Page compressed for about,', '{:.1%}'.format(len(result) / len(text)))

    def test_comment(self):
        txt = '&lt;!-- In the interest of restricting article length, please limit this section to two or three short ' \
              'paragraphs and add any substantial information to the main Issues in anarchism article. Thank you. ' \
              '--&gt; '
        parser = Parser()
        ast = parser.parse(txt, Grammar.comment)
        print(ast, Compiler().render(ast))

    def test_listener(self):
        def listener(node):
            if node.value.text.startswith('Category'):
                print(node.value.text)

        compiler = Compiler()
        compiler.on(listener, ParseTypes.LINK)
        result = compiler.render(self.test_parse())