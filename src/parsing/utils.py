import re

""" Recursive match helper that regular expressions can't handle """


def recursive(text, start, end, position):
    # match_start = re.compile(start, re.DOTALL)
    # match_end = re.compile(end, re.DOTALL)
    text_match = re.compile(r'.*?(?={0}|{1})'.format(start.regex, end.regex), re.DOTALL)
    stack = []
    index = position
    content = ''
    should_start = start.match(text, index)
    last_end = None

    if should_start:
        while True:
            is_start = start.match(text, index)
            is_end = end.match(text, index)
            txt = text_match.match(text, index)

            if is_start:
                stack.append(start)
                index = is_start.end()

            elif is_end:
                stack.pop()
                index = is_end.end()
                last_end = is_end

            elif txt:
                content += txt.group(0)
                index = txt.end()

            if not stack:
                rec = RecursiveMatch(should_start.start, index, [
                    (should_start, start),
                    (re.match(r'.*', content, re.DOTALL), content),
                    (last_end, end)])

                return rec
    return None


class RecursiveMatch:
    # Can't subclass re.Match
    def __init__(self, start, end, matches):
        self._start = start
        self._end = end
        self._matches = matches

    def end(self, pos=0):
        return self._end

    def start(self):
        return self._start

    @property
    def matches(self):
        return self._matches
