""" Small set of combinator utilities to combine rules """


class ParseError(Exception):
    def __init__(self, message=''):
        self.message = f"ParseError: {message}"


def seq(*args):
    """ Sequence of parsers """

    def parse(parser):
        acc = []
        for i in args:
            result = i(parser)
            if result is not None and result is not False:
                acc.append(result)
            else:
                if len(acc) > 0:
                    # breakpoint()
                    raise ParseError('Syntax error, bad token sequence')
                return None
        return acc

    return parse


def sor(*args):
    """ sor aka or aka alternative; "or" keyword is reserved, that's why this name """

    def parse(parser):
        for i in args:
            result = i(parser)
            if result is not None:
                return result

        return None

    return parse


def pipe(arg, *args):
    """ Pipe """
    last_result = arg
    for combinator in args:
        last_result = combinator(last_result)
        if last_result is None:
            return None
    return last_result


def expect(token):
    def parse(parser):
        current = parser.current
        if current and current.token == token:
            parser.next()
            return current
        return False

    return parse


def extract(result):
    if result:
        __left, content, __right = result
        return content
    return None


def opt():
    """ Optional """
    pass


def rep(expression, stop):
    """ One or more repetition """

    def parse(parser):
        acc = []
        while parser.current.token != stop:
            result = expression(parser)
            if result:
                acc.append(result)
        # parser.next()
        return acc

    return parse

# def extractor(arr, f):
#     return (lambda *f(): (content, nodes))(*arr)
