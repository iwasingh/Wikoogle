from .lexer import TemplateT
import logging

logger = logging.getLogger('Parser')

"""LL(1) parser implementation
You can find the grammar in the ABNF form here(https://www.mediawiki.org/wiki/Preprocessor_ABNF),
this parser implements a context-free grammar and each rule is described in the proper class.
Obviously this parser will not handle every production, in fact there are rules
that might be simplified and a internal grammar is used and explained in the EBNF form.

For indexing purpose i don't need too much, however it is pretty solid and can handle most of
them or can be further extended if necessary

"""


class Node:
    def __init__(self, value=None):
        self.value = value
        self.children = []

    def add(self, node):
        assert isinstance(node, Node)
        self.children.append(node)

    def __str__(self):
        ret = '(' + self.value.__str__() + ' '
        for child in self.children:
            ret += child.__str__()
        return ret + ')'

    def __repr__(self):
        return self.__str__()


class ParseError(Exception):
    def __init__(self, message=''):
        self.message = f"ParseError: {message}"


# class TextP(Node):
#     def __init__(self, body):
#         super().__init__()
#         self._type = 'TEXT'
#         self.body = body
#         self._context = None
#
#     @staticmethod
#     def parse(context):
#         context.next()
#         return TextP(context.current)


# class LinkP(Node):
#     def __init__(self, text, link):
#         self._type = 'LINK'
#         self.text = text,
#         self.link = link


class Parser:
    def __init__(self, tokens):
        print(tokens, len(tokens))
        self._tokens = iter(tokens)
        self._ast = Node()
        self._index = -1
        self._current = None

    def parse(self):
        self.next()
        ast = WIKIMEDIA(self)
        print(ast)

    def next(self):
        try:
            token = next(self._tokens)
            logging.info('Next token: ' + repr(token))
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


# class S(tuple):
#    def __new__(cls, *args):
#        pass

# def s(*argv):
#    pass
# def
""" Small set of combinator utilities """


# Sequence of parser
def seq(*args):
    pass


# Pipe aka | aka OR aka alternative
def pipe(*args):
    pass


def expect(self):
    pass


def epsilon(self):
    pass


class Grammar:
    TEXT = terminal()
    TEMPLATE = seq()


def TEXT():
    def parse(parser):
        token = parser.current
        parser.next()
        return Node(TextP(token.text))

    return parse


def TEMPLATE():
    tag = TemplateT()

    def parse(parser):
        if parser.current == tag.start:
            parser.next()
            text = (TEXT())(parser)
            if parser.current == tag.end:
                parser.next()
                return Node(TemplateP(text.value))
        return Node(None)

    return parse


def WIKIMEDIA(parser):
    ast = Node()
    ast.add(TEMPLATE()(parser))
    # for i in [TEMPLATE()]:
    #     ast.add(i(parser))
    #

    return ast


class TextP:
    def __init__(self, text):
        self.text = text


class TemplateP:
    """Template grammar
    Wikimedia
        template = "{{", title, { "|", part }, "}}" ;
        part     = [ name, "=" ], value ;
        title    = balanced text ;
    ------
    Internal
        text          := ε
        template      := '{{' text '}}'

        Only the title might be necessary, this is why the template is simplified with a simple text inside brackets
    """

    def __init__(self, node):
        self.content = node
        # self.right
        # self._type = 'TEMPLATE'
        # self._symbol = TemplateT()
        # self._context = context
        #
        # self.body = body

    def compile(self):
        pass
    # def _template(self, context):
    #     if context.current == self._symbol.start:
    #         node = TemplateP()
    #         context.next()
    #         text_p = TextP.parse(context)
    #
    #         if context.current == self._symbol.end:
    #             return TemplateP
    #         # optional_p = self._optional()
    #         # while self._context.current == '|':
    #         #    self._optional()
    #
    #     # if(self._context.expect())
    #
    # def parse(self, context):
    #     # self._context = context
    #     return self._template(context)

    # def next(self):
