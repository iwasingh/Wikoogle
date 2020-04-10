import logging
from .combinators import sor
import src.parsing.lexer as lexer

logger = logging.getLogger('Parser')

"""A recursive descent parser implementation
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
        assert isinstance(node, Node)
        self.children.append(node)

    def __str__(self):
        ret = '(' + self.value.__str__() + ' '
        for child in self.children:
            ret += child.__str__()
        return ret + ')'

    def __repr__(self):
        return self.__str__()


class Parser:
    def __init__(self, tokens):
        print(tokens, len(tokens))
        self._tokens = iter(tokens)
        self._ast = Node()
        self._index = -1
        self._current = None
        self._grammar = Grammar()

    def parse(self):
        expression = self._grammar.expression()
        self.next()
        while self.current.token != lexer.Lexer.EOF:
            result = expression(self)
            if result:
                self._ast.add(result)
            else:
                self.next()

        print(self._ast)

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


# def epsilon(self):
#     return
#     pass


class Grammar:
    """Handles the grammar on which the parser will depend upon
    As said before, each production rule is described in the EBNF form and might be simplified from the original one
    """

    rules = {
        # 'TEMPLATE': lexer.TemplateT.parse,
        # 'LINK': lexer.LinkT.parse,
        # 'TEXT': lexer.Text.parse,
    }

    def __init__(self):
        pass

    # Add additional rules
    def rule(self, rule):
        pass

    def expression(self):
        """
        Wikimedia primary expression

        ε : = text
        expression := template
                        | heading_2
                        | link
                        | ε
        :param parser:
        :return:
        """
        # sor(*Grammar.rules.values())
        return sor(
            self.template,
            self.link,
            self.epsilon
        )

    @staticmethod
    def template(parser):
        """Template grammar
        Wikimedia ABNF
        template = "{{", title, { "|", part }, "}}" ;
        part     = [ name, "=" ], value ;
        title    = text ;

        ------

        Internal
        text          := ε
        template      := '{{' text '}}'

        Templates are used to call functions and do some particular formatting
        Only the title might be necessary, this is why the template is simplified with a simple text inside brackets

        :param parser:
        :return:
        """
        return lexer.TemplateT.parse(parser)

    @staticmethod
    def link(parser):
        """Link grammar
        Wikimedia EBNF

        start link    = "[[";
        end link      = "]]";
        internal link = start link, full pagename, ["|", label], end link,

        ------
        Internal

        pagename   := ε
        link            := '[[' pagename ']]'

        The link contain the page name, i don't consider the optional ["|", label] for now, which is used for the link parameter
        If that is relevant for index purposes, create a not-terminal function and call it inside parse in lexer.LinkT

        :param parser:
        :return:
        """
        return lexer.LinkT.parse(parser)

    @staticmethod
    def heading_2():
        """Heading 2
        A heading
        """
        return lexer.HeadingT.parse

    @staticmethod
    def epsilon(parser):
        """Basic epsilon that consume the token and proceed aka Text for now.
        Maybe i'll further extend this to handle cases like left-recursion but for now there aren't recursive rules

        :param parser:
        :return:
        """
        return lexer.Text.parse(parser)


# def TEXT(parser):
#     if parser.current.token == Text.start:
#         token = parser.current
#         parser.next()
#         return Node(TextP(token.text))
#
#     logging.info('TEXT_NOT_FOUND')
#     return None
#
#
# def TEMPLATE(parser):
#     rule = seq(expect(TemplateT.start), TEXT, expect(TemplateT.end))
#     result = pipe(parser, rule, extract)
#     if result:
#         return Node(TemplateP(result.value))
#     return False
#
#
# def LINK(parser):
#     rule = seq(expect(LinkT.start), TEXT, expect(LinkT.end))
#     result = pipe(parser, rule, extract)
#     if result:
#         return Node(LinkP(result.value))
#     return False
#

# def WIKIMEDIA(parser):
#     ast = Node()
#     ast.add(lexer.TemplateT(parser))
#     # for i in [TEMPLATE()]:
#     #     ast.add(i(parser))
#     #
#     # return sor(TEXT, TEMPLATE, LINK)(parser)


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
