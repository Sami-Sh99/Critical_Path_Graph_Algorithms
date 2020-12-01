import networkx as nx
import os
from DAG_Generator import load

def topological_sort(G, weight="weight", default_weight=1, topo_order=None):
    if not G:
        return []

    if topo_order is None:
        topo_order = nx.topological_sort(G)

    dist = {}  # stores {v : (length, u)}
    for v in topo_order:
        us = [
            (dist[u][0] + data.get(weight, default_weight), u)
            for u, data in G.pred[v].items()
        ]

        # Use the best predecessor if there is one and its distance is
        # non-negative, otherwise terminate.
        maxu = min(us, key=lambda x: x[0]) if us else (0, v)
        dist[v] = maxu if maxu[0] >= -1000 else (0, v)  #TODO Change -1000 to -inf

    u = None
    v = min(dist, key=lambda x: dist[x][0])
    path = []
    while u != v:       #Backtrace
        path.append(v)
        u = v
        v = dist[v][1]

    path.reverse()
    return path,dist

if __name__=='__main__':
    
    fnames=os.listdir('data')
    G = load('data/%s'%fnames[0],True)
    print("Applying Topo Algorithm")
    print(topological_sort(G)[0])