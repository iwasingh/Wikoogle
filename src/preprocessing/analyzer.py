from whoosh.analysis import StemmingAnalyzer
from whoosh.analysis import StandardAnalyzer, Analyzer, CompositeAnalyzer
from whoosh.analysis.filters import Filter, SubstitutionFilter
from whoosh.analysis.morph import StemFilter
from whoosh.analysis.filters import STOP_WORDS
from nltk.stem import WordNetLemmatizer

GOOGLE_STOP_WORDS = frozenset(('I', 'a', 'about', 'an', 'are', 'as', 'at', 'be', 'by', 'com', 'for', 'from',
                               'how', 'in', 'is', 'it', 'of', 'on', 'or', 'that', 'the', 'this', 'to', 'was',
                               'what', 'when', 'where', 'who', 'will', 'with', 'the',
                               'www')).union(STOP_WORDS)


# copy src/query/lemmatizer here
class WikiLemmatizer(Filter):

    def __call__(self, tokens):
        for token in tokens:
            token.text = WordNetLemmatizer().lemmatize(token.text)
            yield token


class WikiNormalizer(Filter):
    # rules = [
    #     (r'_', ''),
    #     (r'-', ''),
    # ]

    def __call__(self, tokens):
        filters = SubstitutionFilter("-", " ") \
                  | SubstitutionFilter('_', " ") \
                  # | SubstitutionFilter("'''''", "") \
                  # | SubstitutionFilter("'''", "") \
                  # | SubstitutionFilter("''", "")

        return filters(tokens)


def WikimediaAnalyzer():
    ret = StandardAnalyzer(stoplist=GOOGLE_STOP_WORDS)

    chain = ret | WikiNormalizer()

    return chain

def HighlightAnalyzer():
    ret = StandardAnalyzer(stoplist=None)
    return ret
