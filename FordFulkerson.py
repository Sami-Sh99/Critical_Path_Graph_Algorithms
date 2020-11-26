
def bfs(graph, source, sink):
    """ Find shortest path between source and sink if path exists.
    :param graph:
    :param source:
    :param sink:
    :return:
    """
    queue, visited = [(source, [source])], [source]
    while queue:
        u, path = queue.pop(0)
        edge_nodes = set(graph[u].keys()) - set(path)
        for v in edge_nodes:
            if v in visited:
                continue
            visited.append(v)
            if not graph.has_edge(u, v):
                continue
            elif v == sink:
                return path + [v]
            else:
                queue.append((v, path + [v]))

def augment_flow(graph, flow_path):
    """ Augment flow of the graph
    :param graph:
    :param flow_path: (list) eg [('source', 'CA'), ('CA', 'AZ'), ('AZ', 'sink')]
    :return:
        1. get the bottleneck capacity
        2. update the residual capacities of forward and back edges
        3. return graph with flow augmented.
    """
    bottleneck = min([graph[u][v]['weight'] for u, v in flow_path])
    for u, v in flow_path:
        updated_capacity = graph[u][v]['weight'] - bottleneck
        if updated_capacity:
            graph[u][v]['weight'] = updated_capacity
        else:
            graph.remove_edge(u, v)
        if not graph.has_edge(v, u):
            graph.add_edge(v, u)
            graph[v][u]['weight'] = 0
        graph[v][u]['weight'] += bottleneck
    return graph

def reduce_graph(graph):
    """ Transform a bipartite graph into a directed flow network with source and sink.
    :param graph: (networkx.classes.digraph.DiGraph)
    :return:
        bipartite G -> network flow
        R(G) -> G'
    """
    G = graph.copy()
    all_nodes = G.nodes()
    G.add_node('source')
    G.add_node('sink')
    for n in all_nodes:
        demand = G.node[n]['demand']
        if demand < 0:
            G.add_edge('source', n, capacity=-demand)
        else:
            G.add_edge(n, 'sink', capacity=demand)
    return G


def ford_fulkerson(graph, source, sink):
    """ Run the Ford Fulkerson method using BFS for shortest path
    :param graph:
    :param source:
    :param sink:
    :return:
        Once BFS can no longer find any shortest direct path between source and sink,
        return the residual graph with the updated capacities.
    """
    path = bfs(graph, source, sink)
    while path:
        flow_path = list(zip(path[:-1], path[1:]))
        graph = augment_flow(graph, flow_path)
        path = bfs(graph, source, sink)
    return  list(dict.fromkeys([i for sub in  flow_path for i in sub]))
