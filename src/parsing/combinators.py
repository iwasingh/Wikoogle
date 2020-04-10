""" Small set of combinator utilities """


class ParseError(Exception):
    def __init__(self, message=''):
        self.message = f"ParseError: {message}"


# Sequence of parsers
def seq(*args):
    def parse(parser):
        acc = []
        for i in args:
            result = i(parser)
            if result:
                acc.append(result)
            else:
                if len(acc) > 0:
                    breakpoint()
                    raise ParseError('Syntax error, bad token sequence')
                return None
        return acc

    return parse


# aka alternatives; or keyword is reserved, that's why this name
def sor(*args):
    def parse(parser):
        for i in args:
            result = i(parser)
            if result is not None:
                return result

        return None

    return parse


# Pipe
def pipe(arg, *args):
    last_result = arg
    for combinator in args:
        last_result = combinator(last_result)
        if last_result is None:
            return None
    return last_result


def expect(token):
    def parse(parser):
        # node = Node(token)
        current = parser.current
        # breakpoint()
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
