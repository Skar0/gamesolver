from collections import defaultdict

from solvers import reachability as rs
from tools import operations as ops


def weak_parity_solver(g):

    h = g
    i = ops.max_priority(h) # Maximum priority in h

    W1 = []
    W2 = []
    strat1 = defaultdict(lambda: -1)
    strat2 = defaultdict(lambda: -1)

    # Considering priorities from i to 0 in decreasing order
    for k in range(i, -1, -1):
        current_player = k % 2
        (Ak, Sk), (regions_opponent, strategy_opponent) = rs.reachability_solver_tuples(h, ops.i_priority_node(h, k), current_player)
        #print "iter "+str(k)+" -- "+str(Ak)+" -- "+str(Sk)

        if current_player == 0:
            W1.extend(Ak)
            strat1.update(Sk)
            strat2.update(strategy_opponent)

        else:
            W2.extend(Ak)
            strat2.update(Sk)
            strat1.update(strategy_opponent)

        h = h.subgame(regions_opponent)
        
    return (W1, strat1), (W2, strat2)
