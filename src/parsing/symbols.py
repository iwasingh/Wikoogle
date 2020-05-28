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

    Must be after new line
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


# class Linebreak(Tag):
#     start = Token('LINE_BREAK', r'\n')
#     end = Token('LINE_BREAK', r'\n')
#
#     def __init__(self):
#         super().__init__(self.start, self.end)


class Table(Tag):
    start = Token('TABLE', r'{\|')
    end = Token('TABLE', r'\|}')

    def __init__(self):
        super().__init__(self.start, self.end)


class Comment(Tag):
    start = Token('COMMENT_START', r'&lt;!--')
    end = Token('COMMENT_END', r'--&gt;')

    def __init__(self):
        super().__init__(self.start, self.end)


class Bold(Tag):
    start = Token('BOLD', r"\'\'\'")
    end = Token('BOLD', r"\'\'\'")

    def __init__(self):
        super().__init__(self.start, self.end)


class Italic(Tag):
    start = Token('ITALIC', r"\'\'")
    end = Token('ITALIC', r"\'\'")

    def __init__(self):
        super().__init__(self.start, self.end)


class ItalicAndBold(Tag):
    start = Token('ITALIC_AND_BOLD', r"\'\'\'\'\'")
    end = Token('ITALIC_AND_BOLD', r"\'\'\'\'\'")

    def __init__(self):
        super().__init__(self.start, self.end)


WIKIMEDIA_MARKUP = [
    Template(),
    Link(),
    Heading(),
    Heading3(),
    Heading4(),
    Heading5(),
    Heading6(),
    Comment(),
    # Bold(),
    # Italic(),
    # ItalicAndBold(),
    # Table() For now tables are threatened as text, hence will be indexed, including formatting attributes not
    # useful for indexing purpose
]

IGNORED_TAGS = [
    r'<math[\s\S]*?<\/math\>',
    r'<\!--[\s\S]*?--\>',
    r'<syntaxhighlight[\s\S]*?<\/syntaxhighlight\>',
    r'<code[\s\S]*?<\/code\>',
    r'<gallery[\s\S]*?<\/gallery\>',
    # r'<ref[\s\S]*?[<]?\/ref\>',
    # r'<[\s\S]*?<\/[\S]*?\>',
    # r'<\!--[\s\S]*?--\>|<[\s\S]*?\>*?[<]?\/[\S]*?\>'
    # r'<[^>]*?[^>]\/>'
]


class Text(Tag):
    # TODO do this in the lexer TextT class
    tags = [symbol.start.regex + '|' + symbol.end.regex for symbol in WIKIMEDIA_MARKUP]
    reserved = '({0})'.format('|'.join(IGNORED_TAGS + tags))
    start = Token('TEXT', r'(.+?(?={0}))|(.+(?!{0}))'.format(reserved), re.DOTALL)
    # print(r'(.+?(?={0}))|(.+(?!{0}))'.format(reserved))
    end = start  # None or NoneToken

    # start = Token('TEXT', '.*?(?={0})|.*'.format('|'.join(tags)))

    def __init__(self):
        super().__init__(self.start, self.end)
