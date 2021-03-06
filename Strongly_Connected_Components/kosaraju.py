from collections import defaultdict
import sys
import matplotlib.pyplot as plt
import networkx as nx
from datetime import datetime
startTime = datetime.now()
sys.setrecursionlimit(30000)

class Graph:
   
    def __init__(self, vertices):
        self.V = vertices
        self.graph = defaultdict(list)
        self.visited = {}
        self.max_scc = []
        #self.condensed_nodes = {}
   
    def addEdge(self, u, v):
        self.graph[u].append(v)
        if u not in self.visited:
            self.visited[u] = False
        if v not in self.visited:
            self.visited[v] = False
   
    def DFS_(self, v, visited, scc):
        visited[v] = True
        scc.append(v)
        for i in self.graph[v]:
            if visited[i] == False:
                self.DFS_(i,visited, scc)

    def fill(self,v,visited, stack):
        visited[v] = True
        for i in self.graph[v]:
            if visited[i] == False:
                self.fill(i, visited, stack)
        stack = stack.append(v)
  
    def getTranspose(self):
        g = Graph(self.V)  
        for i in self.graph:
            for j in self.graph[i]:
                g.addEdge(j,i)
        return g

    def printSCCs(self, output_file):          
        stack = []
        for i in self.visited:
            if self.visited[i] == False:
                self.fill(i, self.visited, stack)
        ofile = open(output_file, "a")
        """
        for key in self.graph:
            group = " "
            for val in self.graph[key]:
                group = group + val + " "
            ofile.write(key + group + "\n")
        #print(self.graph)
        """
        gr = self.getTranspose()
        print("Transposed graph:")
        print(dict(gr.graph))
        for i in self.visited:
            self.visited[i] = False
        while stack:
            i = stack.pop()
            if self.visited[i] == False:
                scc = []
                #self.condensed_nodes_roots.append(i)
                gr.DFS_(i, self.visited, scc)
                print(scc)
                ofile.write(str(scc) + "\n")
                if len(scc) > len(self.max_scc):
                    self.max_scc = scc

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
    G = nx.DiGraph()
    elist = []
    for node in g.max_scc:
        for e2 in g.graph[node]:
            if e2 in g.max_scc:
                elist.append([node, e2])
                n += 1
    #G.add_edges_from(elist)
    return n, elist

def print_stats(file_name, g, split_by):
    g = make_graph(file_name, g, split_by)
    file = file_name[:-4] + "_SCCs_kosaraju.txt"
    print("SSC Stats in " + file_name[:-4] + " graph ")
    print(datetime.now() - startTime)
    g.printSCCs(file)
    print(datetime.now() - startTime)
    n_e, elist = edges_associated(g)
    print("Number of nodes in largest SCC: " + str(len(g.max_scc)))
    print("Number of edges in largest SCC: " + str(n_e))
    write_file_name = file_name[:-4] + "_SCC_edgelist_kosaraju_.csv"
    write_file = open(write_file_name, "w+")
    for el in elist:
        c = str(el[0]) + " " + str(el[1]) + "\n"
        write_file.write(c)
    #nx.draw_networkx(max_scc, pos = nx.spring_layout(max_scc))
    #plt.title("SCC in " + file_name[:-4] + " graph")
    #plt.show()


#g_citation = Graph(27770)
#print_stats("citation.txt", g_citation, "\t")

#g_twitter = Graph(81306)
#print_stats("twitter.txt", g_twitter, " ")


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
print("SSC in zeroth graph ")
g0.printSCCs("check1.txt")

"""
g1 = Graph(5)
g1.addEdge(1, 0)
g1.addEdge(0, 2)
g1.addEdge(2, 1)
g1.addEdge(0, 3)
g1.addEdge(3, 4)
print("SSC in first graph ")
g1.printSCCs("check1.txt")

g2 = Graph(4)
g2.addEdge(0, 1)
g2.addEdge(1, 2)
g2.addEdge(2, 3)
print("SSC in second graph ")
g2.printSCCs("check1.txt")


g3 = Graph(7)
g3.addEdge(0, 1)
g3.addEdge(1, 2)
g3.addEdge(2, 0)
g3.addEdge(1, 3)
g3.addEdge(1, 4)
g3.addEdge(1, 6)
g3.addEdge(3, 5)
g3.addEdge(4, 5)
print("SSC in third graph ")
g3.printSCCs("check1.txt")

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
print("SSC in fourth graph ")
g4.printSCCs("check1.txt")


g5 = Graph (5)
g5.addEdge(0, 1)
g5.addEdge(1, 2)
g5.addEdge(2, 3)
g5.addEdge(2, 4)
g5.addEdge(3, 0)
g5.addEdge(4, 2)
print("SSC in fifth graph ")
g5.printSCCs("check1.txt")
"""