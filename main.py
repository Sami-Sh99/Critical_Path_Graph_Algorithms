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
FD_V=dict()

#Dijsktra
for fname in fnames:
    print("loading %s"%fname)
    G = load('data/%s'%fname)

    print("Applying Dijkstra Algorithm")
    start_time = time.time()
    shortest_path=dijkstra(G,0,len(G.nodes())-1)
    elapsed_time = time.time() - start_time
    D_V[parse_file(fname)]=float(elapsed_time)


#Belmand
# for fname in fnames:
#     #Create Empty digraph G
#     print("loading %s"%fname)
#     G = load('data/%s'%fname)

#     print("Applying Bellman Algorithm")
#     start_time = time.time()
#     shortest_path=bellman_ford(G,0,len(G.nodes())-1)
#     elapsed_time = time.time() - start_time
#     B_V[parse_file(fname)]=float(elapsed_time)

#Topological Sort
for fname in fnames:
    #Create Empty digraph G
    print("loading %s"%fname)
    G = load('data/%s'%fname)

    print("Applying Topological Sort Algorithm")
    start_time = time.time()
    shortest_path=topological_sort(G)
    elapsed_time = time.time() - start_time
    T_V[parse_file(fname)]=float(elapsed_time)


#Fibonacci Dijkstra
for fname in fnames:
    #Create Empty digraph G
    print("loading %s"%fname)
    G = load('data/%s'%fname)

    print("Applying Fibonacci Dijkstra Algorithm")
    start_time = time.time()
    shortest_path=dijkstraFib(G,0,len(G.nodes())-1)
    elapsed_time = time.time() - start_time
    FD_V[parse_file(fname)]=float(elapsed_time)


plt.title("Time to compute Longest-Path")
plt.xlabel("Number of Vetrices")
plt.ylabel("Time taken (seconds)")
plt.plot(list(D_V.keys()),list(D_V.values()))
plt.plot(list(B_V.keys()),list(B_V.values()))
plt.plot(list(T_V.keys()),list(T_V.values()))
plt.plot(list(FD_V.keys()),list(FD_V.values()))
plt.legend(["Dijkstra","Bellman Ford","Topological Sort","Fibonacci Dijkstra"])
plt.show()

