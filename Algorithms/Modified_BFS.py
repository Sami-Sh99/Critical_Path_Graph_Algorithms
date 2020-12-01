import networkx as nx
import os
from DAG_Generator import load
from collections import deque

# Perform BFS on graph g starting from vertex v
def modifiedBFS(g, src):

    q = deque()
    vertices = set([0])

	# (current vertex, current path cost, set of nodes visited so far in current path)
    q.append((src, 0, vertices))

	# stores maximum-cost of path from source
    maxcost = float('-inf')

	# loop till queue is empty
    while q:
        v, cost, vertices = q.popleft()
        maxcost = max(maxcost, cost)
        k = list(g.adjacency())
        for edge in k:
            if not edge in vertices:
                s = set(vertices)
                s.add(edge)
                q.append((edge.dest, cost + edge.weight, s))
    
    return(maxcost)


if __name__ == '__main__':
    fnames=os.listdir('data')
    G = load('data/%s'%fnames[0])
    maxCost = nx.dag_longest_path(G)
    # print([0] + [v for u, v in maxCost])
    print(maxCost)
