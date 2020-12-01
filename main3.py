import matplotlib.pyplot as plt
import networkx as nx
import time
import Fuzzy
from DAG_Generator import load
import os

def parse_file(x:str):
    return int(x[x.find('_')+1:x.find('.')])

fnames=os.listdir('data')[0:5]

F_V=dict()
MF_V=dict()

for fname in fnames:
    print("loading %s"%fname)
    G = load('data/%s'%fname)
    for u,v in G.edges():
        if u=='791':
            _=0
            pass
        w=Fuzzy.get_fuzzy_weight()
        G[u][v]['weight']=w
        G[u][v]['fuzzy']=w


    print("Applying Fuzzy Algorithm for %s"%fname)
    start_time = time.time()
    shortest_path_T=Fuzzy.Fuzzy_CPM(G)
    elapsed_time = time.time() - start_time
    print(elapsed_time)
    F_V[parse_file(fname)]=float(elapsed_time)

    print("Applying Modified Fuzzy Algorithm for %s"%fname)
    start_time = time.time()
    shortest_path_T=Fuzzy.modified_Fuzzy(G)
    elapsed_time = time.time() - start_time
    print(elapsed_time)
    MF_V[parse_file(fname)]=float(elapsed_time)

plt.title("Time to compute Longest-Fuzzy-Path")
plt.xlabel("Number of Vetrices")
plt.ylabel("Time taken (seconds)")
plt.plot(list(F_V.keys()),list(F_V.values()))
plt.plot(list(MF_V.keys()),list(MF_V.values()))
plt.legend(["Fuzzy","Modified Fuzzy"])
plt.show()

