"""
This module contains general-purpose functions used in several of our algorithms.
"""
import ctypes
import collections

from antichains.library_linker import createGraph_c, addEdge_c, displayGraph_c


def opponent(j):
    """
    Returns the opponent of player j.
    :param j: the player (0 or 1).
    :return: its opponent.
    """
    if j == 1:
        return 0
    else:
        return 1


def i_priority_node(g, i):
    """
    Returns all nodes of priority i in game graph g.
    :param g: the game graph.
    :param i: the requested priority.
    :return: a list of nodes of priority i in g.
    """
    nodes = g.nodes  # Nodes from g
    # get all node indexes in node tuple (index, (node_player, node_priority)) when node_priority is i
    return [k for k, v in nodes.iteritems() if v[1] == i]


def i_priority_node_function_j(g, i, j):
    """
    :param g: the game graph.
    :param i: the requested priority.
    :param j: the priority function.
    :return: all nodes of priority i in game graph g according to priority function j.
    """
    nodes = g.nodes  # Nodes from g
    # get all node indexes in node tuple (index, (node_player, node_priority)) when node_priority is i
    return [k for k, v in nodes.iteritems() if v[j] == i]


def max_priority(g):
    """
    Returns the maximum priority occurring in game graph g.
    :param g: a game graph.
    :return: the maximum priority in g.
    """
    nodes = g.nodes  # Nodes from g
    # get maximum node tuple (index, (node_player, node_priority)) according to its priority, then select its priority
    return max(nodes.iteritems(), key=lambda (k, v): v[1])[1][1]


def i_priority_node_non_removed(g, i, removed):
    """
    Returns all nodes of priority i in game graph g considering the removed nodes.
    :param removed: the removed nodes.
    :param g: the game graph.
    :param i: the requested priority.
    :return: a list of nodes of priority i in g except for the removed nodes.
    """
    nodes = {k: v for k, v in g.nodes.iteritems() if not removed[k]}
    # get all node indexes in node tuple (index, (node_player, node_priority)) when node_priority is i
    return [k for k, v in nodes.iteritems() if v[1] == i]


def max_priority_non_removed(g, removed):
    """
    Returns the maximum priority occurring in game graph g, considering the removed nodes.
    :param removed: the removed nodes.
    :param g: a game graph.
    :return: the maximum priority in g except for the removed nodes.
    """
    nodes = {k: v for k, v in g.nodes.iteritems() if not removed[k]}
    # get maximum node tuple (index, (node_player, node_priority)) according to its priority, then select its priority
    return max(nodes.iteritems(), key=lambda (k, v): v[1])[1][1]


def update_strategy(strat1, strat2):
    """
    Updates strategy 1 by adding key/value pairs of strategy 2.
    :param strat1: Old strategy.
    :param strat2: Strategy to add.
    :return: A new strategy which merges strategies 1 and 2 (2 overwrites 1 in case of duplicate keys)
    """
    new_strat = strat1.copy()
    new_strat.update(strat2)
    return new_strat


def print_solution(solution, player):
    """
    Formats the solution of a game and prints it in the command line.
    :param solution: if player is 0, expected solution format is (W_0, sigma_0),(W_1, sigma_1). If player is 1, invert.
    :param player: the player corresponding to the first tuple in solution.
    :return: prints formatted solution
    """
    if player == 0:
        (W_0, sigma_0), (W_1, sigma_1) = solution
    else:
        (W_1, sigma_1), (W_0, sigma_0) = solution

    print "Winning region of player 0 : " + str(W_0)
    print "Winning strategy of player 0 :"
    for key, value in sigma_0.iteritems():
        print " " + str(key) + " -> " + str(value)
    print " "
    print "Winning region of player 1 : " + str(W_1)
    print "Winning strategy of player 1 :"
    for key, value in sigma_1.iteritems():
        print " " + str(key) + " -> " + str(value)

def print_winning_regions(W1, W2):
    """
    Formats the solution of a game and prints it in the command line.
    :param W1: winning region of player 0 (1)
    :param W2: winning region of player 1 (2)
    :return: prints formatted solution
    """
    print "Winning region of player 0 : " + str(W1)+"\n"
    print "Winning region of player 1 : " + str(W2)+"\n"

def transform_graph_into_c(g):
    """
    Transforms a Graph object to a graph structure in c using the c library.
    This function assumes that nodes are numbered from 1 to n
    :param g: a game graph.
    :return: a game graph in c format and the number of nodes in that graph.
    """
    # nbr of nodes in the graph is needed by the c structure
    nbr_nodes = len(g.get_nodes())
    # the c structure needs players (0 for player 0 and 1 for player 1) and priorities as arrays
    priorities = [0]*nbr_nodes
    players = [0]*nbr_nodes

    # need to create every node before creating the edges. /!\ nodes are numbered from 0 to nbr_nodes-1 in the C struct
    for node in g.get_nodes():
        priorities[node-1] = g.nodes[node][1]
        players[node-1] = g.nodes[node][0]

    # creating the c graph
    dir_graph = createGraph_c(nbr_nodes,(ctypes.c_int * len(priorities))(*priorities),(ctypes.c_int * len(players))(*players))

    # adding every edge
    for node in g.get_nodes():
        for succ in g.get_successors(node):
            addEdge_c(dir_graph, node-1, succ-1)

    return dir_graph, nbr_nodes

def transform_graph_into_c_spec(g):
    """
    Transforms a Graph object to a graph structure in c using the c library.
    This function assumes that nodes are numbered from 0 to n-1
    :param g: a game graph.
    :return: a game graph in c format and the number of nodes in that graph.
    """
    # nbr of nodes in the graph is needed by the c structure
    nbr_nodes = len(g.get_nodes())
    # the c structure needs players (0 for player 0 and 1 for player 1) and priorities
    priorities = [0]*nbr_nodes
    players = [0]*nbr_nodes

    # need to create every node before creating the edges.
    # here nodes are already numbered from 0
    for node in g.get_nodes():
        priorities[node] = g.nodes[node][1]
        players[node] = g.nodes[node][0]

    # creating the c graph
    dir_graph = createGraph_c(nbr_nodes,(ctypes.c_int * len(priorities))(*priorities),(ctypes.c_int * len(players))(*players))

    # adding every edge
    for node in g.get_nodes():
        for succ in g.get_successors(node):
            addEdge_c(dir_graph, node, succ)

    return dir_graph, nbr_nodes

def are_lists_equal(list1, list2):
    """
    Checks whether two lists are equal (contain exactly the same elements).
    Using Counter data structure allows duplicates to be considered i.e. [1, 1, 2]  != [1, 2].
    :param list1: the first list.
    :param list2: the second list.
    :return: true if the two lists contain exactly the same elements.
    """
    return collections.Counter(list1) == collections.Counter(list2)