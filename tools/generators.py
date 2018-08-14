from random import randint, sample, choice

import copy

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
        g.add_node(i, (1, 2 * i))
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
    Generates a random game with n nodes, priorities chosen between 0 and p and out-degree of nodes between i and o.
    No verification is made regarding whether the input makes sense (out degree larger than the number of nodes in the
    game, etc).
    :param n: number of nodes.
    :param p: number of priorities.
    :param i: min outdegree.
    :param o: max outdegree.
    :return: a random game graph.
    """
    nodes = [x for x in xrange(n)]
    g = Graph()
    for node in range(0, n):
        g.add_node(node, (randint(0, 1), randint(0, p)))
    # Create two partitions, S and T. Initially store all nodes in S.
    S, T = set(nodes), set()

    # Randomly select a first node, and place it in T.
    node_s = sample(S, 1).pop()
    S.remove(node_s)
    T.add(node_s)

    # Create a random connected graph.
    while S:
        # Select random node from S, and another in T.
        node_s, node_t = sample(S, 1).pop(), sample(T, 1).pop()
        # Create an edge between the nodes, and move the node from S to T.
        g.add_predecessor(node_t, node_s)
        g.add_successor(node_s, node_t)
        S.remove(node_s)
        T.add(node_s)

    for node in range(0, n):
        num = randint(i, o)
        edges_added = 0
        while edges_added < num:
            to = choice(nodes)
            if not (to in g.get_successors(node)):
                g.add_successor(node, to)
                g.add_predecessor(to, node)
                edges_added+=1
    return g

def random_generalized(n, k, p, i, o):
    """
    Generates a random game with n nodes, k priority functions, priorities chosen between 0 and p and out-degree of
    nodes between i and o. No verification is made regarding whether the input makes sense (out degree larger than
    the number of nodes in the game, etc).
    :param n: number of nodes.
    :param k: number of priority functions.
    :param p: number of priorities.
    :param i: min outdegree.
    :param o: max outdegree.
    :return: a random game graph.
    """
    nodes = [x for x in xrange(n)]
    g = Graph()
    for node in range(0, n):
        playerpriorities = [randint(0, 1)] # Choose a player
        for prio in range(0, k):
            playerpriorities.append(randint(0, p))
        g.add_node(node, tuple(playerpriorities))
    # Create two partitions, S and T. Initially store all nodes in S.
    S, T = set(nodes), set()

    # Randomly select a first node, and place it in T.
    node_s = sample(S, 1).pop()
    S.remove(node_s)
    T.add(node_s)

    # Create a random connected graph.
    while S:
        # Select random node from S, and another in T.
        node_s, node_t = sample(S, 1).pop(), sample(T, 1).pop()
        # Create an edge between the nodes, and move the node from S to T.
        g.add_predecessor(node_t, node_s)
        g.add_successor(node_s, node_t)
        S.remove(node_s)
        T.add(node_s)

    for node in range(0, n):
        num = randint(i, o)
        edges_added = 0
        while edges_added < num:
            to = choice(nodes)
            if not (to in g.get_successors(node)):
                g.add_successor(node, to)
                g.add_predecessor(to, node)
                edges_added+=1
    return g

def ladder(n):
    """
    Ladder game graphs as described in PGSolver.
    :param n: parameter of the ladder (2n nodes).
    :return: a ladder game graph.
    """
    g = Graph()
    for node in range(0, 2*n):
        g.add_node(node, (node%2, node%2))
    for v in range(0, 2 * n):
        for w in range(0, 2 * n):
            if (v+1)%(2*n) == w%(2*n) or (v+2)%(2*n) == w%(2*n):
                g.add_successor(v, w)
                g.add_predecessor(w, v)
    return g

def multiple_priorities(g,n):
    """
    Takes a parity game graph and returns a generalized parity game graph which corresponds exactly to
    the same game graph, with every priority function being the same as the one in the parity game graph.
    :param g: a parity game graph.
    :param n: the number of priority functions required in the generalized game.
    :return: a generalized parity game graph.
    """
    new = copy.deepcopy(g)
    for node in new.get_nodes():
        prev = new.nodes[node] # tuple (player, priority)
        new.nodes[node] = tuple([prev[0]]+n*[prev[1]])
    return new

def opposite_priorities(g):
    """
    Takes a parity game graph and returns a generalized parity game graph which corresponds exactly to
    the same game graph except there are two priority function. The first one is the same as in g and the
    second one is the complemented function.
    :param g: a parity game graph.
    :return: a generalized parity game graph.
    """
    new = copy.deepcopy(g)
    for node in new.get_nodes():
        prev = new.nodes[node] # tuple (player, priority)
        new.nodes[node] = tuple([prev[0]]+[prev[1]]+[prev[1]+1])
    return new