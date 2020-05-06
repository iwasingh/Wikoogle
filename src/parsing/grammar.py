import logging
import re
import parsing.parser as p
from .combinators import pipe, expect, extract, seq, sor, rep, ParseError
from .symbols import Template, Text, Link, Heading, Heading6, Heading5, Heading4, Heading3, Comment, Bold, ItalicAndBold, Italic
from .utils import recursive

# import src.parsing.lexer as l

logger = logging.getLogger('Grammar')


# TODO move symbols in a own file
class Grammar:
    """Handles the grammar on which the parser will depend upon
    Each production rule is described in the EBNF or ABNF form and might be simplified from the original one
    You can find the grammar for Wikimedia in the ABNF form here(https://www.mediawiki.org/wiki/Preprocessor_ABNF).
    An internal grammar definition might be used because for index purpose some rules are useless
    """

    rules = {}

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
            self.headings,
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
        Only the title might be necessary, this is why the template is simplified with a simple text inside brackets,
        therefore there is no recursion.

        :param parser:
        :return:
        """
        result = pipe(parser,
                      seq(expect(Template.start), Grammar.epsilon, expect(Template.end)),
                      extract)
        if result:
            return p.Node(p.TemplateP(result.value))
        return None
        # return TemplateT.parse(parser)

    @staticmethod
    def link(parser):
        """Link grammar
        Wikimedia EBNF

        start link    = "[[";
        end link      = "]]";
        internal link = start link, full pagename, ["|", label], end link,

        ---
        Internal

        pagename   := ε
        expression := template
                        | link
                        | ε

        link            := '[[' pagename, { expression } ']]'

        The link contain the page name, and 0 or more repetitions of the expression ["|", label]. That is simplified with
        an expression that can by any one of the wikimedia non-terminals (text, template, link for now)
        Watch out left recursion (a link can contain a link)

        TODO add external link too, https://en.wikipedia.org/wiki/Help:Link#External_links
        :param parser:
        :return:
        """

        # expression = sor(expect(Link.end), rep(sor(Grammar.epsilon, Grammar.template, Grammar.link), Link.end))

        def extractor(arr):
            return (lambda _, c, children, __: (c, children))(*arr)

        result = pipe(parser,
                      seq(expect(Link.start),
                          Grammar.epsilon,
                          rep(sor(Grammar.epsilon, Grammar.template, Grammar.link), Link.end),
                          expect(Link.end)),
                      extractor)

        if result:
            (content, nodes) = result
            node = p.LinkNode(p.LinkP(content.value))
            for n in nodes:
                node.add(n)
            return node
        return None

    @staticmethod
    def headings(parser):
        """ Heading
        Wikimedia EBNF
        header end  = [whitespace], line break;
        header6     = line break, "======", [whitespace], text, [whitespace], "======", header end;
        header5     = line break, "=====",  [whitespace], text, [whitespace], "=====",  header end;
        header4     = line break, "====",   [whitespace], text, [whitespace], "====",   header end;
        header3     = line break, "===",    [whitespace], text, [whitespace], "===",    header end;
        header2     = line break, "==",     [whitespace], text, [whitespace], "==",     header end;

        ---
        Internal EBNF
        header6     = "======", text, "======";
        header5     = "=====", text, "=====";
        header4     = "====", text, "====";
        header3     = "===", text, "===";
        header2     = "==", text, "==";

        NOTE: Linebreak is one of the ignored character in the lexer, i should consider them TODO

        """
        precedence = [
            Heading6,
            Heading5,
            Heading4,
            Heading3,
            Heading
        ]
        try:
            result = pipe(parser, sor(*[seq(expect(i.start), Grammar.epsilon, expect(i.end)) for i in precedence]),
                          extract)
        except ParseError as e:
            raise e

        if result:
            return p.Node(p.HeadingP(result.value))

        return None

    @staticmethod
    def text(parser):
        return Grammar.epsilon(parser)

    @staticmethod
    def epsilon(parser):
        """Basic epsilon that consume the token and proceed aka Text for now.
        Maybe i'll further extend this to handle cases like left-recursion

        :param parser:
        :return:
        """
        result = expect(Text.start)(parser)
        if result:
            return p.Node(p.TextP(result.text))
        return None

    @staticmethod
    def linebreak(parser):
        pass

    @staticmethod
    def table(parser):
        """Table grammar

        Tables are threatened as text, hence will be indexed including formatting attributes not
        useful for indexing purpose
        """
        pass

    @staticmethod
    def comment(parser):
        result = pipe(parser,
                      seq(expect(Comment.start), Grammar.epsilon, expect(Comment.end)),
                      extract)
        if result:
            return p.Node(p.CommentP(result.value))
        return None

    # @staticmethod
    # def formatting(parser):
    #     result = pipe(parser, sor())
