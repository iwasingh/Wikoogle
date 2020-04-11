import logging
from .combinators import sor
import src.parsing.lexer as lexer
import src.parsing.grammar as g

logger = logging.getLogger('Parser')

"""A recursive descent parser implementation LL(1) https://en.wikipedia.org/wiki/Recursive_descent_parser
You can find the grammar for Wikimedia in the ABNF form here(https://www.mediawiki.org/wiki/Preprocessor_ABNF),
this parser implements a context-free grammar and each rule is described in the proper method inside Grammar class.
Obviously this parser will not handle every production rule (non-terminal ones), in fact there are rules
that might be simplified and a internal grammar is used and explained in the EBNF form.

For indexing purpose i don't need too much, however it is pretty solid and can handle most of
them or can be further extended if necessary

"""


# TODO read
#  change .next() with .peak() in some combinators so there is at least 1 lookahead before consuming the
#  token. Current implementation should work anyway because the dump should be correct (no syntax errors, i hope so!)
#  therefore the parser assumes everything is correct. I raise a ParseError if something is wrong

class Node:
    def __init__(self, value=None):
        self.value = value
        self.children = []

    def add(self, node):
        # assert isinstance(node, Node)
        self.children.append(node)

    def __repr__(self):
        NodeVisitor.pretty_print(self)
        return ''


class NodeVisitor:
    @staticmethod
    def pretty_print(node, _prefix="", _last=True):
        print(_prefix, "`- " if _last else "|- ", node.value, sep="")
        _prefix += "   " if _last else "|  "
        child_count = len(node.children)
        for i, child in enumerate(node.children):
            _last = i == (child_count - 1)
            NodeVisitor.pretty_print(child, _prefix, _last)


class Parser:
    def __init__(self, tokens):
        logging.info(tokens)
        logger.info(len(tokens))
        self._tokens = iter(tokens)
        self._ast = Node()
        self._index = -1
        self._current = None
        # self._grammar = g.Grammar()

    def parse(self, expression):
        # expression = self._grammar.expression()
        self.next()
        while self.current.token != lexer.Lexer.EOF:
            result = expression(self)
            if result:
                self._ast.add(result)
            else:
                self.next()

        return self._ast

    def compile(self):

        pass

    def next(self):
        try:
            token = next(self._tokens)
            # logging.info('Next token: ' + repr(token))
            self._index = self._index + 1
            self._current = token
            return token
        except StopIteration:
            return None

    @property
    def index(self):
        return self._index

    @property
    def current(self):
        return self._current


class TextP:
    def __init__(self, text):
        self.text = text


class Expression:
    def __init__(self, node):
        self.content = node

    def compile(self):
        raise NotImplementedError()


class LinkP(Expression):
    def compile(self):
        pass


class TemplateP(Expression):
    def compile(self):
        pass


class HeadingP(Expression):
    def compile(self):
        pass

# class LinkNode(Node):
#     def __init__(self, content):
#         self.content = content
