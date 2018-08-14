"""
This module contains functions used to optimize the run time of several of our algorithms.
"""
import copy


def compress_priorities(g):
    """
    :param g: a game arena
    :return: the game arena g in which the priorities have been compressed.
    """
    g_copy = copy.deepcopy(g)
    nodes = g_copy.get_nodes_descriptors()  # Nodes from g
    priorities = sorted(nodes.iteritems(), key=lambda x:x[1][1]) # sorts nodes per priority
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