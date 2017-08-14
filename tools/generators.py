from random import randint

from graph import Graph

"""
This module contains a series of functions allowing to generate specific game graphs.
"""


def complete_graph(n):
    """
    Generates a complete graph (with self loops) containing n nodes. Nodes are numbered 1 to n.
    All nodes belong to player 1. All priorities are 0. This is used as a worst case for reachability games.
    This version is optimised to take less time by using the range() function.
    :param n: number of nodes.
    :return: a Graph object representing the complete graph.
    """
    g = Graph()  # creates empty graph

    # creates n nodes belonging to player 1 with all nodes as successors and predecessors
    for i in range(1, n + 1):
        g.add_node(i, (1, 0))
        g.successors[i] = range(1, n + 1)
        g.predecessors[i] = range(1, n + 1)

    return g


def complete_graph_weakparity(n):
    """
    Generates a complete graph (with self loops) containing n nodes. Nodes are numbered 1 to n.
    All nodes belong to player 0. All priorities are 0 except for node 1 which has priority 2.
    This is used as a worst case for weak parity games where we compute an attractor with the worst case for the
    reachability algorithm.
    :param n: number of nodes.
    :return: a Graph object representing the complete graph.
    """
    g = Graph()  # create empty graph

    for i in range(1, n + 1):
        g.add_node(i, (0, 0))
        g.successors[i] = range(1, n + 1)
        g.predecessors[i] = range(1, n + 1)
    g.nodes[1] = (0, 2)
    return g


def weak_parity_worst_case(n):
    """
    Generates a complete graph (with self loops) containing n nodes. Nodes are numbered 1 to n.
    All nodes belong to player 1. Priority of node i is 4*i. All priorities are thus even.
    This is used as a worst case for weak parity games where we will compute n attractors with the reachability
    algorithm and each computation will be a worst case for that algorithm.
    :param n: number of nodes.
    :return: a Graph object representing the complete graph.
    """
    g = Graph()  # create empty graph

    # create n nodes belonging to player 1
    for i in range(1, n + 1):
        g.add_node(i, (1, 4 * i))
        g.successors[i] = range(1, n + 1)
        g.predecessors[i] = range(1, n + 1)

    return g


def reachability_worst_case(n):
    """
    Generates a graph which contains n nodes and (n*(n+1))/2 edges and is built using the following formula.
    Node number 1 has n successors (all nodes in the graph). Node number k has k-1 successors which are nodes numbered
    k-1 to 1. All nodes belong to player 1 and have priority 0. This is used as a worst case for reachability games.
    This version is optimised to take less time by using the range() function.
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


def strong_parity_worst_case(n):
    """
    This is a worst case generator for strong parity games yielding an exponential complexity for the algorithm.
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
    for i in range(1, n + 1):
        g.add_node(i, (1 - (i % 2), 1 - (i % 2)))
        a.append(i)
        g.add_node(n + i, (i % 2, 1 - (i % 2)))
        b.append(n + i)
        g.add_node((2 * n) + i, ((i % 2), (3 * (i - 1)) + 5))
        c.append((2 * n) + i)
        g.add_node((3 * n) + i, (1 - (i % 2), (3 * (i - 1)) + 4))
        d.append((3 * n) + i)
        g.add_node((4 * n) + i, (i % 2, (3 * (i - 1)) + 3))
        e.append((4 * n) + i)

    # adding a and b successors
    for i in range(1, n + 1):
        g.add_successor(a[i], b[i])
        g.add_predecessor(b[i], a[i])

        g.add_successor(a[i], d[i - 1])
        g.add_predecessor(d[i - 1], a[i])

        g.add_successor(b[i], a[i])
        g.add_predecessor(a[i], b[i])

        if i >= 0 and i < len(c):
            g.add_successor(b[i], c[i])
            g.add_predecessor(c[i], b[i])

    # adding c,d,e successors
    for i in range(0, n):
        # c
        g.add_successor(c[i], b[i + 1])
        g.add_predecessor(b[i + 1], c[i])

        g.add_successor(c[i], d[i])
        g.add_predecessor(d[i], c[i])

        # d
        g.add_successor(d[i], e[i])
        g.add_predecessor(e[i], d[i])

        if i - 1 >= 0 and i - 1 < len(d):
            g.add_successor(d[i], d[i - 1])
            g.add_predecessor(d[i - 1], d[i])

        if i + 1 >= 0 and i + 1 < len(d):
            g.add_successor(d[i], d[i + 1])
            g.add_predecessor(d[i + 1], d[i])

        # e
        g.add_successor(e[i], b[i + 1])
        g.add_predecessor(b[i + 1], e[i])

        g.add_successor(e[i], d[i])
        g.add_predecessor(d[i], e[i])

    return g


def random(n, p, i, o):
    """
    This function is unfinished.
    Generates a random game with n nodes, priorities chosen between 0 and p and out-degree of nodes between i and o.
    No verification is made regarding whether the input makes sense (out degree larger than the number of nodes in the
    game, etc).
    :param n: number of nodes.
    :param p: number of priorities.
    :param i: min outdegree.
    :param o: max outdegree.
    :return: a random game.
    """
    g = Graph()
    for node in range(0, n):
        g.add_node(node, (randint(0, 1), randint(0, p)))
        notself = False
        for h in range(i, o + 1):
            found = False
            while not found:
                succ = randint(0, n)
                if not notself:
                    if succ != node:
                        g.add_successor(node, succ)
                        g.add_predecessor(succ, node)
                        found = True
                        notself = True
                if notself and succ not in g.successors[node]:
                    g.add_successor(node, succ)
                    g.add_predecessor(succ, node)
                    found = True
    return g
