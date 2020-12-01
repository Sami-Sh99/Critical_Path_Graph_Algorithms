import matplotlib.pyplot as plt
import networkx as nx
import time
from Algorithms.Dijkstra import dijkstra
from Algorithms.FordFulkerson import ford_fulkerson
from Algorithms.Bellmanford import bellman_ford
from Algorithms.TopologicalSort import topological_sort
from Algorithms.DijkstraFib import dijkstraFib
from Generator.DAG_Generator import load
import os

def parse_file(x:str):
    return int(x[x.find('_')+1:x.find('.')])

fnames=os.listdir('data')

D_V=dict()
B_V=dict()
T_V=dict()
MB_V=dict()

for fname in fnames:
    print("loading %s"%fname)
    G = load('data/%s'%fname)
    G_neg = load('data/%s'%fname,True)

    print("Applying Modified Dijkstra Algorithm for %s"%fname)
    start_time = time.time()
    shortest_path_D=dijkstra(G,0,len(G.nodes())-1)
    elapsed_time = time.time() - start_time
    D_V[parse_file(fname)]=float(elapsed_time)

    print("Applying Topological Sort Algorithm for %s"%fname)
    start_time = time.time()
    shortest_path_T=nx.dag_longest_path(G)
    elapsed_time = time.time() - start_time
    T_V[parse_file(fname)]=float(elapsed_time)

    print("Applying Bellman Ford Algorithm for %s"%fname)
    start_time = time.time()
    shortest_path_B=bellman_ford(G,0,len(G.nodes())-1)
    elapsed_time = time.time() - start_time
    B_V[parse_file(fname)]=float(elapsed_time)

    print("D:",shortest_path_D)
    print("T:",shortest_path_T)
    print("B:",shortest_path_B)


plt.title("Time to compute Longest-Path")
plt.xlabel("Number of Vetrices")
plt.ylabel("Time taken (seconds)")
plt.plot(list(D_V.keys()),list(D_V.values()))
plt.plot(list(B_V.keys()),list(B_V.values()))
plt.plot(list(T_V.keys()),list(T_V.values()))
plt.legend(["Modified Dijkstra","Bellman Ford","Topological Sort"])
plt.show()

