# coding=utf-8
from collections import defaultdict, deque
from tools import operations as op


def init_out(g):
    """
    Computes the number of outgoing edges for each node in the graph g.
    :param g: the graph g.
    :return: a dictionary where keys are nodes and values are the number of outgoing edges of that node.
    """
    out = defaultdict(int)

    for node in g.get_nodes():
        out[node] = len(g.get_successors(node))

    return out


def reachability_solver(g, U, j):
    """
    Reachability games solver. This function computes Att_j^g(U), the attractor for player j of target set U in the
    game g. That attractor is the winning region of player j who has the reachability objective in the game. The
    rest of the nodes are part of the winning region of player jbar (player j's opponent). Winning regions and
    strategies are computed and returned by the algorithm. The winning regions and strategies are return as two tuples
    to resemble pseudo-code and facilitate weak and strong parity solvers readability.
    :param g: the game graph.
    :param U: the target set.
    :param j: the player with the reachability objective.
    :return: two tuples : (w_j, strat_j), (w_jbar, strat_jbar) where w_j and w_jbar are lists containing nodes of their
    respective winning regions and where strat_j and strat_jbar are dictionaries containing winning strategies.
    """
    out = init_out(g)  # init out
    queue = deque()  # init queue (deque is part of standard library and allows O(1) append() and pop() at either end)
    # this dictionary is used to know if a node belongs to a winning region without
    # iterating over both winning regions lists (we can check in O(1) in average)
    regions = defaultdict(lambda: -1)
    region_j = []  # winning region of j
    region_opponent = []  # winning region of j bar
    strat_j = defaultdict(lambda: -1)  # init strat for player j
    strat_opponent = defaultdict(lambda: -1)  # init strat for player jbar
    opponent = op.opponent(j)  # player j's opponent (jbar)

    # for each node in the target set U
    for node in U:
        queue.append(node)  # add node to the end of the queue
        regions[node] = j  # set its regions to j (node is winning for j because reachability objective is satisfied)
        region_j.append(node)  # add the node to the winning region list of j
        # if node belongs to j, set an arbitrary strategy for that node (we chose to select first successor)
        if g.get_node_player(node) == j:
            strat_j[node] = g.get_successors(node)[0]

    # while queue is not empty
    while queue:
        s = queue.popleft()  # remove and return node on the left side of the queue (first in, first out)

        # iterating over the predecessors of node s
        for sbis in g.get_predecessors(s):
            if regions[sbis] == -1:  # if sbis is not yet visited, its region is -1 by default
                if g.get_node_player(sbis) == j:
                    # belongs to j, set regions and strategy accordingly
                    queue.append(sbis)
                    regions[sbis] = j
                    region_j.append(sbis)
                    strat_j[sbis] = s

                elif g.get_node_player(sbis) == opponent:
                    # belongs to j bar, decrement out. If out is 0, set the region accordingly
                    out[sbis] -= 1
                    if out[sbis] == 0:
                        queue.append(sbis)
                        regions[sbis] = j
                        region_j.append(sbis)

    # for each node that is not marked we set its region to the opponent and find a successor for the strategy
    for node in g.get_nodes():
        if regions[node] != j:
            regions[node] = opponent
            region_opponent.append(node)
            if g.get_node_player(node) == opponent:
                for successor in g.get_successors(node):
                    if regions[successor] != j:
                        strat_opponent[node] = successor

    return (region_j, strat_j), (region_opponent, strat_opponent)


def init_out_non_removed(g, removed):
    """
    Computes the number of outgoing edges for each node that hasn't been removed in the graph g.
    :param removed: the removed nodes from g.
    :param g: the graph g.
    :return: a dictionary where keys are nodes and values are the number of outgoing edges of that node.
    """
    out = defaultdict(int)

    for node in g.get_nodes():
        if not removed[node]:
            out[node] = len(filter(lambda x: not removed[x], g.get_successors(node)))
    return out


