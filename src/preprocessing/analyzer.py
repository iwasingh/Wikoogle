from whoosh.analysis import StemmingAnalyzer
from whoosh.analysis import StandardAnalyzer, Analyzer, CompositeAnalyzer
from whoosh.analysis.filters import Filter
from whoosh.analysis.filters import STOP_WORDS

GOOGLE_STOP_WORDS = frozenset(('I', 'a', 'about', 'an', 'are', 'as', 'at', 'be', 'by', 'com', 'for', 'from',
                               'how', 'in', 'is', 'it', 'of', 'on', 'or', 'that', 'the', 'this', 'to', 'was',
                               'what', 'when', 'where', 'who', 'will', 'with', 'the',
                               'www')).union(STOP_WORDS)


class WikitextFilter(Filter):
    # def __init__(self):
    #     super().__init__()

    def __call__(self, tokens):
        for token in tokens:
            yield token


def WikimediaAnalyzer():

    ret = StandardAnalyzer(stoplist=GOOGLE_STOP_WORDS)

    # chain = ret | WikitextFilter()

    return ret

def HighlightAnalyzer():
    ret = StandardAnalyzer(stoplist=None)
    return ret
