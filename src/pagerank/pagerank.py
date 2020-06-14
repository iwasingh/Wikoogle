import math
from config import ASSETS_DATA, ROOT
import networkx as nx
import igraph


def normalize_title(title):
    return title.split('|')[0].lower().replace(" ", "_")


class PageRank:
    def __init__(self, graph):
        self.graph = {}
        self.G = graph

    def clear(self):
        pass

    def generate_adjlist(self, path, dump=ROOT / 'src' / 'graph.txt', extensions=None):

        self.G = nx.DiGraph()

        f = open(str(dump), "r", encoding='utf-8')
        for line in f:
            articles = line.split(" ")
            main_article = articles.pop(0)
            self.G.add_edges_from([(article, main_article) for article in articles])

        f.close()
        nx.write_adjlist(self.G, str(path) + '.adjlist')
        nx.write_graphml(self.G, str(path) + '.graphml')

    @staticmethod
    def from_adjlist(path):
        G = nx.read_adjlist(str(path), create_using=nx.DiGraph)
        # nx.write_graphml(G, str(path))
        return PageRank(G)

    @staticmethod
    def from_graphml(path):
        G = nx.read_graphml(str(path))
        return PageRank(G)

    @staticmethod
    def from_igraph_graphml(path):
        G = igraph.Graph.Read_GraphML(str(path))
        return PageRank(G)

    # def __write_rank(self, pr, path):
    #     f = open(str(path), 'w', encoding="utf-8")
    #     for article_title in pr:
    #         f.write(f'{article_title} {pr[article_title]}\n')
    #     f.close()
    #     return pr

    def generate_page_rank(self, path):
        pr = nx.pagerank_numpy(self.G, alpha=0.85)
        f = open(str(path), 'w', encoding="utf-8")
        for article_title in pr:
            f.write(f'{article_title} {pr[article_title]}\n')
        f.close()
        return pr

    def generate_igraph_page_rank(self, path):
        pr = self.G.pagerank()
        f = open(str(path), 'w', encoding="utf-8")
        for index in range(len(pr) - 1):
            article_title = self.G.vs[index]['id']
            f.write(f'{article_title} {pr[index]}\n')
        f.close()
        return pr

    def get(self, name='graph.txt', destructive=False):
        f = open(name, "r")

        for line in f:
            articles = line.split(" ")
            main_article = articles.pop(0)
            self.graph[main_article] = math.log10(len(articles))

        f.close()

        max_values = max(self.graph.items(), key=lambda item: item[1])[1]

        for key in self.graph:
            self.graph[key] = self.graph[key] / max_values

        return self
