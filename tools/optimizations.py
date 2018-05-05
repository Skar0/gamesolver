"""
This module contains functions used to optimize the run time of several of our algorithms.
"""
import copy


def compress_priorities(g):
    """
    Returns a.
    :param j: the player (0 or 1).
    :return: its opponent.
    """
    g_copy = copy.deepcopy(g)
    nodes = g_copy.get_nodes_descriptors()  # Nodes from g
    priorities = sorted(nodes.iteritems(), key=lambda x:x[1][1])
    current = priorities[0][1][1]
    if current % 2 == 0:
        start = 0
    else:
        start = 1
    val = start
    for elem in priorities:
        if(elem[1][1] % 2 == start):
            g_copy.nodes[elem[0]] = tuple([elem[1][0], val])
        else:
            val += 1
            start = ((start + 1) %2)
            g_copy.nodes[elem[0]] = tuple([elem[1][0], val])

    return g_copy



#import file_handler as io
#g = io.load_from_file("/home/clement/PycharmProjects/gamesolver/assets/reachability/fig51.txt")

#compress_priorities(g)

""""
    
    # get all node indexes in node tuple (index, (node_player, node_priority)) when node_priority is i
    return [k for k, v in nodes.iteritems() if v[j] == i]


def max_priority(g):
    
    Returns the maximum priority occurring in game graph g.
    :param g: a game graph.
    :return: the maximum priority in g.
    
    nodes = g.nodes  # Nodes from g
    # get maximum node tuple (index, (node_player, node_priority)) according to its priority, then select its priority
    return max(nodes.iteritems(), key=lambda (k, v): v[1])[1][1]

"""