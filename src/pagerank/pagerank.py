import math

def normalize_title(title):
    return title.split('|')[0].lower().replace(" ", "_")

class PageRank:
    def __init__(self):
        self.graph = {}

    def clear(self):
        pass

    def get(self, name='graph.txt', destructive=False):
        f = open(name, "r")
        
        for line in f:
            articles = line.split(" ")
            main_article = articles.pop(0)
            self.graph[main_article] = math.log10(len(articles))

        f.close()

        max_values = max(self.graph.items(), key=lambda item: item[1])[1]
        
        for key in self.graph:
            self.graph[key] = self.graph[key]/max_values
        
        return self
