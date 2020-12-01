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
    ss=sorted(list(reversed(list(G.edges()))),reverse=True)
    for i,j in ss:
        t=sub_a(tasks['task'+str(j)]['LS'],G[i][j]['fuzzy'])
        tij=ranking_function(t)
        lsj=ranking_function(tasks['task'+str(j)]['LS'])
        if tij<lsj:
            tasks['task'+str(i)]['LS']=t


def compute_T():
    global fuzzy_table
    global tasks
    global G
    T=dict()
    for i,j,f in reversed(fuzzy_table):
        t=sub_a(tasks['task'+str(j)]['LS'],G[i][j]['fuzzy'])
        tasks['task'+str(i)]['float']= sub_a(t,tasks['task'+str(i)]['ES'])
        T[str(i)+'-'+str(j)]=sub_a(t,tasks['task'+str(i)]['ES'])
    return T
        

def get_reversed_edge(cycle):
    for edge in cycle:
        u,v,_=edge
        if u>v:
            return u,v
    return None,None

line = list() #contains a single line
singleElement = list()
tasks = dict() #contains all the tasks
number = -1
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

gg=[(i,j,{'weight':ranking_function(k['fuzzy'])}) for i,j,k in fuzzy_table]

# G=generate_random_dag(10,0.2)
G=nx.DiGraph()
G.add_edges_from(fuzzy_table)
G_adj=G.adj
s=sorted(G.nodes())
# print(nx.dag_longest_path(G))
# exit()
for u in s: #slide the file line by line
    number += 1
    tasks['task'+ str(u) ]= dict()
    tasks['task'+ str(u) ]['id'] = u
    tasks['task'+ str(u) ]['name'] = u
    # tasks['task'+ str(u) ]['duration'] = f['fuzzy']
    dependencies=get_dependencies(fuzzy_table,u)
    if(len(dependencies)!=0):
        tasks['task'+ str(u) ]['dependencies'] = dependencies
    else:
        tasks['task'+ str(u) ]['dependencies'] = ['-1']
    tasks['task'+ str(u) ]['ES'] = (0,0,0,0)
    tasks['task'+ str(u) ]['EF'] = (0,0,0,0)
    tasks['task'+ str(u) ]['LS'] = (0,0,0,0)
    tasks['task'+ str(u) ]['LF'] = (0,0,0,0)
    tasks['task'+ str(u) ]['float'] = (0,0,0,0)
    tasks['task'+ str(u) ]['isCritical'] = False


compute_ES()

f=max(x[4:] for x in tasks.keys())
tasks['task'+f]["LS"]=tasks['task'+f]['ES']

compute_LS()

print(compute_T())
exit()
print('task\t ES\t LS\t float\t isCritical')
for task in tasks:
    if(tasks[task]['float'] == (0,0,0,0)):
        tasks[task]['isCritical'] = True
    print(str(task) +'\t '+str(tasks[task]['ES']) +'\t '+str(tasks[task]['LS']) +'\t '+str(tasks[task]['float']) +'\t '+str(tasks[task]['isCritical']))
    

#Draw the digraph
pos=nx.spring_layout(G,weight=None)
node_colors = ["g" if tasks["task%s"%n]['isCritical'] else "b" for n in G.nodes()]
edge_colors = ["g" if tasks["task%s"%u]['isCritical'] and tasks["task%s"%v]['isCritical'] and tasks["task%s"%u]['ES']== sub_a(tasks["task%s"%v]['ES'],G[u][v]['fuzzy']) else "b" for u,v in G.edges()]
nx.draw(G,with_labels=True,pos=pos,edge_color=edge_colors)
nx.draw_networkx_nodes(G,node_color=node_colors,pos=pos)
plt.show()

             
            
        
                
            
    
        
        
        
    



    













