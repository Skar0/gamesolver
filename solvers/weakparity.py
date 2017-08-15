from collections import defaultdict

from solvers import reachability as rs
from tools import operations as ops


def weak_parity_solver(g):
    """
    Weak parity games solver. This is an implementation of the algorithm presented in chapter 4 of the report.
    :param g: the game to solve.
    :return: the solution in the following format : (W_0, sigma_0), (W_1, sigma_1).
    """

    h = g  # the game we work on
    i = ops.max_priority(h)  # Maximum priority occurring in g

    W0 = []  # winning region for player 0
    W1 = []  # winning region for player 1
    sigma0 = defaultdict(lambda: -1)  # winning strategy for player 0
    sigma1 = defaultdict(lambda: -1)  # winning strategy for player 1

    # considering priorities from i to 0 in decreasing order
    for k in range(i, -1, -1):
        current_player = k % 2  # get current player

        # calling the reachability solver on the game h with target set "nodes of priority k" and for the current player
        (Ak, eta), (Bk, nu) = rs.reachability_solver(h, ops.i_priority_node(h, k), current_player)

        # depending on the current player, we add the nodes of Ak in a winning region and update strategies
        if current_player == 0:
            W0.extend(Ak)
            sigma0.update(eta)
            sigma1.update(nu)

        else:
            W1.extend(Ak)
            sigma1.update(eta)
            sigma0.update(nu)

        h = h.subgame(Bk)  # updates the current game (only keeping nodes in Bk)

    return (W0, sigma0), (W1, sigma1)
