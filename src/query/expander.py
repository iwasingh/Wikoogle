from nltk import pos_tag, word_tokenize, RegexpParser, ngrams, FreqDist
from nltk.collocations import BigramCollocationFinder
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer, PorterStemmer
from preprocessing.analyzer import ThesaurusExpansionAnalyzer, WikimediaAnalyzer
from preprocessing.utils import clean
from enum import Enum
from nltk.tree import Tree
from functools import reduce
import operator
from math import log
from whoosh.analysis import StemmingAnalyzer
from searching.fragmenter import Fragmenter, PhraseTokenizer
import re
import math
from pywsd import disambiguate, adapted_lesk
# from pke.unsupervised import TopicRank


def get_cosine(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x] ** 2 for x in vec1.keys()])
    sum2 = sum([vec2[x] ** 2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator


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


def pke_key_phrase_extract(text, n=10):
    # create a TopicRank extractor
    extractor = TopicRank()

    # load the content of the document, here in CoreNLP XML format
    # the input language is set to English (used for the stoplist)
    # normalization is set to stemming (computed with Porter's stemming algorithm)
    extractor.load_document(text,
                            language="en",
                            normalization='stemming')

    # select the keyphrase candidates, for TopicRank the longest sequences of
    # nouns and adjectives
    extractor.candidate_selection(pos={'NOUN', 'PROPN', 'ADJ'})

    # weight the candidates using a random walk. The threshold parameter sets the
    # minimum similarity for clustering, and the method parameter defines the
    # linkage method
    extractor.candidate_weighting(threshold=0.74,
                                  method='average')

    # print the n-highest (10) scored candidates
    return extractor.get_n_best(n=n, stemming=True)


def thesaurus_expand(query, wikimedia, size=3, threshold=4.23):
    """
    Wordent hierarchy
     - hyponyms concepts that are more specific (immediate), navigate down to the tree
     - hypernyms general concept, navigate up the hierarchy
     - meronyms components. For instance a tree have trunk, ...so on as meronym
     - holonyms things that contain meronyms (i.e. tree)

     Query expansion require good relevance feedback methods. Using a thesaurus based query expansion might decrease
     performance and has query drift problems with polysemic words. This method picks up keyword from gloss of the synsets
     and uses a lesk algorithm to disambiguate terms from each other
    :param query:
    :return:
    """
    analyzer = ThesaurusExpansionAnalyzer()
    wikimedia_analyzer = WikimediaAnalyzer()
    original_tokens = [i.text for i in analyzer(query)]
    # original_tokens = set([i.text for i in query.all_tokens()])
    print(original_tokens)

    synonyms = set()

    rule = r"""
           NBAR: {<NN>}
                 {<JJ>}
                 # {<JJS>}
                 {<NNS>}
                 # {<NNP>}
    """

    synsets = []
    # for i in original_tokens:
    #     for s in wordnet.synsets(i):
    #         for h in s.hypernyms():
    #             print(s, h , s.wup_similarity(h))

    # for i in original_tokens:
    #     for s in wordnet.synsets(i):
    #         print(s.definition())

    for w, s in disambiguate(" ".join(original_tokens), algorithm=adapted_lesk):
        if s:
            definition = s.definition()
            pke_text = definition + ' ' + ' '.join(s.lemma_names())
            # print(pke_key_phrase_extract(pke_text))
            tokens = [i.text for i in wikimedia_analyzer(definition)]
            synsets.append((w, wordnet.synset(s.name()), tokens))

    for word, sense, definition in synsets:
        if sense:
            synonyms = synonyms.union(noun_groups(word_tokenize(sense.definition()), chunk_size=1, rule=rule))
            text = " ".join([i.name() for i in sense.lemmas()])
            for lemma in wikimedia_analyzer(text):
                if lemma.text not in original_tokens:
                    synonyms.add(lemma.text)
                # vfor tok in wikimedia_analyzer(lemma.text):
                #     print(tok.text)
                #     if tok.text not in original_tokens:
                #         synonyms.add(tok.text)

    # for token in tokens: for _, original_sense, _ in synsets: for child_synset in wordnet.synsets(token):
    # if child_synset: # definition = [i.text for i in analyzer(child_synset.definition())] # pywsd. score =
    # wordnet.synset(original_sense.name()).path_similarity(child_synset, simulate_root=False) print(
    # child_synset, child_synset.definition(), original_sense, score)

    # print(tokens)
    # print([j.definition() for i, j in pywsd.disambiguate(query, algorithm=pywsd.simple_lesk)], '\n',
    #       [j.definition() for i, j in pywsd.disambiguate(query, algorithm=pywsd.adapted_lesk)], '\n',
    #       [j.definition() for i, j in pywsd.disambiguate(query, algorithm=pywsd.cosine_lesk)], '\n',
    #       [j.definition() for i, j in pywsd.disambiguate(query, algorithm=pywsd.max_similarity)])

    # if len(_concept) > 0:
    #     concept, similarity_strength = _concept[0]
    #     if similarity_strength > 0.7:
    #         __retrieve_definition_groupings(synsets)
    # else:
    #     print(__retrieve_definition_groupings(synsets))
    # disambiguated_senses = disambiguate(query, algorithm=adapted_lesk)

    # print(disambiguated_senses, '\n\n', simple_lesk, '\n\n', resnik_wsd(word_tokenize(query)), '\n')
    # for token in original_tokens:
    #     senses = wordnet.synsets(token, 'n')
    #     if len(senses) == 1:
    #         synonyms = synonyms.union(set(senses[0].lemma_names()))
    #     else:
    #
    # tokens += [i.text for i in analyzer(' '.join(list(synonyms)))]
    # return original_tokens + [i for i in tokens if i not in original_tokens]

    reader = wikimedia.reader

    terms_vec = {}
    for syn in synonyms:
        score = calc_syn_score(syn, reader)

        terms_vec[syn] = score
        # else:
        #     terms_vec[syn] = 0

    ranked_terms = sorted(terms_vec, key=lambda c: terms_vec[c], reverse=True)
    print('***Ranked terms')
    for i in list(map(lambda q: (q, terms_vec[q]), ranked_terms)):
        print(i[0], ' ', i[1], '\n')

    return list(map(lambda q: q[0], filter(lambda v: v[1] >= threshold, terms_vec.items())))


def calc_syn_score(syn, reader):
    terms_vec = []
    for i in word_tokenize(syn):
        doc_frequency = reader.doc_frequency('text', i)
        term_frequency = reader.frequency('text', i)
        if doc_frequency != 0:
            terms_vec.append(term_frequency / doc_frequency)
        else:
            terms_vec.append(0)

    return max(terms_vec)


def noun_groups(tokens, chunk_size=2, analyzer=StemmingAnalyzer(), rule=None):
    grammar = r"""
        NBAR: {<NN|JJ><|JJ|NN>} # Nouns and Adjectives, terminated with Nouns
              # {<NN>} # If pattern not found just a single NN is ok
    """
    if rule is not None:
        grammar = rule

    cp = RegexpParser(grammar)
    result = cp.parse(pos_tag(tokens))
    nouns = set()
    for chunk in result:
        if type(chunk) == Tree:
            if chunk.label() == 'NBAR':
                words = list(map(lambda entry: entry[0], chunk.leaves()))
                tokens = analyzer(" ".join(words))
                nouns.add(" ".join([i.text for i in tokens]))
                # nouns.add(tuple([i.text for i in tokens]))
        else:
            continue
            # print('Leaf', '\n', chunk)
    return nouns


class Passage:
    """ Deprecated """

    def __init__(self, doc, passage):
        self._doc = doc
        self._passage = passage

        self.concept = []

    def __repr__(self):
        return f'{self._passage[0:3]}...[{len(self._passage)}] [{self._doc["title"]}]'


class DocStats:
    """
     In-memory bigram index for text statistics
    """

    def __init__(self, tokens):
        self._bigram = BigramCollocationFinder.from_words(tokens)

    @staticmethod
    def _score_from_ngram(*args):
        return args[0]

    def _frequency(self, gram: tuple):
        fd_score = self._bigram.score_ngram(self._score_from_ngram, *gram) or 0
        bd_score = self._bigram.score_ngram(self._score_from_ngram, *gram[::-1]) or 0
        return max(fd_score, bd_score)

    def frequency(self, term: str):
        grams = [i for i in ngrams(term.split(" "), 2)]

        if len(grams) == 0: return self._bigram.word_fd[term]
        return max([self._frequency(gram) for gram in grams])


def __count_docs_containing(c, docs):
    docs_containing_c = list(filter(lambda f: f > 0, [d.frequency(c) for d in docs]))
    return len(docs_containing_c)


def prod(products):
    return reduce(operator.mul, products)


def _calculate_qterm_correlation(query_terms, concept, idf_c, docs):
    for qterm, idf_i in query_terms:
        N = len(docs)
        # IDFc = max(1.0, log(N / npc, 10) / 5)
        # IDFi = max(1.0, log(N / npi, 10) / 5)
        y = 0.1

        f = sum([doc_stat.frequency(qterm) * doc_stat.frequency(concept) for doc_stat in docs])

        if f == 0:
            yield y
        else:
            # print(f, N, y, idf_c, idf_i, concept, qterm)
            yield (y + (log(f) * idf_c) / log(N)) ** idf_i
            # yield d


def lca_expand(query, documents, size=15, passage_size=400, threshold=1.4):
    """
    Implements the Local Context Analysis algorithm to expand query based on top ranked concept that
    maximize the sim to the query

    sim(q,c) = ∏ (y + (log(f(ci,ki) + IDFc) / log(n))^IDFi
    where:
    * f(ci, ki) = quantifies the correlation between the concept c and the query term ki:
     and is given by: Σ pfi_j * pfc_j where pf(i,c)_j is the frequency of term ki or concept c in the j-th doc
    * IDFc = inverse document frequency of concept c calculated as max(1, log_10(N/npc)/5)
      IDFi = inverse document frequency of query term i calculated as max(1, log_10(N/npi)/5) to emphasizes infrequent query terms
      where npc is number of documents containing the concept c nad npi number of docs containing the query term i
      and N is number of documents
      IDFi
    * y is a smoothing constant set to 0.1 to avoid zeros values in the product calculation

    A concept is a noun group of single, two, or three words.
    """
    fragmenter = Fragmenter(max_size=passage_size)
    query_terms = set([i.text for i in query.all_tokens()])
    regex = re.compile(r"|".join(query_terms))
    analyzer = StemmingAnalyzer()
    concepts = set()
    doc_stats = []
    for doc in documents:
        text = clean(doc['text']).lower()
        fragment = fragmenter.merge_fragments(PhraseTokenizer().tokenize(text)[:3])
        # fragment = fragmenter.merge_fragments(
        #     fragmenter.calculate_phrase_ranking(
        #         text,
        #         query_terms)[:3])
        tokens = word_tokenize(fragment.text)
        stemmed_tokens = [i.text for i in analyzer(text)]
        key_terms = noun_groups(tokens)
        concepts = concepts.union(key_terms)
        doc_stats.append(DocStats(stemmed_tokens))

    query_terms_with_idf = list()

    for q in query_terms:
        npi = __count_docs_containing(q, doc_stats)
        if npi == 0:
            query_terms_with_idf.append((q, 1))
        else:
            query_terms_with_idf.append((q, log(len(documents) / npi, 10) / 5))

    concepts = set(filter(lambda c: len(c) > 2, concepts))  # Removing blank entries or spurious pos_tag entries
    # tagged as NN
    # breakpoint()
    ranking = []
    for concept in concepts:
        if concept in query_terms: continue
        N = len(documents)
        npc = __count_docs_containing(concept, doc_stats) or 1
        idf_c = max(1.0, log(N / npc, 10) / 5)
        prods = _calculate_qterm_correlation(query_terms_with_idf, concept, idf_c, doc_stats)
        sim = prod([i for i in prods])
        ranking.append((concept, sim))

    print(sorted(ranking, key=lambda c: c[1], reverse=True))
    filtered = filter(lambda c: c[1] > threshold, ranking)
    return list(map(lambda q: q[0], sorted(filtered, key=lambda c: c[1], reverse=True)))[:size]
    # return [re.sub(regex, "", term).strip() for term in top_terms]
