#nxg_citation = nx.DiGraph()
#nxg_citation = make_graph_("citation.txt", nxg_citation, "\t")
#print("yes")
#nx.draw_networkx(nxg_citation, pos = nx.spring_layout(nxg_citation))
#plt.title("Example Citations Graph")
#plt.show()

#g_twitter = Graph(81306)
#print_stats("twitter.txt", g_twitter, " ")

import matplotlib.pyplot as plt
import networkx as nx

def new_graph(nxg, i):
    new_elist = []
    components = nx.strongly_connected_components(nxg)
    new_ngx = nx.DiGraph()
    for comp in components:
        if len(comp) == 1:
            new_ngx.add_node(list(comp)[0])
        else:
            for e in elist:
                if e[0] in comp and e[1] in comp:
                    new_elist.append(e)
    new_ngx.add_edges_from(new_elist)
    nx.draw_networkx(new_ngx, pos = nx.spring_layout(nxg, threshold=1e-5), node_size=2000)
    plt.title("Example Graph " + str(i))
    plt.show()
nxg1 = nx.DiGraph()
elist = [(1, 0), (0, 2), (2, 1), (0, 3), (3, 4)]
nxg1.add_edges_from(elist)
new_graph(nxg1, 1)
nx.draw_networkx(nxg1, pos = nx.spring_layout(nxg1), node_size=2000)
plt.title("Example Graph 1")
plt.show()
nxg2 = nx.DiGraph()
elist = [(0, 1), (1, 2), (2, 3)]
nxg2.add_edges_from(elist)
new_graph(nxg2, 2)

nx.draw_networkx(nxg2, pos = nx.spring_layout(nxg2), node_size=2000)
plt.title("Example Graph 2")
plt.show()

nxg3 = nx.DiGraph()
elist = [(0, 1), (1, 2), (2, 0), (1, 3), (1, 4), (1, 6), (3, 5), (4, 5)]
nxg3.add_edges_from(elist)
new_graph(nxg3, 3)
nx.draw_networkx(nxg3, pos = nx.spring_layout(nxg3), node_size=2000)
plt.title("Example Graph 3")
plt.show()

nxg4 = nx.DiGraph()
elist = [(0, 1), (0, 3), (1, 2), (1, 4), (2, 0), (2, 6), (3, 2), (4, 5), (4, 6), (5, 6), (5, 7), (5, 8), (5, 9), (6, 4), (7, 9), (8, 9), (9, 8)]
nxg4.add_edges_from(elist)
new_graph(nxg4, 4)


nx.draw_networkx(nxg4, pos = nx.spring_layout(nxg4), node_size=2000)
plt.title("Example Graph 4")
plt.show()
nxg5 = nx.DiGraph()
elist = [(0, 1), (1, 2), (2, 3), (2, 4), (3, 0), (4, 2)]
nxg5.add_edges_from(elist)
new_graph(nxg5, 5)

nx.draw_networkx(nxg5, pos = nx.spring_layout(nxg5), node_size=2000)
plt.title("Example Graph 5")
plt.show()
