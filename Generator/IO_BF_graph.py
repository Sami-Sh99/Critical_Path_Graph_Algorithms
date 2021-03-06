import matplotlib.pyplot as plt
import networkx as nx
from Algorithms.Bellmanford import bellman_ford


def is_sublist(x,y):
    try:
        if abs(y.index(x[0])-y.index(x[1]))==1:
            return True
        return False
    except:
        return False

#Create Empty digraph G
G = nx.DiGraph()

#Add nodes to G
G.add_node('1',pos=(0,0))
G.add_node('2',pos=(1,0))
G.add_node('3',pos=(0,1))
G.add_node('4',pos=(1,1))
G.add_node('5',pos=(2,0))
G.add_node('6',pos=(2,1))

#Add directed edges to G
G.add_edges_from([("1", "2", {'weight':5})])
G.add_edges_from([("1", "3", {'weight':6})])
G.add_edges_from([("2", "3", {'weight':3})])
G.add_edges_from([("2", "4", {'weight':8})])
G.add_edges_from([("3", "5", {'weight':2})])
G.add_edges_from([("3", "6", {'weight':11})])
G.add_edges_from([("4", "5", {'weight':1})])
G.add_edges_from([("4", "6", {'weight':1})])
G.add_edges_from([("5", "6", {'weight':12})])



graph = G.copy()
# reduced_graph = reduce_graph(graph)
G_f = bellman_ford(graph, '1','6')

print(G_f)
#print distance table:
shortest_path=G_f[1]

#Color the critical nodes in blue
node_colors = ["g" if n in shortest_path else "r" for n in G.nodes()]
edge_colors = ["g" if is_sublist([u,v],shortest_path) else "r" for u,v in G.edges()]
#Get list of labels & positions 
labels = nx.get_edge_attributes(G,'capacity')
pos=nx.get_node_attributes(G,'pos')

#Draw the digraph
nx.draw(G,pos,with_labels=True,edge_color=edge_colors)
nx.draw_networkx_nodes(G,pos,node_color=node_colors)
nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)

plt.show()

