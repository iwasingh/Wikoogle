from whoosh.analysis import StemmingAnalyzer
from whoosh.analysis.filters import Filter, SubstitutionFilter, CharsetFilter
from whoosh.analysis.filters import STOP_WORDS
from nltk.stem import WordNetLemmatizer
from whoosh.support.charset import accent_map

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


def WikimediaAnalyzer(stoplist=GOOGLE_STOP_WORDS, cachesize=50000):
    # Use different analyzer for the title
    ret = StemmingAnalyzer(stoplist=stoplist, cachesize=cachesize) | CharsetFilter(accent_map)
    chain = ret | WikiNormalizer()

    return chain


def FragmenterAnalyzer():
    ret = StemmingAnalyzer(minsize=0, stoplist=None)
    return ret
