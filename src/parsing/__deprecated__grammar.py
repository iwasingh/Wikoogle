from .lexer import Lexer, Symbol, Tag, Token
# from .utils import recursive, RecursiveMatch
# from .combinators import pipe, expect, extract, seq, sor
# import re
#
# @Lexer.symbol(Symbol.RESERVED)
# class TemplateT(Tag):
#     start = Token('TEMPLATE_START', r'{{')
#     end = Token('TEMPLATE_END', r'}}')
#
#     def __init__(self):
#         super().__init__(self.start, self.end)
#         # self._context = context
#
#     def match(self, text, pos, **kwargs):
#         return recursive(text, self.start, self.end, pos), self.start
#
#     @staticmethod
#     def parse(parser):
#         result = pipe(
#             parser,
#             seq(expect(TemplateT.start),
#                 Text.parse,
#                 expect(TemplateT.end)),
#             extract)
#         if result:
#             return parser.Node(parser.TemplateP(result.value))
#         return None
#         # result = pipe(parser, rule, extract)
#         # if result:
#         #     return Node(TemplateP(result.value))
#         # return False
#         # pass
#
#
# @Lexer.symbol(Symbol.RESERVED)
# class LinkT(Tag):
#     start = Token('LINK_START', r'\[\[')
#     end = Token('LINK_END', r']]')
#
#     def __init__(self):
#         super().__init__(self.start, self.end)
#
#     @staticmethod
#     def parse(parser):
#         """Link grammar
#             Wikimedia EBNF
#                 start link    = "[[";
#                 end link      = "]]";
#                 internal link = start link, full pagename, ["|", label], end link,
#             ------
#             Internal
#                 full pagename          := ε
#                 link                   := '[[' full pagename ']]'
#
#                 The link contain the pagename, i don't consider the optional | for now.
#             """
#         pass
#
#
# @Lexer.symbol(Symbol.RESERVED)
# class HeadingT(Tag):
#     start = Token('HEADING_2', r'==')
#     end = Token('HEADING_2', r'==')
#
#     def __init__(self):
#         super().__init__(self.start, self.end)
#
#     @staticmethod
#     def parse(parser):
#         pass
#
#
# @Lexer.symbol(Symbol.ID)
# class Text(Tag):
#     tags = [symbol.start.regex + '|' + symbol.end.regex for symbol in Lexer.table[Symbol.RESERVED]]
#     start = Token('TEXT', '.*?(?={0})'.format('|'.join(tags), re.DOTALL))
#     end = start  # None or NoneToken
#
#     def __init__(self):
#         super().__init__(self.start, self.end)
#
#     @staticmethod
#     def parse(parser):
#         pass
#
#
# @Lexer.symbol(Symbol.IGNORE)
# class Ignore:
#     def __init__(self):
#         self._regex = re.compile('\n|\\s')
#
#     def match(self, text, pos, **kwargs):
#         return self._regex.match(text, pos)
