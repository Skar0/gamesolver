"""
This module contains general-purpose functions used in several of our algorithms.
"""


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


def max_priority(g):
    """
    Returns the maximum priority occurring in game graph g.
    :param g: a game graph.
    :return: the maximum priority in g.
    """
    nodes = g.nodes  # Nodes from g
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
