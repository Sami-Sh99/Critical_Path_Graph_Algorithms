import os
from Generator.DAG_Generator import load
from collections import deque
import networkx as nx

def backtrace(prev, start, end):
    node = end
    path = []
    while node != start:
        path.append(node)
        node = prev[node][0]
    path.append(node) 
    path.reverse()
    return path

def bellman_ford(G, source,target):
    if source not in G:
        raise nx.NodeNotFound("Source {} not in G".format(source))

    pred = {source:[]}
    dist = {source:0}

    G_succ = dict(G.adjacency())
    inf = float(0)
    n = len(G)

    count = {}
    q = deque([source])
    in_q = set([source])
    while q:
        u = q.popleft()
        in_q.remove(u)
        # Skip relaxations if any of the predecessors of u is in the queue.
        if all(pred_u not in in_q for pred_u in pred[u]):
            dist_u = dist[u]
            for v, e in dict(G.adjacency())[u].items():
                dist_v = dist_u + G_succ[u][v]['weight']

                if dist_v > dist.get(v, inf):
                    if v not in in_q:
                        q.append(v)
                        in_q.add(v)
                        count_v = count.get(v, 0) + 1
                        count[v] = count_v
                    dist[v] = dist_v
                    pred[v] = [u]

                elif dist.get(v) is not None and dist_v == dist.get(v):
                    pred[v].append(u)

    return backtrace(pred,source,target)


if __name__=='__main__':
    
    fnames=os.listdir('data')
    G = load('data/%s'%fnames[0])
    print("Applying Bellmanford Algorithm")
    print(bellman_ford(G,0,len(G.nodes())-1))