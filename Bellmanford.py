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
        node = prev[node]
    path.append(node) 
    path.reverse()
    return path

def bellman_ford(graph, source,sink):
    d, p = initialize(graph, source)
    for i in range(len(graph)-1): #Run this until is converges
        for u in graph:
            for v in graph[u]: #For each neighbour of u
                relax(u, v, graph, d, p) #Lets relax it

    # Step 3: check for negative-weight cycles
    # for u in graph:
    #     for v in graph[u]:
    #         assert d[v] <= d[u] + graph[u][v]['weight']

    return d, backtrace(p,source,sink)