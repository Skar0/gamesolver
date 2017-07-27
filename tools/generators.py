from graph import Graph


def reachability_worstcase_generator(n):
    g = Graph()  # create empty graph
    for i in range(0, n):
        g.add_node(i, (0, 0))
        g.add_successor(i, i)
        g.add_predecessor(i, i)
        if (i != n - 1):
            g.add_successor(i, i + 1)
            g.add_predecessor(i + 1, i)
    return g


def complete_graph(n):
    """
    Generate a complete graph (with self loops) containing n nodes. Nodes are numbered 1 to n.
    All nodes belong to player 1 except node 1 which belongs to player 0. All priorities are 0.
    This is used as a worst case for reachability games.
    :param n: number of nodes.
    :return: a Graph object representing the complete graph.
    """
    g = Graph()  # create empty graph

    # create n-1 nodes belonging to player 1
    for i in range(2, n + 1):
        g.add_node(i, (1, 0))
        # adding all successors to node i
        for j in range(1, n + 1):
            g.add_successor(i, j)
            g.add_predecessor(j, i)

    # same for node 1 which belongs to player 0
    g.add_node(1, (0, 0))
    for j in range(1, n + 1):
        g.add_successor(1, j)
        g.add_predecessor(j, 1)

    return g


def reachability_worstcase_chain(n):
    """
    Generate a graph containing n nodes. Nodes are numbered 1 to n. The graph contains (n*(n+1))/2 edges and is built
    using the following formula. Node number 1 has n successors (all nodes in the graph). Node number k has k-1
    successors which are nodes numbered k-1 to 1. All nodes belong to player 1 and have priority 0. This is used as a
    worst case for reachability games.
    :param n: number of nodes.
    :return: a Graph object of the described form.
    """
    g = Graph()
    # create n-1 nodes numbered from n to 2
    for k in range(n, 1, -1):
        g.add_node(k, (1, 0))
        # add successors to node k (numbered k-1 to 1)
        for j in range(k - 1, 0, -1):
            g.add_successor(k, j)
            g.add_predecessor(j, k)

    # same for node 1 which has all nodes as successors
    g.add_node(1, (1, 0))
    for i in range(n, 0, -1):
        g.add_successor(1, i)
        g.add_predecessor(i, 1)

    return g
