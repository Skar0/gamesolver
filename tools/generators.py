from graph import Graph

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

def complete_graph_optimised(n):
    """
    Generate a complete graph (with self loops) containing n nodes. Nodes are numbered 1 to n.
    All nodes belong to player 1 except node 1 which belongs to player 0. All priorities are 0.
    This is used as a worst case for reachability games. This version is optimised to take less time
    by using the range() function.
    :param n: number of nodes.
    :return: a Graph object representing the complete graph.
    """
    g = Graph()  # create empty graph

    # create n-1 nodes belonging to player 1
    for i in range(2, n + 1):
        g.add_node(i, (1, 0))
        g.successors[i] = range(1,n+1)
        g.predecessors[i] = range(1,n+1)

    # same for node 1 which belongs to player 0
    g.add_node(1, (0, 0))
    for j in range(1, n + 1):
        g.add_successor(1, j)
        g.add_predecessor(j, 1)

    return g

def complete_graph_oneplayer_parity(n):
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
        g.successors[i] = range(1,n+1)
        g.predecessors[i] = range(1,n+1)

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

def reachability_worstcase_chain_optimised(n):
    """
    Generate a graph containing n nodes. Nodes are numbered 1 to n. The graph contains (n*(n+1))/2 edges and is built
    using the following formula. Node number 1 has n successors (all nodes in the graph). Node number k has k-1
    successors which are nodes numbered k-1 to 1. All nodes belong to player 1 and have priority 0. This is used as a
    worst case for reachability games. This version is optimised to take less time by using the range() function.
    :param n: number of nodes.
    :return: a Graph object of the described form.
    """
    g = Graph()
    # create n-1 nodes numbered from n to 2
    for k in range(n, 1, -1):
        g.add_node(k, (1, 0))
        # add successors to node k (numbered k-1 to 1)
        g.successors[k] = range(k - 1, 0, -1)
        g.predecessors[k] = range(k + 1, n + 1)
        g.add_predecessor(1, k)
    # same for node 1 which has all nodes as successors
    g.add_node(1, (1, 0))
    for i in range(n, 0, -1):
        g.add_successor(1, i)
        g.add_predecessor(i, 1)

    return g

def reachability_worstcase_chain2_parity_order(n):
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
        g.add_node(k, (1, (n+1)-k))
        # add successors to node k (numbered k-1 to 1)
        g.successors[k] = range(k - 1, 0, -1)
        g.predecessors[k] = range(n, k-1,-1)

    # same for node 1 which has all nodes as successors
    g.add_node(1, (0, n))
    for i in range(n, 0, -1):
        g.add_successor(1, i)
        g.add_predecessor(i, 1)

    return g

def reachability_worstcase_chain2_parity_unorder(n):
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
        g.add_node(k, (1, k))
        # add successors to node k (numbered k-1 to 1)
        g.successors[k] = range(k - 1, 0, -1)
        g.predecessors[k] = range(k+1,n+1)
        g.add_predecessor(1,k)


    # same for node 1 which has all nodes as successors
    g.add_node(1, (0, 1))
    for i in range(n, 0, -1):
        g.add_successor(1, i)
        g.add_predecessor(i, 1)

    return g

def parity_worstcase_chain_unordered(n):
    """
    Generate a graph containing n nodes. Nodes are numbered 1 to n. The graph contains (n*(n+1))/2 edges and is built
    using the following formula. Node number 1 has n successors (all nodes in the graph). Node number k has k-1
    successors which are nodes numbered k-1 to 1. All nodes belong to player 1 and have priority 0. This is used as a
    worst case for reachability games. This version is optimised to take less time by using the range() function.
    :param n: number of nodes.
    :return: a Graph object of the described form.
    """
    g = Graph()
    # create n-1 nodes numbered from n to 2
    for k in range(n, 1, -1):
        g.add_node(k, (1, (n+1)-k))
        # add successors to node k (numbered k-1 to 1)
        g.successors[k] = range(k - 1, 0, -1)
        g.predecessors[k] = range(k + 1, n + 1)
        g.add_predecessor(1, k)
    # same for node 1 which has all nodes as successors
    g.add_node(1, (1, n))
    for i in range(n, 0, -1):
        g.add_successor(1, i)
        g.add_predecessor(i, 1)

    return g

def strongParity_worst_case(n):
    g = Graph()
    ai = [">"]
    bi = [">"]
    ci = []
    di = []
    ei = []
    # creating nodes (ok)
    for i in range(1,n+1):
        g.add_node(i, (1-(i%2), 1-(i%2)))
        ai.append(i)
        g.add_node(n+i, (i%2, 1-(i%2)))
        bi.append(n+i)
        g.add_node((2*n)+i, ((i%2), (3*(i-1))+5))
        ci.append((2*n)+i)
        g.add_node((3*n)+i, (1-(i%2), (3*(i-1))+4))
        di.append((3*n)+i)
        g.add_node((4*n)+i, (i%2, (3*(i-1))+3))
        ei.append((4*n)+i)

    print ai
    print bi
    print ci
    print di
    print ei

    for i in range(1,n+1):
        g.add_successor(ai[i], bi[i])
        g.add_predecessor(bi[i], ai[i])

        g.add_successor(ai[i], di[i-1])
        g.add_predecessor(di[i-1], ai[i])

        g.add_successor(bi[i], ai[i])
        g.add_predecessor(ai[i], bi[i])

        if i >= 0 and i < len(ci):
            g.add_successor(bi[i], ci[i])
            g.add_predecessor(ci[i], bi[i])
        """

        g.add_successor(n+i, i)
        g.add_predecessor(i, n+i)

        if g.nodes[(2*n)+i-1] != -1:
            g.add_successor(n+i,(2*n)+i-1 )
            g.add_predecessor((2*n)+i-1, n+i)

        # ci
        g.add_successor((2*n)+i, n+i)
        g.add_predecessor(n+i, (2*n)+i)

        g.add_successor((2 * n) + i, (3*n)+i-1)
        g.add_predecessor((3*n)+i-1, (2 * n) + i)

        #di
        g.add_successor((3*n)+i, (4*n)+i)
        g.add_predecessor((4*n)+i, (3*n)+i)

        if g.nodes[(3*n)+i-2] != -1:
            g.add_successor((3*n)+i,(3*n)+i-2)
            g.add_predecessor((3*n)+i-2, (3*n)+i)
        """
    return g

print strongParity_worst_case(3)












