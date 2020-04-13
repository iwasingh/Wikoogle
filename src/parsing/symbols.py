import re
import logging
from abc import ABC

# from .utils import RecursiveMatch, recursive
logging = logging.getLogger('Symbols')


class Token:
    """
    Basic token
    """

    def __init__(self, tag, regex='', flags=0):
        self._tag = tag
        self._regex = regex
        self._match = re.compile(regex, flags)

    @property
    def tag(self):
        return self._tag

    @property
    def regex(self):
        return self._regex

    @property
    def re(self):
        return self._match

    def match(self, text, pos=0, **kwargs):
        return self._match.match(text, pos, **kwargs)

    def __str__(self):
        return self.tag

    def __repr__(self):
        return '({0})'.format(self.__str__())

    def __eq__(self, token):
        return self._tag == token.tag


class NoneToken(Token):
    def __init__(self):
        super().__init__('NONE')


class Tag(ABC):
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def match(self, text, pos, **kwargs):
        match = self.start.match(text, pos, **kwargs) or self.end.match(text, pos, **kwargs)
        token = None
        if match:
            token = self.start if match.re == self.start.re else self.end if match.re == self.end.re else NoneToken()
            if token.tag == 'NONE':
                logging.info('NONE token returned, there might be a problem')
        return match, token


class Template(Tag):
    start = Token('TEMPLATE_START', r'{{')
    end = Token('TEMPLATE_END', r'}}')

    def __init__(self):
        super().__init__(self.start, self.end)


class Link(Tag):
    start = Token('LINK_START', r'\[\[')
    end = Token('LINK_END', r']]')

    def __init__(self):
        super().__init__(self.start, self.end)


class Heading(Tag):
    """
    Equals signs are used for headings (must be at start of line)

    Must the after new line
    """
    start = Token('HEADING_2', r'==')
    end = Token('HEADING_2', r'==')

    def __init__(self):
        super().__init__(self.start, self.end)


class Heading3(Tag):
    start = Token('HEADING_3', r'===')
    end = Token('HEADING_3', r'===')

    def __init__(self):
        super().__init__(self.start, self.end)


class Heading4(Tag):
    start = Token('HEADING_4', r'====')
    end = Token('HEADING_4', r'====')

    def __init__(self):
        super().__init__(self.start, self.end)


class Heading5(Tag):
    start = Token('HEADING_5', r'=====')
    end = Token('HEADING_5', r'=====')

    def __init__(self):
        super().__init__(self.start, self.end)


class Heading6(Tag):
    start = Token('HEADING_6', r'======')
    end = Token('HEADING_6', r'======')

    def __init__(self):
        super().__init__(self.start, self.end)


class Table(Tag):
    pass


class Comment(Tag):
    pass


WIKIMEDIA_MARKUP = [
    Template(),
    Link(),
    Heading(),
    Heading3(),
    Heading4(),
    Heading5(),
    Heading6(),
]


class Text(Tag):
    # TODO do this in the lexer TextT class
    tags = [symbol.start.regex + '|' + symbol.end.regex for symbol in WIKIMEDIA_MARKUP]
    start = Token('TEXT', '.*?(?={0})|.*'.format('|'.join(tags), re.DOTALL))
    end = start  # None or NoneToken

    def __init__(self):
        super().__init__(self.start, self.end)
