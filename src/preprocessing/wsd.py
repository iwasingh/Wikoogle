from nltk.corpus import wordnet


def maximum_similarity(w1, w2, threshold=0):
    arr = []
    for s1 in wordnet.synsets(w1):
        for s2 in wordnet.synsets(w2):
            arr.append((s1, s2, s1.wup_similarity(s2) or 0))
    filtered = list(filter(lambda t: t[2] >= threshold, arr))
    return max(filtered, key=lambda t: t[2], default=('', '', 0))


def resnik_wsd(tokens, threshold=0.8):
    """https://arxiv.org/pdf/1105.5444.pdf"""
    """
    For each pair the algorithm goes through all possible combinations of
    the words' senses, and assigns \credit" to senses on the basis of shared information content,
    as measured using the wu_palmer similarity of the most informative subsumer.

    TODO: optimize with numpy
    """
    length = len(tokens)
    i = 0
    v = [[0.0 for i in range(len(tokens))] for j in range(len(tokens))]
    c = [[(None, 0.0) for i in range(len(tokens))] for j in range(len(tokens))]

    support = {}
    normalization = [0 for i in range(len(tokens))]
    while i < length:
        j = i + 1
        while j < length:
            wi = tokens[i]
            wj = tokens[j]
            s1, s2, score = maximum_similarity(wi, wj, 0)
            if score == 0:
                i = i + 1
                j = j + 1
                continue
            v[i][j] = score
            c[i][j] = (s1.lowest_common_hypernyms(s2)[0], score)

            def count_synset(synsets):
                for k in synsets:
                    possible_hypernyms = list(filter(lambda s: s == c[i][j][0], k.lowest_common_hypernyms(c[i][j][0])))
                    if possible_hypernyms:
                        value = support.get(k.name(), 0)
                        support[k.name()] = value + v[i][j]

            if c:
                count_synset(wordnet.synsets(wi))
                count_synset(wordnet.synsets(wj))

            normalization[i] += v[i][j]
            normalization[j] += v[i][j]
            j += 1
        i += 1

    p = {}
    for i in range(length):
        senses = wordnet.synsets(tokens[i])
        p[tokens[i]] = []
        for z in range(len(senses)):
            if normalization[i] > 0 and support.get(senses[z].name(), 0) != 0:
                value = support.get(senses[z].name()) / normalization[i]
                if value >= threshold:
                    p[tokens[i]].append((senses[z], support.get(senses[z].name()) / normalization[i]))
            else:
                value = 1 / len(senses)
                if value >= threshold:
                    p[tokens[i]].append((senses[z], value))

    common_senses = []
    for i in c:
        result = max(i, key=lambda t: t[1])
        if result and result[0]:
            common_senses.append(result)

    return p, common_senses
