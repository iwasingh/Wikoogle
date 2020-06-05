import logging
import re
from enum import Enum
from .symbols import Template, Link, Heading, Text, Token, Redirect, \
    Heading3, Heading4, Heading5, Heading6, Comment, Italic, ItalicAndBold, Bold, Tag, WIKIMEDIA_MARKUP, \
    IGNORED_TAGS

from .utils import RecursiveMatch, recursive, MalformedTag

logger = logging.getLogger('Lexer')


class Encoder:
    def __init__(self):
        pass

    def encode(self, text):
        return text


class Symbol(Enum):
    """
    Type of symbol
    """
    RESERVED = 'RESERVED'
    ID = 'ID'
    IGNORE = 'IGNORE'


class LexerToken(Token):
    def __init__(self, token, row, col, text=''):
        self._token = token
        self._row = row
        self._col = col
        self._text = text

        # TODO call super()

    @property
    def token(self):
        return self._token

    @property
    def text(self):
        return self._text

    def __repr__(self):
        # return self._text + '\n'
        return self.__str__()

    def __str__(self):
        return self._token.__repr__() + f' [{self._col}]'
        # return '\n' + self._text

    def __eq__(self, token):
        return self._token == token

    def __ne__(self, token):
        return not self.__eq__(token)


class EOFToken(LexerToken):
    def __init__(self, row, col):
        super().__init__(Lexer.EOF, row, col)


class Lexer:
    """
    Lexer that handles streams of character and delivers tokens
    """
    table = {
        Symbol.RESERVED: [],
        Symbol.ID: [],
        Symbol.IGNORE: []
    }

    EOF = Token('EOF')

    def __init__(self, encoder=Encoder()):
        self._row = 0  # Not used yet
        self._col = 0
        self.encoder = encoder

    def _tokenize(self, text, symbol_type):
        """
        Tokenizer
        :param text:
        :param symbol_type:
        :return:
        """
        text = self.encoder.encode(text)
        tokens = []

        # Debugging
        # if symbol_type == Symbol.ID: breakpoint()
        for symbol in self.table[symbol_type]:
            # try:
            match, token = symbol.match(text, self._col)
            # Find a better way to do it
            if match:
                if isinstance(match, RecursiveMatch):
                    for (m, t) in match.matches:
                        tokens.append(
                            LexerToken(t if isinstance(t, Token) else TextT.start,
                                       self._row,
                                       self._col,
                                       m.group(0)))

                else:
                    tokens.append(LexerToken(token, self._row, self._col, match.group(0)))

                self._col = match.end(0)
            # except MalformedTag as e:

        if len(tokens) == 0 and symbol_type == Symbol.ID:
            self._col += 1

        if self._col >= len(text):
            return tokens, None

        return tokens, Symbol.RESERVED if len(tokens) > 0 else Symbol.ID

    def tokenize(self, text):
        tokens = list()
        self._col = 0
        symbol_type = Symbol.RESERVED

        while self._col < len(text):
            for ignore in self.table[Symbol.IGNORE]:
                match = ignore.match(text, self._col)
                if match:
                    # print(match, text[match.start(0):match.end(0)])
                    self._col = match.end(0)
            else:
                resolved_tokens, next_symbol = self._tokenize(text, symbol_type)
                symbol_type = next_symbol
                tokens = tokens + resolved_tokens
                if symbol_type is None:
                    break

        tokens.append(EOFToken(self._row, self._col))
        logger.info('EOF')
        self._col += 1
        return tokens

    @classmethod
    def symbol(cls, symbol_type):
        def __wrap(symbol):
            if symbol_type in cls.table:
                cls.table[symbol_type].append(symbol())
            else:
                raise SymbolNotFoundError('Symbol definition missing')
            return symbol

        return __wrap


class SymbolNotFoundError(Exception):
    def __init__(self, message):
        super().__init__(message)


""" Lexer symbol definitions """


@Lexer.symbol(Symbol.RESERVED)
class TemplateT(Template):
    def __init__(self):
        super().__init__()

    def match(self, text, pos, **kwargs):
        return recursive(text, self.start, self.end, pos), self.start


# Lexer.symbol(Symbol.RESERVED)(Link)
@Lexer.symbol(Symbol.RESERVED)
class LinkT(Link):

    def __init__(self):
        super().__init__()


# Headings
# Lexer.symbol(Symbol.RESERVED)(Heading6)
# Lexer.symbol(Symbol.RESERVED)(Heading5)
# Lexer.symbol(Symbol.RESERVED)(Heading4)
# Lexer.symbol(Symbol.RESERVED)(Heading3)
# Lexer.symbol(Symbol.RESERVED)(Heading)

# Comment
Lexer.symbol(Symbol.RESERVED)(Comment)


@Lexer.symbol(Symbol.RESERVED)
class RedirectT(Redirect):
    def match(self, text, pos, **kwargs):
        if self.start.match(text, pos, **kwargs):
            raise RedirectFound(text)

        return None, self.start


# Formatting, whoosh automatically removes apices
# Lexer.symbol(Symbol.RESERVED)(ItalicAndBold)
# Lexer.symbol(Symbol.RESERVED)(Bold)
# Lexer.symbol(Symbol.RESERVED)(Italic)

@Lexer.symbol(Symbol.IGNORE)
class IgnoreTags:
    # start = Token('MATH_JAX_START', r'<math')
    # end = Token('MATH_JAX_END', r'')
    tags = [] + IGNORED_TAGS

    def __init__(self):
        self.regex = re.compile('|'.join(self.tags), re.DOTALL)

    def match(self, text, pos, **kwargs):
        return self.regex.match(text, pos, **kwargs)


@Lexer.symbol(Symbol.ID)
class TextT(Text):
    # TODO Copy here the logic in the base class
    # tags = [symbol.start.regex + '|' + symbol.end.regex for symbol in Lexer.table[Symbol.RESERVED]]
    # start = Token('TEXT', '.*?(?={0})|.*'.format('|'.join(tags), re.DOTALL))
    # end = start  # None or NoneToken

    def __init__(self):
        super().__init__()


# @Lexer.symbol(Symbol.IGNORE)
class Ignore:
    def __init__(self):
        self._regex = re.compile(r'\s')

    def match(self, text, pos, **kwargs):
        return self._regex.match(text, pos)


class RedirectFound(Exception):
    def __init__(self, message=''):
        self.type = 'RedirectFound'
        self.message = f"RedirectError: Redirect article"
