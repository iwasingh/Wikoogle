import unittest
import logging
from pathlib import Path
from pagerank.pagerank import PageRank
from config import ASSETS_DATA
import networkx as nx

logging.basicConfig(level=logging.INFO)

DATA_FOLDER = Path(__file__).parent / 'data'
ASSETS_GRAPH_FOLDER = ASSETS_DATA / 'graphs'


class TestPageRank(unittest.TestCase):

    def test_generate_adjlist(self, name='graph.txt'):
        p = PageRank()
        p.generate_adjlist(path=DATA_FOLDER / name)

    def test_pagerank(self):
        p = PageRank.from_adjlist(path=ASSETS_GRAPH_FOLDER / 'graph.graphml')
        pr = p.generate_page_rank(path=ASSETS_GRAPH_FOLDER / 'graph.networkx.rank')
        # TODO assert file exists and not empty

    def test_graph(self):
        PR = PageRank.from_adjlist(path=ASSETS_GRAPH_FOLDER / 'graph.adjlist')
        # PR.G.number_of_nodes() > 0

    def test_igraph_pagerank(self):
        p = PageRank.from_igraph_graphml(path=ASSETS_GRAPH_FOLDER / 'graph.graphml')
        pr = p.generate_igraph_page_rank(path=ASSETS_GRAPH_FOLDER / 'graph.igraph.rank')


if __name__ == '__main__':
    unittest.main()
