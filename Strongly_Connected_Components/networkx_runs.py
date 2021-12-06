import networkx as nx
from datetime import datetime
startTime = datetime.now()

def make_graph_(file_name, g, split_by):
    file = open(file_name, "r")
    elist = []
    for line in file:
        line_ = line.split(split_by)
        v1 = int(line_[0])
        v2 = int(line_[1])
        elist.append((v1, v2))
    g.add_edges_from(elist)
    file.close()
    return g
g_citation = nx.DiGraph()
#g_citation = make_graph_("citation.txt", g_citation, "\t")
print(datetime.now() - startTime)
check = nx.kosaraju_strongly_connected_components(g_citation)
print(datetime.now() - startTime)
print(datetime.now() - startTime)
check = nx.strongly_connected_components(g_citation)
print(datetime.now() - startTime)
#print(max(check))
g_twitter = nx.DiGraph()
#g_twitter = make_graph_("citation.txt", g_twitter, "\t")
g_twitter = nx.DiGraph()
g_twitter = make_graph_("twitter.txt", g_twitter, " ")
print(datetime.now() - startTime)
check = nx.kosaraju_strongly_connected_components(g_twitter)
print(datetime.now() - startTime)
print(datetime.now() - startTime)
check = nx.strongly_connected_components(g_twitter)
print(datetime.now() - startTime)
#print(max(check))
#for c in check:
	#sorted(check, key=len, reverse=True):
	#print(len(c))