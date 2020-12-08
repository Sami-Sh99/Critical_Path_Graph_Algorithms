from queue import PriorityQueue
from heapq import heappush, heappop
from itertools import count
from math import inf
import time
import os
from Generator.DAG_Generator import load
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
    adj=graph.adj
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
    return backtrace(prev, start, end), dist

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

if __name__ == "__main__":
    fnames=os.listdir('data')
    G = load('data/%s'%fnames[0])
    Gi = load('data/%s'%fnames[0],True)
    print("Applying Dijkstra Algorithm")
    print(dijkstra(G,0,len(G.nodes())-1 ))
                    