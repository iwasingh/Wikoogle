from io import StringIO


# TODO move this tiny logic into the parser, the compilation process is simple

class Compiler:
    def __init__(self):
        self.writer = StringIO()

    def render(self, node):
        """ Render function """
        node.compile(self.writer)
        result = self.writer.getvalue()
        self.writer.close()
        return result
