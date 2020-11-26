import matplotlib.pyplot as plt
import networkx as nx
import time
from Dijkstra import dijkstra
from FordFulkerson import ford_fulkerson
from Bellmanford import bellman_ford
from TopologicalSort import topological_sort
from DijkstraFib import dijkstraFib
from DAG_Generator import load
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

    # print("Applying Dijkstra Algorithm for %s"%fname)
    # start_time = time.time()
    # shortest_path_D=nx.shortest_path_length(G_neg,0,len(G.nodes())-1)
    # elapsed_time = time.time() - start_time
    # D_V[parse_file(fname)]=float(elapsed_time)

    print("Applying Modified Topological Sort Algorithm for %s"%fname)
    start_time = time.time()
    shortest_path_T=topological_sort(G_neg,topo_order=nx.topological_sort(G))[0]
    elapsed_time = time.time() - start_time
    T_V[parse_file(fname)]=float(elapsed_time)

    print("Applying Modified Bellman Ford Algorithm for %s"%fname)
    start_time = time.time()
    shortest_path_B=nx.bellman_ford_path(G_neg,0,len(G.nodes())-1)
    elapsed_time = time.time() - start_time
    MB_V[parse_file(fname)]=float(elapsed_time)

    # print("D:",shortest_path_D)
    print("T:",shortest_path_T)
    print("B:",shortest_path_B)

    # input("press enter to continues")


plt.title("Time to compute Longest-Path")
plt.xlabel("Number of Vetrices")
plt.ylabel("Time taken (seconds)")
# plt.plot(list(D_V.keys()),list(D_V.values()))
plt.plot(list(MB_V.keys()),list(MB_V.values()))
plt.plot(list(T_V.keys()),list(T_V.values()))
plt.legend(["Modified Bellman Ford","Modified Topological Sort"])
plt.show()

