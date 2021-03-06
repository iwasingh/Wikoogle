from nltk.tokenize.treebank import TreebankWordDetokenizer
from nltk.tokenize.punkt import PunktSentenceTokenizer
from nltk import word_tokenize
from nltk.stem.porter import *
import re
from parsing.symbols import Bold, Italic, ItalicAndBold, Heading3, Heading4, Heading
from preprocessing.utils import clean
from markupsafe import Markup, escape
import time

stemmer = PorterStemmer()
detokenizer = TreebankWordDetokenizer()


# def clean(text):
#     tags = [
#         Bold,
#         ItalicAndBold,
#         Italic,
#         Heading3,
#         Heading4,
#         Heading,
#         Tab
#     ]
#
#     for i in tags:
#         text = re.sub(i.start.regex, "", text)
#
#     text = re.sub(r'<ref[\s\S]*?\/\>(!?<\/ref\>)*|<ref[\s\S]*?\>*?[<]?\/ref\>', "", text)
#
#     return text


def truncate(text, size):
    maximum_size = size + 100
    truncated_text = text[:size]
    last_char = truncated_text[-1]
    while not last_char.isspace() \
            and last_char not in {'!', '.', '?'} \
            and len(truncated_text) <= maximum_size \
            and len(truncated_text) < len(text):
        truncated_text += text[len(truncated_text)]
        last_char = truncated_text[-1]

    ellips = '...' if last_char.isspace() else ''

    return truncated_text + ellips


class Term:
    def __init__(self, start, end):
        self.start = start
        self.end = end


class Phrase:
    def __init__(self, phrase, index):
        self.index = index
        self.matches = []
        self.score = 0
        self.text = phrase
        self.tokens = [stemmer.stem(i) for i in word_tokenize(self.text)]

    def __repr__(self):
        return self.text + ' ' + f'[{self.score}]' + '\n'

    def __hash__(self):
        return hash(f'{self.text}')

    def add_match(self, token):
        self.matches.append(token)


class PhraseTokenizer:
    def __init__(self):
        self._tokenizer = self._tokenizer = PunktSentenceTokenizer()

    def tokenize(self, text):
        tokens = self._tokenizer.tokenize(text)
        return [Phrase(phrase, index) for index, phrase in enumerate(tokens)]
        # for index, phrase in enumerate(tokens):
        #     phrases.append(Phrase(phrase, index))

        # return phrases


class Fragment:
    def __init__(self, matches, phrase):
        self._matches = matches
        self._phrase = phrase


class Hit:
    def __init__(self, term, score, matched_token):
        self._term = term
        self._score = score
        self._matched_token = matched_token

    @property
    def term(self):
        return self._term

    @property
    def token(self):
        return self._matched_token

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
            if t in self._aliases or t == self._term:
                matches.append(Hit(self._term, 1, t))

        return matches

    def __eq__(self, term):
        return term in self._aliases or term == self._term


class Fragmenter:
    """
    :param max_size: max window size, google goes from min=150 to 200-250

    TODO caching
    """

    def __init__(self, max_size=300, top=2, threshold=0.25):
        self._tokenizer = PhraseTokenizer()
        self._stemmer = PorterStemmer()
        self._threshold = threshold
        self._top = top
        self._max_size = max_size

    def merge_fragments(self, fragments):
        text = ''
        matches = []
        sorted_fragments = sorted(fragments, key=lambda p: p.index)
        for phrase in sorted_fragments:
            text += phrase.text
            matches.extend(phrase.matches)
        # text = truncate(text, self._max_size)
        merged = Phrase(text, sorted_fragments[0].index)
        merged.score = sorted_fragments[0].score
        merged.matches = matches
        return merged

    def top_fragments(self, phrases):
        sorted_fragments = sorted(filter(lambda p: len(p.matches) > 0 and p.score > 0, phrases), key=lambda p: p.score,
                                  reverse=True)

        if len(sorted_fragments) == 0:
            return phrases[0]

        top_fragments = sorted_fragments[:self._top]
        top_fragment = top_fragments[0]
        best_fragments = []
        for t in top_fragments:
            epsilon = abs(top_fragment.score - t.score)
            if epsilon <= self._threshold:
                best_fragments.append(t)

        return self.merge_fragments(best_fragments)

    def calculate_phrase_ranking(self, text, terms):
        text = clean(text)
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

            phrase.score = ((d ** 2) / nqterms) + (l * (d / nqterms))

        return phrases

    def frag(self, text, terms):
        phrases = self.calculate_phrase_ranking(text, terms)
        best_fragment = self.top_fragments(phrases)
        return best_fragment

    @staticmethod
    def highlight(phrase, max_size=300):
        # template = '<%(tag)s class=%(q)s%(cls)s%(tn)s%(q)s>%(t)s</%(tag)s>'
        output = []
        highlight_terms = set(map(lambda hit: hit.term, phrase.matches))
        text = word_tokenize(escape(truncate(phrase.text, max_size)))
        for term in text:
            if stemmer.stem(term).lower() in highlight_terms:
                term = f'<strong>{term}</strong>'

            output.append(term)

        return detokenizer.detokenize(output)
