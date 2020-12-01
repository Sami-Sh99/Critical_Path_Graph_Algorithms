#!/usr/bin/env python

import networkx as nx
# import matplotlib.pyplot as plt
from networkx.readwrite import json_graph
import json
import random
from random import randrange

nb_of_generated_graphs=40
min_nb_of_nodes=500
nb_of_nodes=5000
edge_prob=0.05
max_weight=10
min_weight=2

def generate_random_dag(n, p):

    random_graph = nx.fast_gnp_random_graph(n, p, directed=True)
    random_dag = nx.DiGraph([
        [u, v,{'weight':randrange(min_weight,max_weight)}] for (u, v) in random_graph.edges() if u < v
    ])
    while True:
        try:
        #Ensure that source is connected to all vertices
            for node in random_dag.nodes():
                if node!=0 and not nx.has_path(random_dag,0,node):
                    random_dag.add_edges_from([(0,node,{'weight':1})])

            #Ensure that only the sink has an out degree equal to zero
            x= dict(random_dag.out_degree())
            for node in random_dag.nodes():
                if x[node]==0 and node!=n-1:
                    random_dag.add_edges_from([(node,n-1,{'weight':1})])

            c=nx.find_cycle(random_dag, orientation="original")
            x,y=get_reversed_edge(c)
            if x is not None : 
                random_dag.remove_edge(x,y)
                # random_dag.remove_edges_from([(x,y)])
            # random_graph = nx.fast_gnp_random_graph(n, p, directed=True)
    #         random_dag = nx.DiGraph([
    #     [u, v,{'weight':randrange(min_weight,max_weight)}] for (u, v) in random_graph.edges() if u < v
    # ])
        except nx.NetworkXNoCycle:
            if nx.is_weakly_connected(random_dag):
                break
            print("acyclic but not weakly connected")
    return random_dag

def save(G, fname):
    data=json_graph.node_link_data(G)

    with open(fname, 'w') as json_file:
        json.dump(data, json_file)


def load(fname, inverse=False)->'networkx.classes.graph.DiGraph':
    with open(fname, "r") as read_file:
        data = json.load(read_file)
    G=json_graph.node_link_graph(data,directed=True,multigraph=False)
    if inverse:
        G_p=G.copy()
        for u,v in G.edges():
            G_p[u][v]['weight']=-G[u][v]['weight']
        return G_p
    return G

def get_reversed_edge(cycle):
    for edge in cycle:
        u,v,_=edge
        if u>v:
            return u,v
    return None,None

if __name__ == '__main__':
    for n in random.sample(range(min_nb_of_nodes,nb_of_nodes), nb_of_generated_graphs):
        G=generate_random_dag(n, edge_prob)
        save(G,"data/DAG_%d.json" % n)
    # G=load("sout.json")
    
    
    #Draw the digraph
    # nx.draw(G,with_labels=True)
    # plt.show()