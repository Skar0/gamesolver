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
    Returns all node of priority i in game graph g.
    :param g: the game graph.
    :param i: the requested priority.
    :return: a list of nodes of priority i in g.
    """
    nodes = g.nodes  # Nodes from g
    # get all node_id's in node tuple (node_id, (node_player, node_priority)) when node_priority is i
    return [k for k, v in nodes.iteritems() if v[1] == i]


def max_priority(g):
    """
    Returns the maximum priority occuring in game graph g.
    :param g: a game graph.
    :return: the maximum priority in g.
    """
    nodes = g.nodes  # Nodes from g
    # get maximum node tuple (node_id, (node_player, node_priority)) according to its priority, then select its priority
    return max(nodes.iteritems(), key=lambda (k, v): v[1])[1][1]
