import math
from config import ASSETS_DATA, ROOT, N_PROC
from multiprocessing import Pool
import networkx as nx
import igraph


def normalize_title(title):
    return title.split('|')[0].lower().replace(" ", "_")

def normalize_graph(graph, N = 0.85):
    len_graph = len(graph)

    for key in graph:
        graph[key] = graph[key] * len_graph
    
    maxg = max([graph[key] for key in graph])

    for key in graph:
        graph[key] = graph[key] / maxg * N

    return graph

def proc_handler(data):
    tmp = ""
    articles = data.get("articles")
    chunk = data.get("chunk")

    for block in chunk:
        a_title = block.get("a_title")
        a_datum = block.get("a_datum")

        adj = [x for x in a_datum if x in articles]

        if len(adj):
            lin = a_title + " " + " ".join(adj)

            if not lin.endswith("\n"):
                lin = lin + "\n"

            tmp += lin
    
    return tmp

class Adjacency:
    def __init__(self):
        self.adjlist = {}
        self.articles = []
        self.__c_size = 0

    def load_from_index(self):
        with open(ASSETS_DATA / 'graphs' / 'graph.adjlist.tmp', "r") as file_in:
            for line in file_in:
                items = line.split(" ")
                article = items.pop(0)

                self.adjlist[article] = items
                self.articles = list(self.adjlist.keys())
                self.__c_size = math.ceil(len(self.articles) / N_PROC)

            file_in.close()

    def write_adjlist_clean(self):
        with Pool(N_PROC) as p:
            th_data = []

            for x in range(0, N_PROC):
                std = x * self.__c_size
                end = std + self.__c_size

                chunk = []

                for cnt in range(std, end):
                    if cnt >= len(self.articles):
                        break

                    a_title = self.articles[cnt]
                    a_datum = self.adjlist[a_title]

                    chunk.append(dict(a_title=a_title, a_datum=a_datum))

                th_data.append(dict(articles=self.articles, chunk=chunk))

            t_rd = p.map(proc_handler, th_data)
            f_ot = open(ASSETS_DATA / 'graphs' / 'graph.adjlist', "w")
            f_ot.write("".join(t_rd))
            f_ot.close()


class PageRank:
    def __init__(self, g=None):
        self.graph = {}
        self.G = g

    def clear(self):
        pass

    def load_adjlist(self):
        file_adjlist = ASSETS_DATA / 'graphs' / 'graph.adjlist'
        self.G = nx.read_adjlist(str(file_adjlist), create_using=nx.DiGraph)
        nx.write_graphml(self.G, ASSETS_DATA / 'graphs' / 'graph.graphml')

    def load_graphml(self): # leggi da adjlist per memoria
        file_graphml = ASSETS_DATA / 'graphs' / 'graph.graphml'
        self.G = igraph.Graph.Read_GraphML(str(file_graphml))

    def generate_rank(self):
        file_pagerank = ASSETS_DATA / 'graphs' / 'graph.igraph.rank'
        self.graph = self.G.pagerank()
        with open(str(file_pagerank), "w") as ff:
            for index in range(len(self.graph) - 1):
                article_title = self.G.vs[index]['id']
                ff.write(f'{article_title.rstrip()} {self.graph[index]}\n')
            ff.close()

    def get(self):
        file_pagerank = ASSETS_DATA / 'graphs' / 'graph.igraph.rank'
        graph_temp = {}

        with open(str(file_pagerank), "r") as ff:
            for line in ff:
                article, rank = tuple(line.split(" "))
                graph_temp[article] = float((rank.rstrip()))
            ff.close()

        self.graph = normalize_graph(graph_temp)

        return self.graph
