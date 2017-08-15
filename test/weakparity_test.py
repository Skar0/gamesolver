from tools import file_handler as io
from solvers import weakparity as wp

"""
Test module for weak parity games.
Some examples are solved by our algorithm and we verify the solution. 
"""


def figure41():
    """
    Solves the weak parity game from figure 4.1.
    """
    g = io.load_from_file("assets/weak parity/figure41.txt")
    (a, b), (c, d) = wp.weak_parity_solver(g)
    return a == [3] and b == {1: 2, 5: 5} and c == [4, 5, 1, 2] and d == {4: 4, 2: 1, 3: 3}


def example_1():
    g = io.load_from_file("assets/weak parity/example_1.txt")
    (a, b), (c, d) = wp.weak_parity_solver(g)
    return a == [3, 6, 2] and b == {1: 5, 3: 3, 6: 1} and c == [8, 7, 4, 5, 1] and d == {8: 3, 5: 1, 7: 8}


def launch_tests():
    """
    Launches all tests.
    :return: true if all tests succeeded.
    """
    return figure41() and example_1()
