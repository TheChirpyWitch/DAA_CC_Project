from collections import defaultdict
import sys
import matplotlib.pyplot as plt
import networkx as nx
from datetime import datetime
startTime = datetime.now()
sys.setrecursionlimit(30000)

class Graph:

	def __init__(self,vertices):
		self.V= vertices
		self.graph = defaultdict(list)
		#defaultdict(lambda: defaultdict(int)) or defaultdict(lambda: defaultdict(dict))
		self.Time = 0
		self.disc = {}
		self.low = {}
		self.stackMember = {}
		self.max_scc = []
		self.condensed_nodes_roots = []

	def addEdge(self, u, v):
		self.graph[u].append(v)
		if u not in self.disc:
			self.disc[u] = -1
		if u not in self.low:
			self.low[u] = -1
		if v not in self.disc:
			self.disc[v] = -1
		if v not in self.low:
			self.low[v] = -1

	def SCCUtil(self,u, low, disc, stackMember, st, output_file):
		disc[u] = self.Time
		low[u] = self.Time
		self.Time += 1
		stackMember[u] = True
		st.append(u)
		for v in self.graph[u]:
			if disc[v] == -1:			
				self.SCCUtil(v, low, disc, stackMember, st, output_file)
				low[u] = min(low[u], low[v])						
			elif stackMember[v] == True:
				low[u] = min(low[u], disc[v])
		w = -1
		
		ofile = open(output_file, "a")
		"""
		ofile.write("Start on " + u + "\n")
		ofile.write(u + " " + str(low[u]) + "\n")
		for v in self.graph[u]:
			ofile.write(v + " " + str(low[v]) + "\n")
		ofile.write("Finish " + u + "\n")
		ofile.write(u + " " + str(disc[u]) + "\n")
		for v in self.graph[u]:
			ofile.write(v + " " + str(disc[v]) + "\n")
		"""
		if low[u] == disc[u]:
			scc = []
			while w != u:
				w = st.pop()
				scc.append(w)
				stackMember[w] = False	
			ofile.write(str(scc) + "\n")
			if len(scc) > len(self.max_scc):
				self.max_scc = scc
			self.condensed_nodes_roots.append(scc[0])
			
	def printSCCs(self, output_file):
		st =[]
		for i in self.disc:
			if self.disc[i] == -1:
				self.SCCUtil(i, self.low, self.disc, self.stackMember, st, output_file)

def make_graph(file_name, g, split_by):
    file = open(file_name, "r")
    for line in file:
        line_ = line.split(split_by)
        v1 = int(line_[0])
        v2 = int(line_[1])
        g.addEdge(v1, v2)
    file.close()
    return g

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

def edges_associated(g):
    n = 0
    elist = []
    for node in g.max_scc:
        for e2 in g.graph[node]:
            if e2 in g.max_scc:
            	elist.append([node, e2])
            	n += 1
    return n, elist

def print_stats(file_name, g, split_by):
    g = make_graph(file_name, g, split_by)
    file = file_name[:-4] + "_SCCs_tarjan.txt"
    print(datetime.now() - startTime)
    g.printSCCs(file)
    print(datetime.now() - startTime)
    n_e, elist = edges_associated(g)
    print("SSC Stats in " + file_name[:-4] + " graph ")
    print("Number of nodes in largest SCC: " + str(len(g.max_scc)))
    print("Number of edges in largest SCC: " + str(n_e))
    write_file_name = file_name[:-4] + "_SCC_edgelist_tarjan_.csv"
    write_file = open(write_file_name, "w+")
    for el in elist:
        c = str(el[0]) + " " + str(el[1]) + "\n"
        write_file.write(c)

#g_citation = Graph(27770)
#print_stats("citation.txt", g_citation, "\t")
#nxg_citation = nx.DiGraph()
#nxg_citation = make_graph_("citation.txt", nxg_citation, "\t")
#print("yes")
#nx.draw_networkx(nxg_citation, pos = nx.spring_layout(nxg_citation))
#plt.title("Example Citations Graph")
#plt.show()

g_twitter = Graph(81306)
print_stats("twitter.txt", g_twitter, " ")

