from io import StringIO
import re
from .parser import Parser
from .lexer import Lexer
from .grammar import Grammar


class Compiler:
    def __init__(self):
        self.writer = StringIO()
        self.lexer = Lexer()
        self.grammar = Grammar()

    def render(self, node):
        """ Render function """
        self.writer = StringIO()
        node.compile(self.writer)
        result = self.writer.getvalue()
        self.writer.close()
        return result

    def compile(self, text):
        ast = Parser(self.lexer.tokenize(text)).parse(self.grammar.expression())
        return self.render(ast)
