import unittest
import logging
from pathlib import Path
from searching.searcher import Searcher
from preprocessing.index import WikiIndex
from searching.fragmenter import Fragmenter
from parsing.compiler import Compiler
logging.basicConfig(level=logging.INFO)

DATA_FOLDER = Path(__file__).parent / 'data'


class TestSearcher(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestSearcher, self).__init__(*args, **kwargs)
        self.index = WikiIndex().get('__index')
        self.searcher = Searcher(self.index)

    def test_snippet(self):
        results = self.searcher.search('anarkhia')
        results[0].snippet()

    def test_fragmenter(self):
        text = """Anarchism is an [[Anti-authoritarianism|anti-authoritarian]] [[Political philosophy|political]] and 
        [[Social philosophy|social philosophy]]{{sfn|Flint|2009|p=27}} that rejects [[Hierarchy|hierarchies]] as 
        unjust and advocates their replacement with [[Workers' self-management|self-managed]], 
        [[Self-governance|self-governed]] societies based on voluntary, [[cooperative]] institutions. These 
        institutions are often described as [[Stateless society|stateless societies]],
        {{sfnm|1a1=Sheehan|1y=2003|1p=85|2a1=Craig|2y=2005|2p=14}} although several authors have defined them more 
        specifically as distinct institutions based on non-hierarchical or [[Free association (communism and 
        anarchism)|free associations]].{{sfn|Suissa|2006|p=7}} Anarchism's central disagreement with other ideologies 
        is that it holds the [[Sovereign state|state]] to be undesirable, unnecessary, and harmful.{{
        sfnm|1a1=McLean|1a2=McMillan|1y=2003|loc=Anarchism|2a1=Craig|2y=2005|2p=14}} Anarchism is usually placed on 
        the [[Far-left politics|far-left]] of the [[political spectrum]],
        {{sfnm|1a1=Brooks|1y=1994|1p=xi|2a1=Kahn|2y=2000|3a1=Moynihan|3y=2007}} and much of its [[Anarchist 
        economics|economics]] and [[Anarchist law|legal philosophy]] reflect [[Libertarian 
        socialism|anti-authoritarian interpretations]] of [[Anarcho-communism|communism]], [[Collectivist 
        anarchism|collectivism]], [[Anarcho-syndicalism|syndicalism]], [[Mutualism (economic theory)|mutualism]], 
        or [[participatory economics]].{{sfn|Guerin|1970|p=35|loc=Critique of authoritarian socialism}} As anarchism 
        does not offer a fixed body of doctrine from a single particular worldview,{{sfn|Marshall|1993|pp=14–17}} 
        many [[History of anarchism|anarchist types and traditions]] exist and varieties of anarchy diverge widely.{{
        sfn|Sylvan|2007|p=262}} [[Anarchist schools of thought]] can differ fundamentally, supporting anything from 
        extreme [[individualism]] to complete [[collectivism]].{{sfn|McLean|McMillan|2003|loc=Anarchism}} Strains of 
        anarchism have often been divided into the categories of [[Social anarchism|social]] and [[individualist 
        anarchism]], or similar dual classifications.{{
        sfnm|1a1=Fowler|1y=1972|2a1=Kropotkin|2y=2002|2p=5|3a1=Ostergaard|3y=2009|3p=14|3loc=Anarchism}} """
        f = Fragmenter()
        result = Compiler().compile(text)
        f.frag(result, ['anarchism'])


if __name__ == '__main__':
    unittest.main()
