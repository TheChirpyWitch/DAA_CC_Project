# DAA_CC_Project

Kosaraju's Algorithm:

Test Cases:
1. SSCs in first graph
* [1, 2, 0]
* [3]
* [4]
2. SSCs in second graph
* [0]
* [1]
* [2]
* [3]
3. SSCs in third graph
* [0, 2, 1]
* [6]
* [4]
* [3]
* [5]
4. SSCs in fourth graph
* [0, 2, 1, 3]
* [6, 4, 5]
* [7]
* [9, 8]
5. SSCs in fifth graph
* [0, 3, 2, 1, 4]

SSC Stats in citation graph 
* Number of nodes in largest SCC: 7464
* Number of edges in largest SCC: 116268

SSC Stats in twitter graph 
* Number of nodes in largest SCC: 68413
* Number of edges in largest SCC: 2322563

Tarjan's Algorithm:

Test Cases:
1. SSCs in first graph 
* [4]
* [3]
* [1, 2, 0]
2. SSCs in second graph 
* [3]
* [2]
* [1]
* [0]
3. SSCs in third graph 
* [5]
* [3]
* [4]
* [6]
* [2, 1, 0]
4. SSCs in fourth graph 
* [8, 9]
* [7]
* [5, 4, 6]
* [3, 2, 1, 0]
5. SSCs in fifth graph 
* [4, 3, 2, 1, 0]

SSC Stats in citation graph 
* Number of nodes in largest SCC: 7464
* Number of edges in largest SCC: 116268

SSC Stats in twitter graph 
* Number of nodes in largest SCC: 68413
* Number of edges in largest SCC: 2322563

Next Steps:
* Graph Condensation
* Compare with networkx's strongly_connected_components_recursive(uses Tarjan's) and kosaraju_strongly_connected_components.
