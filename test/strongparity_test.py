from bitarray import bitarray

from tools import file_handler as io
from solvers import strongparity as sp
from solvers import generalizedparity as gp
from tools import operations as ops
"""
Test module for strong parity games.
Some examples are solved by our algorithm and we verify the solution. 
"""

"""
Recursive algorithm
"""

def figure56():
    """
    Solves the strong parity game from figure 5.6.
    """
    fig56_graph = io.load_from_file("assets/strong parity/figure56.txt")
    (a, b), (c, d) = sp.strong_parity_solver(fig56_graph)
    return (a == [2, 4, 1, 6]) and b == {2: 2, 4: 1} and c == [5, 3] and d == {5: 5}

def example_1():
    """
    Solves a simple example.
    """
    g = io.load_from_file("assets/strong parity/example_1.txt")
    (a, b), (c, d) = sp.strong_parity_solver(g)
    return (a == [1, 3, 2]) and b == {1: 1, 3: 3} and c == [] and d == {}


def example_2():
    """
    Solves a simple example.
    """
    g = io.load_from_file("assets/strong parity/example_2.txt")
    (a, b), (c, d) = sp.strong_parity_solver(g)
    return (a == [1, 3, 4, 2]) and b == {1: 1, 3: 3, 4: 4} and c == [] and d == {}


def example_3():
    """
    Solves a simple example.
    """
    g = io.load_from_file("assets/strong parity/example_3.txt")
    (a, b), (c, d) = sp.strong_parity_solver(g)
    return (a == [2, 1, 3, 4]) and b == {4: 4, 2: 4, 1: 2} and c == [6, 7, 5] and d == {7: 6, 6: 6, 5: 6}


def example_4():
    """
    Solves a simple example.
    """
    g = io.load_from_file("assets/strong parity/example_4.txt")
    (a, b), (c, d) = sp.strong_parity_solver(g)
    return a == [2, 1, 5] and b == {1: 2, 2: 2, 5: 5} and c == [6, 3, 4] and d == {3: 6, 4: 3, 6: 6}


def example_5():
    """
    Solves a simple example.
    """
    g = io.load_from_file("assets/strong parity/example_5.txt")
    (a, b), (c, d) = sp.strong_parity_solver(g)
    return a == [2, 1, 5] and b == {1: 2, 2: 2, 5: 5} and c == [7, 6, 3, 4] and d == {3: 6, 4: 3, 6: 6}


def worstcase1():
    """
    Solves a worst case graph G_n for n = 1.
    """
    g = io.load_from_file("assets/strong parity/worstcase_1.txt")
    (a, b), (c, d) = sp.strong_parity_solver(g)
    return a == [1, 3, 4, 2, 0] and b == {1: 2, 3: 1} and c == [] and d == {}


def worstcase2():
    """
    Solves a worst case graph G_n for n = 2.
    """
    g = io.load_from_file("assets/strong parity/worstcase_2.txt")
    (a, b), (c, d) = sp.strong_parity_solver(g)
    return a == [] and b == {} and c == [6, 8, 9, 7, 5, 4, 0, 2, 1, 3] and d == {0: 4, 2: 4, 4: 5, 6: 7, 8: 6}


"""
Recursive algorithm with the removed list optimization
"""

def figure56_removed_optimization():
    """
    Solves the strong parity game from figure 5.6.
    """
    fig56_graph = io.load_from_file("assets/strong parity/figure56.txt")
    removed = bitarray([False]+([False]*len(fig56_graph.nodes)))
    (a, b), (c, d) = sp.strong_parity_solver_non_removed(fig56_graph, removed)
    return (a == [2, 4, 1, 6]) and b == {2: 2, 4: 1} and c == [5, 3] and d == {5: 5}

def example_1_removed_optimization():
    """
    Solves a simple example.
    """
    g = io.load_from_file("assets/strong parity/example_1.txt")
    removed = bitarray([False]+([False]*len(g.nodes)))
    (a, b), (c, d) = sp.strong_parity_solver_non_removed(g, removed)
    return (a == [1, 3, 2]) and b == {1: 1, 3: 3} and c == [] and d == {}


def example_2_removed_optimization():
    """
    Solves a simple example.
    """
    g = io.load_from_file("assets/strong parity/example_2.txt")
    removed = bitarray([False]+([False]*len(g.nodes)))
    (a, b), (c, d) = sp.strong_parity_solver_non_removed(g,removed)
    return (a == [1, 3, 4, 2]) and b == {1: 1, 3: 3, 4: 4} and c == [] and d == {}


