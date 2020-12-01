import networkx as nx
import matplotlib.pyplot as plt
from networkx.readwrite import json_graph
import json
import random
from random import randrange
from math import floor,ceil

nb_of_generated_graphs=40
min_nb_of_nodes=500
nb_of_nodes=5000
edge_prob=0.05
max_weight=20
min_weight=2

def get_dependencies(table,target):
    ans=list()
    for u,v,_ in table:
        if(v==target):
            ans.append(u)
    return ans

def get_fuzzy_weight():
    a1=randrange(min_weight,int(max_weight/4))
    a2=randrange(int(max_weight/4),int(max_weight/2))
    a3=randrange(int(max_weight/2),ceil(3*max_weight/4))
    a4=randrange(ceil(3*max_weight/4),max_weight)
    return a1,a2,a3,a4

def ranking_function(a):
    return(a[0]+2*a[1]+2*a[2]+a[3])/6

def add_a(a,b):
    return (a[0]+b[0],a[1]+b[1],a[2]+b[2],a[3]+b[3])

def sub_a(a,b):
    return (a[0]-b[0],a[1]-b[1],a[2]-b[2],a[3]-b[3])

def compute_ES():
    global fuzzy_table
    global tasks
    global G
    for i,j,f in fuzzy_table:
        t=add_a(tasks['task'+str(i)]['ES'],G[i][j]['fuzzy'])
        if ranking_function(t)>ranking_function(tasks['task'+str(j)]['ES']):
            tasks['task'+str(j)]['ES']=t

def compute_LS():
    global fuzzy_table
    global tasks
    global G
    for i in sorted(tasks.keys(),reverse=True):
        n=i[4:]
        L=list()
        if ranking_function(tasks[i]['LS'])!=0:
            L.append(tasks[i]['LS'])
        J=G._succ[n]
        for j in J:
            x=sub_a(tasks['task'+str(j)]['LS'],G[n][j]['fuzzy'])
            if ranking_function(x)>0: L.append(x)
        tasks[i]['LS']=min(L,key=lambda x: ranking_function(x))

def compute_T():
    global fuzzy_table
    global tasks
    global G
    T=dict()
    for i,j,f in reversed(fuzzy_table):
        t=sub_a(tasks['task'+str(j)]['LS'],G[i][j]['fuzzy'])
        T[str(i)+'-'+str(j)]=sub_a(t,tasks['task'+str(i)]['ES'])
    return T
        

tasks = dict() #contains all the tasks
fuzzy_table1=[
    ("1", "2", {'fuzzy':(10,15,15,20)}),
    ("1", "3", {'fuzzy':(30,40,40,50)}),
    ("2", "3", {'fuzzy':(30,40,40,50)}),
    ("1", "4", {'fuzzy':(15,20,25,30)}),
    ("2", "5", {'fuzzy':(60,100,150,180)}),
    ("3", "5", {'fuzzy':(60,100,150,180)}),
    ("4", "5", {'fuzzy':(60,100,150,180)})
]

fuzzy_table=[
    ("1", "2", {'fuzzy':(2,2,3,4)}),
    ("1", "3", {'fuzzy':(2,3,3,6)}),
    ("1", "5", {'fuzzy':(2,3,4,5)}),
    ("2", "4", {'fuzzy':(2,2,4,5)}),
    ("2", "5", {'fuzzy':(2,4,5,8)}),
    ("3", "4", {'fuzzy':(1,1,2,2)}),
    ("3", "6", {'fuzzy':(7,8,11,15)}),
    ("4", "5", {'fuzzy':(2,3,3,5)}),
    ("4", "6", {'fuzzy':(3,3,4,6)}),
    ("5", "6", {'fuzzy':(1,1,1,2)}),
]

# G=generate_random_dag(10,0.2)
G=nx.DiGraph()
G.add_edges_from(fuzzy_table)
G_adj=G.adj
s=sorted(G.nodes())
# print(nx.dag_longest_path(G))
# exit()
for u in s: #slide the file line by line
    tasks['task'+ str(u) ]= dict()
    tasks['task'+ str(u) ]['id'] = u
    tasks['task'+ str(u) ]['name'] = u
    tasks['task'+ str(u) ]['ES'] = (0,0,0,0)
    tasks['task'+ str(u) ]['LS'] = (0,0,0,0)


compute_ES()

#Assign LS=ES to Sink Node
f=max(x[4:] for x in tasks.keys())
tasks['task'+f]["LS"]=tasks['task'+f]['ES']

compute_LS()

CPM=compute_T()

ansE=list()
ansN=set()
for t,f in CPM.items():
    t=t.split('-')
    if(f == (0,0,0,0)):
        ansE.append( (int(t[0]),int(t[1])) )
        ansN.add(int(t[0]))
        ansN.add(int(t[1]))

#Draw the digraph
pos=nx.spring_layout(G,weight=None)
node_colors = ["g" if int(n) in ansN else "b" for n in G.nodes()]
edge_colors = ["g" if (int(u),int(v)) in ansE else "b" for u,v in G.edges()]
nx.draw(G,with_labels=True,pos=pos,edge_color=edge_colors)
nx.draw_networkx_nodes(G,node_color=node_colors,pos=pos)
plt.show()

             
            
        
                
            
    
        
        
        
    



    













