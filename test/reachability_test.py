from tools import file_handler as io
from solvers import reachability as rs

"""
Test module for reachability games.
Some examples are solved by our algorithm and we verify the solution. 
"""


def figure32():
    """
    Solves the reachability game from figure 3.2.
    """
    fig32_graph = io.load_from_file("assets/reachability/figure32.txt")
    (W0, sig0), (W1, sig1) = rs.reachability_solver(fig32_graph, [1], 0)
    return W0 == [1, 2, 3, 5] and sig0 == {1: 1, 2: 1, 5: 2} and W1 == [4, 6] and sig1 == {4: 6, 6: 4}


def example_1():
    """
    Solves a simple example.
    """
    fig51_graph = io.load_from_file("assets/reachability/fig51.txt")
    (W1, sig1), (W0, sig0) = rs.reachability_solver(fig51_graph, [8], 1)
    return W1 == [8, 7, 4] and sig1 == {8: 3, 7: 8} and W0 == [1, 2, 3, 5, 6] and sig0 == {1: 5, 3: 3, 6: 5}


def launch_tests():
    """
    Launches all tests.
    :return: true if all tests succeeded.
    """
    return figure32() and example_1()