def example_3_removed_optimization():
    """
    Solves a simple example.
    """
    g = io.load_from_file("assets/strong parity/example_3.txt")
    removed = bitarray([False]+([False]*len(g.nodes)))
    (a, b), (c, d) = sp.strong_parity_solver_non_removed(g, removed)
    return (a == [2, 1, 3, 4]) and b == {4: 4, 2: 4, 1: 2} and c == [6, 7, 5] and d == {7: 6, 6: 6, 5: 6}


def example_4_removed_optimization():
    """
    Solves a simple example.
    """
    g = io.load_from_file("assets/strong parity/example_4.txt")
    removed = bitarray([False]+([False]*len(g.nodes)))
    (a, b), (c, d) = sp.strong_parity_solver_non_removed(g, removed)
    return a == [2, 1, 5] and b == {1: 2, 2: 2, 5: 5} and c == [6, 3, 4] and d == {3: 6, 4: 3, 6: 6}


def example_5_removed_optimization():
    """
    Solves a simple example.
    """
    g = io.load_from_file("assets/strong parity/example_5.txt")
    removed = bitarray([False]+([False]*len(g.nodes)))
    (a, b), (c, d) = sp.strong_parity_solver_non_removed(g, removed)
    return a == [2, 1, 5] and b == {1: 2, 2: 2, 5: 5} and c == [7, 6, 3, 4] and d == {3: 6, 4: 3, 6: 6}


def worstcase1_removed_optimization():
    """
    Solves a worst case graph G_n for n = 1.
    """
    g = io.load_from_file("assets/strong parity/worstcase_1.txt")
    removed = bitarray([False]+([False]*len(g.nodes)))
    (a, b), (c, d) = sp.strong_parity_solver_non_removed(g, removed)
    return a == [1, 3, 4, 2, 0] and b == {1: 2, 3: 1} and c == [] and d == {}


def worstcase2_removed_optimization():
    """
    Solves a worst case graph G_n for n = 2.
    """
    g = io.load_from_file("assets/strong parity/worstcase_2.txt")
    removed = bitarray([False]+([False]*len(g.nodes)))
    (a, b), (c, d) = sp.strong_parity_solver_non_removed(g, removed)
    return a == [] and b == {} and c == [6, 8, 9, 7, 5, 4, 0, 2, 1, 3] and d == {0: 4, 2: 4, 4: 5, 6: 7, 8: 6}

"Antichain-based algorithm"

def figure56_antichain_algorithm():
    """
    Solves the strong parity game from figure 5.6.
    """
    fig56_graph = io.load_from_file("assets/strong parity/figure56.txt")
    (a, c) = sp.strong_parity_antichain_based(fig56_graph,1)
    return ops.are_lists_equal(a,[2, 4, 1, 6])  and ops.are_lists_equal(c,[5, 3])

def example_1_antichain_algorithm():
    """
    Solves a simple example.
    """
    g = io.load_from_file("assets/strong parity/example_1.txt")
    (a, c) = sp.strong_parity_antichain_based(g,1)
    return ops.are_lists_equal(a , [1, 3, 2]) and ops.are_lists_equal(c, [])


def example_2_antichain_algorithm():
    """
    Solves a simple example.
    """
    g = io.load_from_file("assets/strong parity/example_2.txt")
    (a, c) = sp.strong_parity_antichain_based(g,1)
    return ops.are_lists_equal(a, [1, 3, 4, 2]) and ops.are_lists_equal(c, [])


def example_3_antichain_algorithm():
    """
    Solves a simple example.
    """
    g = io.load_from_file("assets/strong parity/example_3.txt")
    (a, c) = sp.strong_parity_antichain_based(g,1)
    return ops.are_lists_equal(a, [2, 1, 3, 4])  and ops.are_lists_equal(c, [6, 7, 5])


def example_4_antichain_algorithm():
    """
    Solves a simple example.
    """
    g = io.load_from_file("assets/strong parity/example_4.txt")
    (a, c) = sp.strong_parity_antichain_based(g,1)
    return ops.are_lists_equal(a, [2, 1, 5]) and ops.are_lists_equal(c, [6, 3, 4])


def example_5_antichain_algorithm():
    """
    Solves a simple example.
    """
    g = io.load_from_file("assets/strong parity/example_5.txt")
    (a, c) = sp.strong_parity_antichain_based(g,1)
    return ops.are_lists_equal(a, [2, 1, 5]) and ops.are_lists_equal(c, [7, 6, 3, 4])


def worstcase1_antichain_algorithm():
    """
    Solves a worst case graph G_n for n = 1.
    """
    g = io.load_from_file("assets/strong parity/worstcase_1.txt")
    (a, c) = sp.strong_parity_antichain_based(g,0)
    return ops.are_lists_equal(a, [1, 3, 4, 2, 0]) and ops.are_lists_equal(c, [])


