from nltk import pos_tag
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer, PorterStemmer
from preprocessing.analyzer import WikimediaAnalyzer
from enum import Enum


class POSTag(Enum):
    J = wordnet.ADJ
    V = wordnet.VERB
    N = wordnet.NOUN
    A = wordnet.ADV

    # ALL = 'ALL'

    @classmethod
    def to_wordnet(cls, nltk_pos):
        for pos in cls:
            if nltk_pos.startswith(pos.name):
                return pos
        return cls.N  # TODO check. Not founded tag are threatened as nouns. Maybe None?


def lemmatizer(tokens):
    w_lemmatizer = WordNetLemmatizer()
    return [w_lemmatizer.lemmatize(token, POSTag.to_wordnet(pos).value) for (token, pos) in pos_tag(tokens)]


def extract(tokens, tags=None):
    if tags is None:
        tags = [POSTag.J, POSTag.N]

    t = [token for token in pos_tag(tokens) if POSTag.to_wordnet(token[1][0]) in tags]

    return list(filter(None, t))


def stemming(tokens):
    stemmer = PorterStemmer()
    return [stemmer.stem(t) for t in tokens]


def expand(query):
    """
    Wordent hierarchy
     - hyponyms concepts that are more specific (immediate), navigate down to the tree
     - hypernyms general concept, navigate up the hierarchy
     - meronyms components. For instance a tree have trunk, ...so on as meronym
     - holonyms things that contain meronyms (i.e. tree)

     Query expansion require good relevance feedback methods. Using a thesaurus based query expansion might decrease
     performance and has query drift problems with polysemic words. For now query expansion
     for now only stems and lemmas of non-polysemic words are expanded
    :param query:
    :return:
    """
    analyzer = WikimediaAnalyzer()
    original_tokens = [i.text for i in analyzer(query)]
    tokens = stemming(original_tokens)
    synonyms = set()
    for token in original_tokens:
        senses = wordnet.synsets(token, 'n')
        if len(senses) == 1:
            synonyms = synonyms.union(set(senses[0].lemma_names()))

    tokens += [i.text for i in analyzer(' '.join(list(synonyms)))]
    return original_tokens + [i for i in tokens if i not in original_tokens]