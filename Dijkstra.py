# dependencies for our dijkstra's implementation
from queue import PriorityQueue
from heapq import heappush, heappop
from itertools import count
from math import inf
import time
import os
from DAG_Generator import load
# graph dependency  
import networkx as nx


def dijkstra(graph: 'networkx.classes.graph.Graph', start: str, end: str) -> 'List':
    def backtrace(prev, start, end):
        node = end
        path = []
        while node != start:
            path.append(node)
            node = prev[node]
        path.append(node) 
        path.reverse()
        return path
        
    def cost(u, v):
        """get the cost of edges from node -> node; cost(u,v) = edge_weight(u,v)"""
        return graph.get_edge_data(u,v).get('weight')
    # predecessor of current node on shortest path 
    prev = {} 
    # initialize distances from start -> given node i.e. dist[node] = dist(start, node)
    dist = {v: inf for v in list(nx.nodes(graph))} 
    # nodes we've visited
    visited = set() 
    # prioritize nodes from start -> node with the shortest distance!
    ## elements stored as tuples (distance, node) 
    pq = PriorityQueue()  
    
    dist[start] = 0  # dist from start -> start is zero
    pq.put((dist[start], start))
    adj=dict(graph.adjacency())
    start_time = time.time()
    while 0 != pq.qsize():
        curr_cost, curr = pq.get()
        visited.add(curr)
        # look at curr's adjacent nodes
        for neighbor in adj.get(curr):
            # if we found a shorter path 
            path = dist[curr] + cost(curr, neighbor)
            if path > dist[neighbor] or dist[neighbor]==inf:
                # update the distance, we found a shorter one!
                dist[neighbor] = path
                # update the previous node to be prev on new shortest path
                prev[neighbor] = curr
                # insert into priority queue and mark as visited
                visited.add(neighbor)
                pq.put((dist[neighbor],neighbor))
    elapsed_time = time.time() - start_time                
    return elapsed_time, backtrace(prev, start, end), dist

def backPropagate(graph: 'networkx.classes.graph.DiGraph', start: str, end: str,init: int) -> 'List':

    rev=graph.reverse()

    def backtrace(prev, start, end):
        node = end
        path = []
        while node != start:
            path.append(node)
            node = prev[node]
        path.append(node) 
        path.reverse()
        return path
        
    def cost(u, v):
        """get the cost of edges from node -> node; cost(u,v) = edge_weight(u,v)"""
        return rev.get_edge_data(u,v).get('weight')
        
    # predecessor of current node on shortest path 
    prev = {} 
    # initialize distances from start -> given node i.e. dist[node] = dist(start, node)
    dist = {v: init for v in list(nx.nodes(rev))} 
    # nodes we've visited
    visited = set() 
    # prioritize nodes from start -> node with the shortest distance!
    ## elements stored as tuples (distance, node) 
    pq = PriorityQueue()  
    
    # dist[start] = 0  # dist from start -> start is zero
    pq.put((dist[start], start))
    
    while 0 != pq.qsize():
        curr_cost, curr = pq.get()
        visited.add(curr)
        # print(f'visiting {curr}')
        # look at curr's adjacent nodes
        for neighbor in dict(rev.adjacency()).get(curr):
            # if we found a shorter path 
            path = max(0,dist[curr] - cost(curr, neighbor))
            if path < dist[neighbor]:
                # update the distance, we found a shorter one!
                dist[neighbor] = path
                # update the previous node to be prev on new shortest path
                prev[neighbor] = curr
                pq.put((dist[neighbor],neighbor))
    return backtrace(prev, start, end), dist


def single_source_dijkstra(G, source, target=None, cutoff=None,
                           weight='weight'):

    return multi_source_dijkstra(G, {source}, cutoff=cutoff, target=target,
                                 weight=weight)

def multi_source_dijkstra(G, sources, target=None, cutoff=None,
                          weight='weight'):
    if not sources:
        raise ValueError('sources must not be empty')
    if target in sources:
        return (0, [target])
    weight = _weight_function(G, weight)
    paths = {source: [source] for source in sources}  # dictionary of paths
    dist = _dijkstra_multisource(G, sources, weight, paths=paths,
                                 cutoff=cutoff, target=target)
    if target is None:
        return (dist, paths)
    try:
        return (dist, paths[target])
    except KeyError:
        raise nx.NetworkXNoPath("No path to {}.".format(target))

def _weight_function(G, weight):
    if callable(weight):
        return weight
    # If the weight keyword argument is not callable, we assume it is a
    # string representing the edge attribute containing the weight of
    # the edge.
    if G.is_multigraph():
        return lambda u, v, d: min(attr.get(weight, 1) for attr in d.values())
    return lambda u, v, data: data.get(weight, 1)

def _dijkstra_multisource(G, sources, weight, pred=None, paths=None,
                          cutoff=None, target=None):

    G_succ = G._succ if G.is_directed() else G._adj

    push = heappush
    pop = heappop
    dist = {}  # dictionary of final distances
    seen = {}
    # fringe is heapq with 3-tuples (distance,c,node)
    # use the count c to avoid comparing nodes (may not be able to)
    c = count()
    fringe = []
    for source in sources:
        if source not in G:
            raise nx.NodeNotFound("Source {} not in G".format(source))
        seen[source] = 0
        push(fringe, (0, next(c), source))
    while fringe:
        (d, _, v) = pop(fringe)
        if v in dist:
            continue  # already searched this node.
        dist[v] = d
        if v == target:
            break
        for u, e in G_succ[v].items():
            cost = weight(v, u, e)
            if cost is None:
                continue
            vu_dist = dist[v] + cost
            if cutoff is not None:
                if vu_dist > cutoff:
                    continue
            if u in dist:
                if vu_dist < dist[u]:
                    raise ValueError('Contradictory paths found:',
                                     'negative weights?')
            elif u not in seen or vu_dist > seen[u]:
                seen[u] = vu_dist
                push(fringe, (vu_dist, next(c), u))
                if paths is not None:
                    paths[u] = paths[v] + [u]
                if pred is not None:
                    pred[u] = [v]
            elif vu_dist == seen[u]:
                if pred is not None:
                    pred[u].append(v)

    # The optional predecessor and path dictionaries can be accessed
    # by the caller via the pred and paths objects passed as arguments.
    return dist

if __name__ == "__main__":
    fnames=os.listdir('data')
    G = load('data/%s'%fnames[0])
    Gi = load('data/%s'%fnames[0],True)
    print("Applying Dojkstra Algorithm")
    print(dijkstra(G,0,len(G.nodes())-1 ))       #Heap Dijkstra
    print(nx.dag_longest_path(G))                   #Topological Sort
    print(nx.bellman_ford_path(Gi,0,len(G.nodes())-1))  #ModifiedBellman
                    