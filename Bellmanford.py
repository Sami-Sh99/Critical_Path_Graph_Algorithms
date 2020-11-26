import os
from DAG_Generator import load
from collections import deque
import networkx as nx
def initialize(graph, source):
    d = {} # Stands for destination
    p = {} # Stands for predecessor
    for node in graph:
        d[node] = -1#float('Inf') # We start admitting that the rest of nodes are very very far
        p[node] = None
    d[source] = 0 # For the source we know how to reach
    return d, p

def relax(node, neighbour, graph, d, p):
    # If the distance between the node and the neighbour is lower than the one I have now
    if d[neighbour] < d[node] + graph[node][neighbour]['weight']:
        # Record this lower distance
        d[neighbour]  = d[node] + graph[node][neighbour]['weight']
        p[neighbour] = node

def backtrace(prev, start, end):
    node = end
    path = []
    while node != start:
        path.append(node)
        node = prev[node][0]
    path.append(node) 
    path.reverse()
    return path

def bellman_ford(G, source,target,pred=None, paths=None, dist=None):
    if source not in G:
        raise nx.NodeNotFound("Source {} not in G".format(source))

    if pred is None:
        pred = {source:[]}

    if dist is None:
        dist = {source:0}

    G_succ = G.succ if G.is_directed() else G.adj
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
            for v, e in G_succ[u].items():
                dist_v = dist_u + G_succ[u][v]['weight']

                if dist_v > dist.get(v, inf):
                    if v not in in_q:
                        q.append(v)
                        in_q.add(v)
                        count_v = count.get(v, 0) + 1
                        if count_v == n:
                            raise nx.NetworkXUnbounded(
                                "Negative cost cycle detected.")
                        count[v] = count_v
                    dist[v] = dist_v
                    pred[v] = [u]

                elif dist.get(v) is not None and dist_v == dist.get(v):
                    pred[v].append(u)

    if paths is not None:
        dsts = [target] if target is not None else pred
        for dst in dsts:

            path = [dst]
            cur = dst

            while pred[cur]:
                cur = pred[cur][0]
                path.append(cur)

            path.reverse()
            paths[dst] = path

    return backtrace(pred,source,target)


if __name__=='__main__':
    
    fnames=os.listdir('data')
    G = load('data/%s'%fnames[0])
    print("Applying Bellmanford Algorithm")
    print(bellman_ford(G,0,len(G.nodes())-1))