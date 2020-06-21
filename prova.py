from multiprocessing import Pool
import math

def handler(data):
    tmp = ""
    articles = data.get("articles")
    chunk = data.get("chunk")

    for count, block in enumerate(chunk):
        print(count, len(chunk))

        a_title = block.get("a_title")
        a_datum = block.get("a_datum")

        adj = [x for x in a_datum if x in articles]

        if len(adj):
            lin = a_title + " " + " ".join(adj)

            if not lin.endswith("\n"):
                lin = lin + "\n"

            tmp += lin
    
    print(' ? done')

    return tmp

if __name__ == '__main__':
    adjlist = {}

    file_in = open("__assets/graphs/graph.adjlist.txt", "r")

    print(' + read file')

    for line in file_in:
        items = line.split(" ")
        article = items.pop(0)
        adjlist[article] = items

    print(' - read file')

    file_in.close()

    articles = list(adjlist.keys())
    size = math.ceil(len(articles) / 4)

    with Pool(4) as p:
        th_data = []

        print(' + pool size')

        for x in range(0, 4):
            std = x * size
            end = std + size

            chunk = []

            for cnt in range(std, end):
                if cnt >= len(articles):
                    break

                a_title = articles[cnt]
                a_datum = adjlist[a_title]

                chunk.append(dict(a_title=a_title, a_datum=a_datum))

            th_data.append(dict(articles=articles, chunk=chunk))

        print(' - pool size')

        t_rd = p.map(handler, th_data)
        f_ot = open("__assets/graphs/graph.adjlist", "w")
        f_ot.write("".join(t_rd))
        f_ot.close()
