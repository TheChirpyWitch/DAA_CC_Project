from collections import defaultdict
import sys
sys.setrecursionlimit(30000)

class Graph:

	def __init__(self,vertices):
		self.V= vertices
		self.graph = defaultdict(list)
		self.Time = 0
		self.disc = {}
		self.low = {}
		self.stackMember = {}
		self.max_scc = []

	def addEdge(self,u,v):
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
		#print(self.graph[u])
		#print(disc)
		for v in self.graph[u]:
			#print(v)	
			if disc[v] == -1:			
				self.SCCUtil(v, low, disc, stackMember, st, output_file)
				low[u] = min(low[u], low[v])						
			elif stackMember[v] == True:
				low[u] = min(low[u], disc[v])
		w = -1
		ofile = open(output_file, "a")
		if low[u] == disc[u]:
			scc = []
			while w != u:
				w = st.pop()
				scc.append(w)
				stackMember[w] = False	
			#print(scc)
			ofile.write(str(scc) + "\n")
			if len(scc) > len(self.max_scc):
				self.max_scc = scc
			
	def printSCCs(self, output_file):
		#disc = [-1] * (self.V)
		#low = [-1] * (self.V)
		#stackMember = [False] * (self.V)
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

def edges_associated(g):
    n = 0
    for e in g.max_scc:
        for e2 in g.graph[e]:
            if e2 in g.max_scc:
                n += 1
    return n

def print_stats(file_name, g, split_by):
    g = make_graph(file_name, g, split_by)
    file = file_name[:-4] + "_SCCs_tarjan.txt"
    g.printSCCs(file)
    print("SSC Stats in " + file_name[:-4] + " graph ")
    print("Number of nodes in largest SCC: " + str(len(g.max_scc)))
    print("Number of edges in largest SCC: " + str(edges_associated(g)))

#g_citation = Graph(27770)
#print_stats("citation.txt", g_citation, "\t")

g_twitter = Graph(81306)
print_stats("twitter.txt", g_twitter, " ")

"""
g1 = Graph(5)
g1.addEdge(1, 0)
g1.addEdge(0, 2)
g1.addEdge(2, 1)
g1.addEdge(0, 3)
g1.addEdge(3, 4)
print("SSCs in first graph ")
g1.printSCCs("check.txt")

g2 = Graph(4)
g2.addEdge(0, 1)
g2.addEdge(1, 2)
g2.addEdge(2, 3)
print("SSCs in second graph ")
g2.printSCCs("check.txt")


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


g5 = Graph (5)
g5.addEdge(0, 1)
g5.addEdge(1, 2)
g5.addEdge(2, 3)
g5.addEdge(2, 4)
g5.addEdge(3, 0)
g5.addEdge(4, 2)
print("SSCs in fifth graph ")
g5.printSCCs("check.txt")
"""