from collections import defaultdict

import reachability
from tools import operations as ops


def generalized_parity_solver(g):
    """
    Generalized parity games solver. This is an implementation of the algorithm presented by Chatterjee.
    :param g: the game to solve.
    :return: the solution in the following format : (W_0, sigma_0), (W_1, sigma_1).
    """
    W1 = []  # Winning region of player 0
    W2 = []  # Winning region of player 1
    strat1 = defaultdict(lambda: -1)  # Winning strategy of player 0
    strat2 = defaultdict(lambda: -1)  # Winning strategy of player 1

    return (W1, strat1), (W2, strat2)