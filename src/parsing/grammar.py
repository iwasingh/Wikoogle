import logging
import re
import src.parsing.parser as p
from .combinators import pipe, expect, extract, seq, sor, rep
from .symbols import Template, Text, Link, Heading
from .utils import recursive

# import src.parsing.lexer as l

logger = logging.getLogger('Grammar')

""" Grammar definition """


# TODO move symbols in a own file
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
            # self.heading_2,
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

    # """Internal test method """
    # @staticmethod
    # def _link_expr(parser):
    #     # if parser.current.token == Link.end:
    #     #     return
    #
    #     return sor(Grammar.template, Grammar._link, Grammar.epsilon)(parser)
    #
    # """Internal test method """
    # @staticmethod
    # def _link(parser):
    #     if parser.current.token == Link.start:
    #         parser.next()
    #         text = parser.current
    #         node = p.Node(p.LinkP(text.text))
    #         parser.next()
    #         while parser.current.token != Link.end:
    #             result = Grammar._link_expr(parser)
    #             if result:
    #                 # breakpoint()
    #                 node.add(result)
    #         parser.next()
    #         return node

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
        expression := template
                        | link
                        | ε

        link            := '[[' pagename { expression } ']]'

        The link contain the page name, and 0 or more repetitions of the expression ["|", label]. That is simplified with
        an expression that can by any one of the wikimedia non-terminals (text, template, link for now)
        Watch out left recursion (a link can contain a link)

        link := '[[' pagename expr
        expr := ']]' | {expression}
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
            # breakpoint()
            (content, nodes) = result
            node = p.Node(p.LinkP(content.value))
            for n in nodes:
                node.add(n)
            return node
        return None

    @staticmethod
    def heading_2(parser):
        """Heading 2
        A heading
        """
        result = pipe(parser,
                      seq(expect(Heading.start), Grammar.epsilon, expect(Heading.end)),
                      extract)

        if result:
            return p.Node(p.HeadingP(result.value))

        return None
        # return HeadingT.parse(parser)

    @staticmethod
    def text(parser):
        return Grammar.epsilon(parser)

    @staticmethod
    def epsilon(parser):
        """Basic epsilon that consume the token and proceed aka Text for now.
        Maybe i'll further extend this to handle cases like left-recursion but for now there aren't recursive rules

        :param parser:
        :return:
        """
        result = expect(Text.start)(parser)
        if result:
            return p.Node(p.TextP(result.text))
        return None
