import logging
import re
# import src.parsing.lexer as lexer
import parsing.lexer as lexer
from .combinators import ParseError
import parsing.grammar as g

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
#  change .next() with .peek() in some combinator so there is at least 1 lookahead before consuming the
#  token. Current implementation should work anyway because the dump should be correct (no syntax errors, i hope so!)
#  therefore the parser assumes everything is correct. I raise a ParseError if something is wrong

class Node:
    """AST
                         Node(None)
            ________________|_______ ....
            |       |              |
    Node(TextP) Node(TemplateP)  LinkNode(LinkP)
                             ______|____
                            |         |
                    Node(Text)       LinkNode(LinkP)
                                      |
                                    ....
    """

    def __init__(self, value=None):
        self.value = value
        self.children = []

    def add(self, node):
        # assert isinstance(node, Node)
        self.children.append(node)

    def __repr__(self):
        NodeVisitor.pretty_print(self)
        return ''

    def compile(self, writer, parser):
        parser.notify(self)
        if self.value:
            self.value.render(writer)

        for children in self.children:
            children.compile(writer, parser)


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
    def __init__(self):
        self._tokens = iter([])
        self._ast = Node()
        self._index = -1
        self._current = None
        self._listeners = []
        self.lexer = lexer.Lexer()
        # self.expression =
        self._grammar = g.Grammar()

    def parse(self, text, expression=None):
        self._ast = Node()
        self._tokens = iter(self.lexer.tokenize(text))
        expression = expression if expression else self._grammar.expression()
        self.next()
        try:
            while self.current.token != lexer.Lexer.EOF:
                result = expression(self)
                if result:
                    self._ast.add(result)
                else:
                    self.next()

        except ParseError as e:
            raise e

        return self._ast

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

    def on(self, fn, type):
        self._listeners.append((fn, type))
        index = len(self._listeners) - 1

        def off():
            if index >= 0:
                self._listeners.pop(index)

        return off

    def notify(self, node):
        if node.value and len(self._listeners) > 0:
            for fn, type in self._listeners:
                if isinstance(node.value, type.value):
                    fn(node)


class Expression:
    def __init__(self, exp):
        self.expression = exp

    def render(self, writer):
        raise NotImplementedError()

    # def value(self):
    #     return self.expression


class TextP(Expression):
    def __init__(self, text):
        self.text = text

    def render(self, writer):
        writer.write(self.text)
        return self.text


class LinkP(Expression):
    category_match = re.compile(r'(?<=Category:).+')

    def __init__(self, node):
        self.text = node.text
        super().__init__(node)

    def render(self, writer):
        writer.write(self.text.split('|')[0])

    def category(self):
        return self.category_match.search(self.text)


class TemplateP(Expression):
    def __init__(self, node):
        self.text = ''

    def render(self, writer):
        # Ignore templates
        pass

    # def value(self):
    #     return ''


class CommentP(Expression):
    def __init__(self, node):
        self.text = node.text
        super().__init__(node)

    def render(self, writer):
        # Ignore comments
        pass

    # def value(self):
    #     return ''


class HeadingP(Expression):
    def __init__(self, node):
        super().__init__(node)
        # self.text = node.value()
        # if isinstance(node, TemplateP):
        self.text = node.text
        # else:
        #     self.text = ''

    def render(self, writer):
        writer.write(self.text)


class LinkNode(Node):
    # https://en.wikipedia.org/wiki/Wikipedia:Manual_of_Style/Linking
    media = re.compile('^(File:|Image:)')

    def __init__(self, value):
        self.text = value.text
        super().__init__(value)

    def is_media(self):
        return self.media.match(self.text)

    def compile(self, writer, parser):
        if not self.is_media():
            parser.notify(self)
            self.value.render(writer)
