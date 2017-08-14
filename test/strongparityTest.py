from tools import fileHandler as io
from solvers import strongParity as sp

"""
Test class for strong parity games.
Some examples are solved by our algorithm and we verify the solution. 
"""


def figure56():
    """
    Solves the strong parity game from figure 5.6.
    """
    fig47_graph = io.load_from_file("assets/strong parity/figure56.txt")
    (a, b), (c, d) = sp.strongparity_solver2(fig47_graph)
    return (a == [2, 4, 1, 6]) and b == {2: 2, 4: 1} and c == [5, 3] and d == {5: 5}


def example_1():
    """
    Solves a simple example.
    """
    g = io.load_from_file("assets/strong parity/example_1.txt")
    (a, b), (c, d) = sp.strongparity_solver2(g)
    return (a == [1, 3, 2]) and b == {1: 1, 3: 3} and c == [] and d == {}


def example_2():
    """
    Solves a simple example.
    """
    g = io.load_from_file("assets/strong parity/example_2.txt")
    (a, b), (c, d) = sp.strongparity_solver2(g)
    return (a == [1, 3, 4, 2]) and b == {1: 1, 3: 3, 4: 4} and c == [] and d == {}


def example_3():
    """
    Solves a simple example.
    """
    g = io.load_from_file("assets/strong parity/example_3.txt")
    (a, b), (c, d) = sp.strongparity_solver2(g)
    return (a == [2, 1, 3, 4]) and b == {4: 4, 2: 4, 1: 2} and c == [6, 7, 5] and d == {7: 6, 6: 6, 5: 6}


def example_4():
    """
    Solves a simple example.
    """
    g = io.load_from_file("assets/strong parity/example_4.txt")
    (a, b), (c, d) = sp.strongparity_solver2(g)
    return a == [2, 1, 5] and b == {1: 2, 2: 2, 5: 5} and c == [6, 3, 4] and d == {3: 6, 4: 3, 6: 6}


def example_5():
    """
    Solves a simple example.
    """
    g = io.load_from_file("assets/strong parity/example_5.txt")
    (a, b), (c, d) = sp.strongparity_solver2(g)
    return a == [2, 1, 5] and b == {1: 2, 2: 2, 5: 5} and c == [7, 6, 3, 4] and d == {3: 6, 4: 3, 6: 6}


def worstcase1():
    """
    Solves a worst case graph G_n for n = 1.
    """
    g = io.load_from_file("assets/strong parity/worstcase_1.txt")
    (a, b), (c, d) = sp.strongparity_solver2(g)
    return a == [1, 3, 4, 2, 0] and b == {1: 2, 3: 1} and c == [] and d == {}


def worstcase2():
    """
    Solves a worst case graph G_n for n = 2.
    """
    g = io.load_from_file("assets/strong parity/worstcase_2.txt")
    (a, b), (c, d) = sp.strongparity_solver2(g)
    return a == [] and b == {} and c == [6, 8, 9, 7, 5, 4, 0, 2, 1, 3] and d == {0: 4, 2: 4, 4: 5, 6: 7, 8: 6}


def launch_tests():
    """
    Launches all tests.
    :return: true if all tests succeeded.
    """
    return figure56() and example_1() and example_2() and example_3() and example_4() and example_5() and worstcase1() and worstcase2()
