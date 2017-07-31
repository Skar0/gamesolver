from collections import defaultdict

from solvers import reachability
from tools import operations as ops


def weak_parity_solver(g):

    h = g
    i = ops.max_priority(h) # Maximum priority in h

    W1 = []
    W2 = []
    strategies = defaultdict(lambda: -1)

    # Considering priorities from i to 0 in decreasing order
    for k in range(i, -1, -1):
        current_player = k % 2
        (Ak, Sk), (regions_opponent, strategy_opponent) = reachability.reachability_solver_tuples(h, ops.i_priority_node(h, k), current_player)
        #print "iter "+str(k)+" -- "+str(Ak)+" -- "+str(Sk)
        p = []
        strategies.update(strategy_opponent)
        strategies.update(Sk)

        if current_player == 0:
            W1.extend(Ak)
        else:
            W2.extend(Ak)

        h = h.subgame(regions_opponent)

    return W1, W2, strategies
