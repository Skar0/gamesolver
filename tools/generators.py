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
    """
    This is a worst case generator for strong parity game yielding an exponential complexity for the algorithm.
    The construction of this type of graph, which contains n*5 nodes can be found in Oliver Friedmann's paper "Recursive
    Algorithm for Parity Games requires Exponential Time".
    :param n: the number for the generation of the graph (yields n*5 nodes).
    :return: a worst case graph for the recursive algorithm.
    """
    g = Graph()
    # We use a list to store each of the 5 types of nodes. Each node has a unique integer value, but for increased
    # readability and understandability, we work with the nodes using their list and the position they are in their list
    # For a and b, first element is a placeholder so indexes start at 1
    a = [">"]
    b = [">"]
    c = []
    d = []
    e = []

    # creating nodes, their integer value is from 1 to 5*n
    # we adapted the code (modulos and parities for c,d,e) because we count from 1 to n in the loop
    for i in range(1,n+1):
        g.add_node(i, (1-(i%2), 1-(i%2)))
        a.append(i)
        g.add_node(n+i, (i%2, 1-(i%2)))
        b.append(n+i)
        g.add_node((2*n)+i, ((i%2), (3*(i-1))+5))
        c.append((2*n)+i)
        g.add_node((3*n)+i, (1-(i%2), (3*(i-1))+4))
        d.append((3*n)+i)
        g.add_node((4*n)+i, (i%2, (3*(i-1))+3))
        e.append((4*n)+i)

    # adding a and b successors
    for i in range(1,n+1):
        g.add_successor(a[i], b[i])
        g.add_predecessor(b[i], a[i])

        g.add_successor(a[i], d[i-1])
        g.add_predecessor(d[i-1], a[i])

        g.add_successor(b[i], a[i])
        g.add_predecessor(a[i], b[i])

        if i >= 0 and i < len(c):
            g.add_successor(b[i], c[i])
            g.add_predecessor(c[i], b[i])

    # adding c,d,e successors
    for i in range(0, n):
        #c
        g.add_successor(c[i], b[i+1])
        g.add_predecessor(b[i+1], c[i])

        g.add_successor(c[i], d[i])
        g.add_predecessor(d[i], c[i])

        #d
        g.add_successor(d[i], e[i])
        g.add_predecessor(e[i], d[i])

        if i-1 >= 0 and i-1 < len(d):
            g.add_successor(d[i], d[i-1])
            g.add_predecessor(d[i-1], d[i])

        if i+1 >= 0 and i+1 < len(d):
            g.add_successor(d[i], d[i+1])
            g.add_predecessor(d[i+1], d[i])

        #e
        g.add_successor(e[i], b[i + 1])
        g.add_predecessor(b[i + 1], e[i])

        g.add_successor(e[i], d[i])
        g.add_predecessor(d[i], e[i])

    return g








