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
    Reachability games solver. This function computes Att_j^g(U), the attractor for player j of target set U over the
    game g. That attractor is the winning region of player j for the reachability game associated to the attractor. The
    rest of the nodes are part of the winning region of player j bar (player j's opponent). Winning regions and
    strategies are computed and returned by the algorithm. The winning regions and strategies are return as two tuples
    to ressemble pseudo-code and facilitate weak and strong parity readability.
    :param g: the game graph.
    :param U: the target set.
    :param j: the player.
    :return: two tuples : (w_j, strat_j), (w_jbar, strat_jbar) where w_j and w_jbar are lists containing nodes of their
    respective winning regions and where strat_j and strat_jbar are dictionaries containing winning strategies.
    """
    out = init_out(g)  # init out
    queue = deque()  # init queue (deque is part of standard library and allows O(1) append() and pop() at either end)
    regions = defaultdict(lambda: -1)  # init marq, better access time than using the player's region list to check if
                                       # node is already in the attractoir
    region_j = []  #winning nodes of j
    region_opponent = []  #winning node of j bar
    strat_j = defaultdict(lambda: -1)  # init strat for player j
    strat_opponent = defaultdict(lambda: -1)  #init strat for player jbar
    opponent = op.opponent(j)  # player j's opponent (j bar)

    # for each node in the target set U
    for node in U:
        queue.append(node)  # add node to the end of the queue
        regions[node] = j  # set its regions to j (node is winning for j because it belongs to the attractor)
        region_j.append(node)
        # if node belongs to j, set an arbitrary strategy for that node (we chose to select first successor)
        if g.get_node_player(node) == j:
            strat_j[node] = g.get_successors(node)[0]

    # while queue is not empty
    while queue:
        s = queue.popleft()  # remove and return node on the left side of the queue (first in, first out)

        # print("considering node "+str(s))
        for sbis in g.get_predecessors(s):
            # print("--considering predecessor " + str(sbis)+" "+str(g.get_node_player(sbis)))
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
                        # print("---- current regions "+str(g.get_regions()))
                        # print("---- current strat "+str(g.get_strategies()))

    # for each node that is not marked we set its region to the opponent and find a successor for the strategy
    for node in g.get_nodes():
        if regions[node] != j:
            regions[node] = opponent
            region_opponent.append(node)
            if g.get_node_player(node) == opponent:
                for successor in g.get_successors(node):
                    if regions[successor] != j:
                        strat_opponent[node] = successor
                        # print("---- current regions " + str(g.get_regions()))
                        # print("---- current strat " + str(g.get_strategies()))
    return (region_j,strat_j), (region_opponent, strat_opponent)