"""
g0 = Graph(8)
g0.addEdge("a", "b")
g0.addEdge("b", "c")
g0.addEdge("c", "d")
g0.addEdge("d", "c")
g0.addEdge("c", "g")
g0.addEdge("g", "f")
g0.addEdge("f", "g")
g0.addEdge("h", "g")
g0.addEdge("h", "d")
g0.addEdge("d", "h")
g0.addEdge("e", "f")
g0.addEdge("e", "a")
g0.addEdge("b", "f")
g0.addEdge("b", "e")
print("SSC in first graph ")
g0.printSCCs("check.txt")

g1 = Graph(5)
g1.addEdge(1, 0)
g1.addEdge(0, 2)
g1.addEdge(2, 1)
g1.addEdge(0, 3)
g1.addEdge(3, 4)
print("SSCs in first graph ")
g1.printSCCs("check.txt")

nxg1 = nx.DiGraph()
elist = [(1, 0), (0, 2), (2, 1), (0, 3), (3, 4)]
nxg1.add_edges_from(elist)
nx.draw_networkx(nxg1, pos = nx.spring_layout(nxg1))
plt.title("Example Graph 1")
plt.show()

g2 = Graph(4)
g2.addEdge(0, 1)
g2.addEdge(1, 2)
g2.addEdge(2, 3)
print("SSCs in second graph ")
g2.printSCCs("check.txt")


nxg2 = nx.DiGraph()
elist = [(0, 1), (1, 2), (2, 3)]
nxg2.add_edges_from(elist)
nx.draw_networkx(nxg2, pos = nx.spring_layout(nxg2))
plt.title("Example Graph 2")
plt.show()


g3 = Graph(7)
g3.addEdge(0, 1)
g3.addEdge(1, 2)
g3.addEdge(2, 0)
g3.addEdge(1, 3)
g3.addEdge(1, 4)
g3.addEdge(1, 6)
g3.addEdge(3, 5)
g3.addEdge(4, 5)
print("SSCs in third graph ")
g3.printSCCs("check.txt")

nxg3 = nx.DiGraph()
elist = [(0, 1), (1, 2), (2, 0), (1, 3), (1, 4), (1, 6), (3, 5), (4, 5)]
nxg3.add_edges_from(elist)
nx.draw_networkx(nxg3, pos = nx.spring_layout(nxg3))
plt.title("Example Graph 3")
plt.show()

g4 = Graph(10)
g4.addEdge(0, 1)
g4.addEdge(0, 3)
g4.addEdge(1, 2)
g4.addEdge(1, 4)
g4.addEdge(2, 0)
g4.addEdge(2, 6)
g4.addEdge(3, 2)
g4.addEdge(4, 5)
g4.addEdge(4, 6)
g4.addEdge(5, 6)
g4.addEdge(5, 7)
g4.addEdge(5, 8)
g4.addEdge(5, 9)
g4.addEdge(6, 4)
g4.addEdge(7, 9)
g4.addEdge(8, 9)
g4.addEdge(9, 8)
print("SSCs in fourth graph ")
g4.printSCCs("check.txt")

nxg4 = nx.DiGraph()
elist = [(0, 1), (0, 3), (1, 2), (1, 4), (2, 0), (2, 6), (3, 2), (4, 5), (4, 6), (5, 6), (5, 7), (5, 8), (5, 9), (6, 4), (7, 9), (8, 9), (9, 8)]
nxg4.add_edges_from(elist)
nx.draw_networkx(nxg4, pos = nx.spring_layout(nxg4))
plt.title("Example Graph 4")
plt.show()

g5 = Graph (5)
g5.addEdge(0, 1)
g5.addEdge(1, 2)
g5.addEdge(2, 3)
g5.addEdge(2, 4)
g5.addEdge(3, 0)
g5.addEdge(4, 2)
print("SSCs in fifth graph ")
g5.printSCCs("check.txt")

nxg5 = nx.DiGraph()
elist = [(0, 1), (1, 2), (2, 3), (2, 4), (3, 0), (4, 2)]
nxg5.add_edges_from(elist)
nx.draw_networkx(nxg5, pos = nx.spring_layout(nxg5))
plt.title("Example Graph 5")
plt.show()
"""