def worstcase2_antichain_algorithm():
    """
    Solves a worst case graph G_n for n = 2.
    """
    g = io.load_from_file("assets/strong parity/worstcase_2.txt")
    (a, c) = sp.strong_parity_antichain_based(g,0)
    return ops.are_lists_equal(a , [] ) and ops.are_lists_equal(c, [6, 8, 9, 7, 5, 4, 0, 2, 1, 3])

"""
Reduction to safety algorithm
"""

def figure56_reduction_to_safety():
    """
    Solves the strong parity game from figure 5.6.
    """
    fig56_graph = io.load_from_file("assets/strong parity/figure56.txt")
    (a, c) = sp.reduction_to_safety_parity_solver(fig56_graph)
    return ops.are_lists_equal(a,[2, 4, 1, 6])  and ops.are_lists_equal(c,[5, 3])

def example_1_reduction_to_safety():
    """
    Solves a simple example.
    """
    g = io.load_from_file("assets/strong parity/example_1.txt")
    (a, c) = sp.reduction_to_safety_parity_solver(g)
    return ops.are_lists_equal(a , [1, 3, 2]) and ops.are_lists_equal(c, [])


def example_2_reduction_to_safety():
    """
    Solves a simple example.
    """
    g = io.load_from_file("assets/strong parity/example_2.txt")
    (a, c) = sp.reduction_to_safety_parity_solver(g)
    return ops.are_lists_equal(a, [1, 3, 4, 2]) and ops.are_lists_equal(c, [])


def example_3_reduction_to_safety():
    """
    Solves a simple example.
    """
    g = io.load_from_file("assets/strong parity/example_3.txt")
    (a, c) = sp.reduction_to_safety_parity_solver(g)
    return ops.are_lists_equal(a, [2, 1, 3, 4])  and ops.are_lists_equal(c, [6, 7, 5])


def example_4_reduction_to_safety():
    """
    Solves a simple example.
    """
    g = io.load_from_file("assets/strong parity/example_4.txt")
    (a, c) = sp.reduction_to_safety_parity_solver(g)
    return ops.are_lists_equal(a, [2, 1, 5]) and ops.are_lists_equal(c, [6, 3, 4])


def example_5_reduction_to_safety():
    """
    Solves a simple example.
    """
    g = io.load_from_file("assets/strong parity/example_5.txt")
    (a, c) = sp.reduction_to_safety_parity_solver(g)
    return ops.are_lists_equal(a, [2, 1, 5]) and ops.are_lists_equal(c, [7, 6, 3, 4])


def worstcase1_reduction_to_safety():
    """
    Solves a worst case graph G_n for n = 1.
    """
    g = io.load_from_file("assets/strong parity/worstcase_1.txt")
    (a, c) = sp.reduction_to_safety_parity_solver(g)
    return ops.are_lists_equal(a, [1, 3, 4, 2, 0]) and ops.are_lists_equal(c, [])


def worstcase2_reduction_to_safety():
    """
    Solves a worst case graph G_n for n = 2.
    """
    g = io.load_from_file("assets/strong parity/worstcase_2.txt")
    (a, c) = sp.reduction_to_safety_parity_solver(g)
    return ops.are_lists_equal(a , [] ) and ops.are_lists_equal(c, [6, 8, 9, 7, 5, 4, 0, 2, 1, 3])

def launch_tests():
    """
    Launches all tests.
    :return: true if all tests succeeded.
    """
    recursive =  figure56() and example_1() and example_2() and example_3() and example_4() and example_5() and \
                 worstcase1() and worstcase2()
    removed_optimization = figure56_removed_optimization() and example_1_removed_optimization() and \
                      example_2_removed_optimization() and example_3_removed_optimization() and \
                      example_4_removed_optimization() and example_5_removed_optimization() and \
                      worstcase1_removed_optimization() and worstcase2_removed_optimization()
    reduction_to_safety = figure56_reduction_to_safety() and example_1_reduction_to_safety() and \
                      example_2_reduction_to_safety() and example_3_reduction_to_safety() and \
                      example_4_reduction_to_safety() and example_5_reduction_to_safety() and \
                      worstcase1_reduction_to_safety() and worstcase2_reduction_to_safety()
    antichain_based = figure56_antichain_algorithm() and example_1_antichain_algorithm() and \
                      example_2_antichain_algorithm() and example_3_antichain_algorithm() and \
                      example_4_antichain_algorithm() and example_5_antichain_algorithm() and \
                      worstcase1_antichain_algorithm() and worstcase2_antichain_algorithm()

    return recursive and removed_optimization and reduction_to_safety and antichain_based