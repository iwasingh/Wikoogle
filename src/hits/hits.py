from config import ASSETS_DATA
from pagerank.pagerank import normalize_title, normalize_graph
import networkx as nx
import igraph

class Hits:
    def __init__(self):
        self.G = None

    def load_graphml(self):
        file_graphml = ASSETS_DATA / 'graphs' / 'graph.graphml'
        self.G = igraph.Graph.Read_GraphML(str(file_graphml))

    def rank_from_results(self, results):
        ne_graph_ids = []
        search_set = [r.get("title") for r in results]

        for t in search_set:
            try:
                v = self.G.vs.find(id=normalize_title(t))

                for n in v.neighbors():
                    if n.index not in ne_graph_ids:
                        ne_graph_ids.append(n.index)

                if v.index not in ne_graph_ids:
                    ne_graph_ids.append(v.index)
            except:
                pass

        subV = self.G.vs.select(ne_graph_ids)
        subG = self.G.subgraph(subV)

        nodes = {}

        for v in subG.vs:
            nodes[v.index] = v["id"]

        edges = [(nodes[x[0]], nodes[x[1]]) for x in subG.get_edgelist()]

        nxGraph = nx.DiGraph()

        nxGraph.add_nodes_from([nodes[x] for x in nodes])
        nxGraph.add_edges_from(edges)

        auth = normalize_graph(nx.hits(nxGraph)[1])
        hubs = normalize_graph(nx.hits(nxGraph)[0])

        return (auth, hubs)
        
