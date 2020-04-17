from whoosh.analysis import StemmingAnalyzer
from whoosh.analysis import StandardAnalyzer, Analyzer, CompositeAnalyzer
from whoosh.analysis.filters import Filter
from whoosh.analysis.filters import STOP_WORDS

GOOGLE_STOP_WORDS = frozenset(('I', 'a', 'about', 'an', 'are', 'as', 'at', 'be', 'by', 'com', 'for', 'from',
                               'how', 'in', 'is', 'it', 'of', 'on', 'or', 'that', 'the', 'this', 'to', 'was',
                               'what', 'when', 'where', 'who', 'will', 'with', 'the',
                               'www'))


class WikitextFilter(Filter):
    def __call__(self, tokens):
        for token in tokens:
            yield token


class WikimediaAnalyzer:

    def __call__(self, value, **kwargs):

        ret = StandardAnalyzer(stoplist=GOOGLE_STOP_WORDS)(value, **kwargs)

        # chain = ret | WikitextFilter()

        return ret
