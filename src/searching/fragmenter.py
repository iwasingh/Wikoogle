from nltk import word_tokenize
import nltk
from nltk.tokenize import WhitespaceTokenizer
from whoosh.analysis import StandardAnalyzer
import re
from collections import OrderedDict


# In [2]: tokenizer =

class Phrase:
    def __init__(self, text, index, start, end):
        self._text = text
        self.start = start
        self.end = end
        self.index = index
        self.matches = []

    def __repr__(self):
        return self._text[self.start:self.end] + '...' + f'[{self.start} {self.end}]'

    def __hash__(self):
        return hash(f'{self.start}{self.end}')

    def add_match(self, token):
        self.matches.append(token)


class PhraseTokenizer:
    def __init__(self):
        self._tokenizer = self._tokenizer = nltk.tokenize.punkt.PunktSentenceTokenizer()

    def tokenize(self, text):
        phrases = []
        counter = 0
        for index, phrase in enumerate(self._tokenizer.tokenize(text)):
            start = counter
            end = start + len(phrase) - 1
            phrases.append(Phrase(text, index, start, end))
            counter = end + 1

        return phrases


class Fragment:
    def __init__(self, matches, phrase):
        self._matches = matches
        self._phrase = phrase


class Fragmenter:
    def __init__(self, max_size=150, ):
        self._tokenizer = PhraseTokenizer()

    # def _filter_matches(self, phrases, terms):
    #     for phrase in phrases:
    #         all(term in phrase.matches for term in terms)

    def frag(self, text, terms):
        regex = re.compile(r'|'.join(terms))
        phrases = self._tokenizer.tokenize(text)
        for token in regex.finditer(text.lower()):
            start = token.start()
            end = token.end()
            for phrase in phrases:
                if phrase.start <= start <= end <= phrase.end:
                    phrase.add_match(token)

        for phrase in phrases:
            for term in terms:
                if term not in phrase.matches:
                    break

        # selected = sorted(filter(lambda p: len(p.matches) > 0, phrases), key=lambda p: p.index)
        # for i in selected:
        #     print(i, '\n', '__MATCHES__', i.matches, '\n___')
