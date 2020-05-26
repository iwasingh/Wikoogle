from nltk import word_tokenize
import nltk
from nltk.tokenize import WhitespaceTokenizer
from whoosh.analysis import StandardAnalyzer
import re
from collections import OrderedDict
from preprocessing.analyzer import FragmenterAnalyzer
from nltk.stem.porter import *
import re
from statistics import stdev

# In [2]: tokenizer =

# phrase_analyzer = FragmenterAnalyzer()

stemmer = PorterStemmer()


class Phrase:
    def __init__(self, text, phrase, index):
        self.index = index
        self.matches = []
        self.score = 0

        self.phrase = phrase
        self.tokens = [stemmer.stem(i) for i in word_tokenize(self.phrase)]
        # self.phrase = [i.text for i in phrase_analyzer(text)]

    def __repr__(self):
        return self.phrase + ' ' + f'[{self.score}]' + '\n'

    def __hash__(self):
        return hash(f'{self.phrase}')

    def add_match(self, token):
        self.matches.append(token)


class PhraseTokenizer:
    def __init__(self):
        self._tokenizer = self._tokenizer = nltk.tokenize.punkt.PunktSentenceTokenizer()

    def tokenize(self, text):
        phrases = []
        counter = 0
        for index, phrase in enumerate(self._tokenizer.tokenize(text)):
            print(phrase)
            start = counter
            end = start + len(phrase) - 1
            phrases.append(Phrase(text, phrase, index))
            counter = end + 1

        return phrases


class Fragment:
    def __init__(self, matches, phrase):
        self._matches = matches
        self._phrase = phrase


class Hit:
    def __init__(self, term, score):
        self._term = term
        self._score = score

    @property
    def term(self):
        return self._term

    def __repr__(self):
        return self._term + '[' + str(self._score) + ']'


class QueryTerm:
    def __init__(self, term, aliases):
        self._term = term
        self._aliases = aliases
        self._regex = re.compile('|'.join([term] + aliases))

    def match(self, phrase):
        matches = []
        for t in phrase.tokens:
            # if t == self._term:
            #     matches.append(Hit(self._term, 1))
            #
            # elif t in self._aliases:
            if t in self._aliases or t == self._term:
                matches.append(Hit(self._term, 1))

        return matches

    def __eq__(self, term):
        return term in self._aliases or term == self._term


class Fragmenter:
    """
    :param max_size: max window size, google goes from min=150 to 200-250

    """

    def __init__(self, max_size=200, top=3):
        self._tokenizer = PhraseTokenizer()
        self._stemmer = PorterStemmer()
        self._threshold = 0.25
        self._top = 2
        self._max_size = max_size

    def merge_fragments(self, fragments):
        # for i in sorted(fragments, key=lambda p: p.index):
        return fragments

    def top_fragments(self, phrases):
        sorted_fragments = sorted(filter(lambda p: len(p.matches) > 0 and p.score > 0, phrases), key=lambda p: p.score,
                                  reverse=True)

        if len(sorted_fragments) == 0:
            return [phrases[0]]

        top_fragments = sorted_fragments[:self._top]
        top_fragment = top_fragments[0]
        best_fragments = []
        for t in top_fragments:
            epsilon = top_fragment.score - t.score
            if epsilon <= self._threshold:
                best_fragments.append(t)

        return self.merge_fragments(best_fragments)

    def frag(self, text, terms):
        query_terms = list(map(lambda t: QueryTerm(t, [self._stemmer.stem(t)]), list(set(terms))))
        phrases = self._tokenizer.tokenize(text)
        nqterms = len(terms)
        for phrase in phrases:
            for qterm in query_terms:
                matches = qterm.match(phrase)
                if len(matches) > 0:
                    phrase.matches.extend(matches)

        for index, phrase in enumerate(phrases):
            # 1 if heading 0 otherwise
            h = 0
            # if first line, 1 if second line, 0 otherwise
            l = (2 - index) if index <= 1 else 0
            # number of query terms in phrase, counting repetitions
            c = len(phrase.matches)
            # number of distinct query terms in phrase
            d = 0
            for m in set([i.term for i in phrase.matches]):
                for qterm in query_terms:
                    if qterm == m:
                        d = d + 1

            # TODO k = longest run of query terms in phrase, let's say from wj ... wj+k

            phrase.score = ((d ** 2) / nqterms) + (l * (d/nqterms))

        print('\n\n\n\n', phrases, '\n\n\n')
        for i in self.top_fragments(phrases):
            print(i, 'score', '[', i.score, ']', '\n', '__MATCHES__', i.matches, '\n___')

    def highlight(self, phrase, terms):
        pass
        
