from whoosh.analysis import StandardAnalyzer, RegexAnalyzer, KeywordAnalyzer, SimpleAnalyzer, LowercaseFilter
from whoosh import highlight


def StandardScorer(fragment):
    analyzer = StandardAnalyzer()
    paragraph = fragment.text[fragment.startchar:fragment.endchar]
    tokens = [token.text for token in analyzer(paragraph)]
    print("_______________________________________\n", paragraph, '\n')


class Result:
    def __init__(self, result, query):
        self._value = result
        self._query = query

    @property
    def value(self):
        return self._value

    def snippet(self):
        title = self._value["title"]
        text = self._value["text"]

        analyzer = StandardAnalyzer(stoplist=None)

        def matched(token):
            token.matched = token.text.startswith(self._query)
            return token

        # tokens = map(matched, analyzer(text, chars=True, mode='query', removestops=False))

        # tokens = highlight.set_matched_filter(tokens, frozenset(self._query))

        # result = highlight.SentenceFragmenter().fragment_tokens(text, tokens)
        # for i in result:
        #     print('___', i.text[i.startchar:i.endchar])

        # breakpoint()
        # tokens = [i for i in result]

        # highlight.Highlighter(fragmenter=highlight.SentenceFragmenter, scorer=StandardScorer)
        # d = frozenset(self._query)
        # breakpoint()
        text = highlight.highlight(
            text,
            self._query,
            analyzer,
            highlight.ContextFragmenter(maxchars=150, surround=10, charlimit=150*10),
            highlight.HtmlFormatter(),
            top=1,
            scorer=StandardScorer
        )

        return dict(title=title, text=text)