def reachability_solver_non_removed(g, U, j, removed):
    """
    Reachability games solver. Uses a list of removed nodes instead of creation of subgames. This function computes
    Att_j^g(U), the attractor for player j of target set U in the game g. That attractor is the winning region of player
    j who has the reachability objective in the game. The rest of the nodes are part of the winning region of player
    jbar (player j's opponent). Winning regions and strategies are computed and returned by the algorithm. The winning
    regions and strategies are return as two tuples to resemble pseudo-code and facilitate weak and strong parity
    solvers readability.
    :param removed: the removed nodes from g.
    :param g: the game graph.
    :param U: the target set.
    :param j: the player with the reachability objective.
    :return: two tuples : (w_j, strat_j), (w_jbar, strat_jbar) where w_j and w_jbar are lists containing nodes of their
    respective winning regions and where strat_j and strat_jbar are dictionaries containing winning strategies.
    """
    out = init_out_non_removed(g, removed)  # init out
    queue = deque()  # init queue (deque is part of standard library and allows O(1) append() and pop() at either end)
    # this dictionary is used to know if a node belongs to a winning region without
    # iterating over both winning regions lists (we can check in O(1) in average)
    regions = defaultdict(lambda: -1)
    region_j = []  # winning region of j
    region_opponent = []  # winning region of j bar
    strat_j = defaultdict(lambda: -1)  # init strat for player j
    strat_opponent = defaultdict(lambda: -1)  # init strat for player jbar
    opponent = op.opponent(j)  # player j's opponent (jbar)

    # for each node in the target set U
    for node in U:
        queue.append(node)  # add node to the end of the queue
        regions[node] = j  # set its regions to j (node is winning for j because reachability objective is satisfied)
        region_j.append(node)  # add the node to the winning region list of j
        # if node belongs to j, set an arbitrary strategy for that node (we chose to select first successor)
        if g.get_node_player(node) == j:
            strat_j[node] = filter(lambda x: not removed[x], g.get_successors(node))[0]

    # while queue is not empty
    while queue:
        s = queue.popleft()  # remove and return node on the left side of the queue (first in, first out)

        # iterating over the predecessors of node s
        for sbis in g.get_predecessors(s):
            if not removed[sbis]:
                if regions[sbis] == -1:  # if sbis is not yet visited, its region is -1 by default
                    if g.get_node_player(sbis) == j:
                        # belongs to j, set regions and strategy accordingly
                        queue.append(sbis)
                        regions[sbis] = j
                        region_j.append(sbis)
                        strat_j[sbis] = s

                    elif g.get_node_player(sbis) == opponent:
                        # belongs to j bar, decrement out. If out is 0, set the region accordingly
                        out[sbis] -= 1
                        if out[sbis] == 0:
                            queue.append(sbis)
                            regions[sbis] = j
                            region_j.append(sbis)

    # for each node that is not marked we set its region to the opponent and find a successor for the strategy
    for node in g.get_nodes():
        if not removed[node]:
            if regions[node] != j:
                regions[node] = opponent
                region_opponent.append(node)
                if g.get_node_player(node) == opponent:
                    for successor in g.get_successors(node):
                        if regions[successor] != j and not removed[successor]:
                            strat_opponent[node] = successor

    return (region_j, strat_j), (region_opponent, strat_opponent)


def attractor(g, U, j):
    """
    Computes the attractor for player j of the set U in g. Does not create any strategy and only returns the set that
    corresponds to the attractor.
    :param g: the game graph.
    :param U: the target set.
    :param j: the player for which we compute the attractor.
    :return: W the set of nodes corresponding to the attractor.
    """
    out = init_out(g)  # init out
    queue = deque()  # init queue (deque is part of standard library and allows O(1) append() and pop() at either end)
    # this dictionary is used to know if a node belongs to a winning region without
    # iterating over both winning regions lists (we can check in O(1) in average)
    regions = defaultdict(lambda: -1)
    W = []  # the attractor
    opponent = op.opponent(j)  # player j's opponent

    # for each node in the target set U
    for node in U:
        queue.append(node)  # add node to the end of the queue
        regions[node] = j  # set its regions to j (node is winning for j because reachability objective is satisfied)
        W.append(node)  # add the node to the winning region list of j

    # while queue is not empty
    while queue:
        s = queue.popleft()  # remove and return node on the left side of the queue (first in, first out)

        # iterating over the predecessors of node s
        for sbis in g.get_predecessors(s):
            if regions[sbis] == -1:  # if sbis is not yet visited, its region is -1 by default
                if g.get_node_player(sbis) == j:
                    # belongs to j, set regions and strategy accordingly
                    queue.append(sbis)
                    regions[sbis] = j
                    W.append(sbis)

                elif g.get_node_player(sbis) == opponent:
                    # belongs to j bar, decrement out. If out is 0, set the region accordingly
                    out[sbis] -= 1
                    if out[sbis] == 0:
                        queue.append(sbis)
                        regions[sbis] = j
                        W.append(sbis)

    Wbis = []
    for node in g.get_nodes():
            if regions[node] != j:
                Wbis.append(node)
    return W, Wbis
