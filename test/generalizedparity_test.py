from tools import file_handler as io
from tools import operations as op
from solvers import generalizedparity as gp
"""
Test module for generalized parity games.
Some examples are solved by our algorithm and we verify the solution. 
"""

"""
The first tests only have one priority function
"""
def figure56():
    """
    Solves the strong parity game from figure 5.6.
    """
    g = io.load_generalized_from_file("../assets/strong parity/figure56.txt")
    (a,c) = gp.generalized_parity_solver(g)
    return op.are_lists_equal(a ,[2, 4, 1, 6]) and op.are_lists_equal(c , [5, 3])

def example_1():
    """
    Solves a simple example.
    """
    g = io.load_generalized_from_file("../assets/strong parity/example_1.txt")
    (a,c) = gp.generalized_parity_solver(g)
    return op.are_lists_equal(a, [1, 3, 2]) and op.are_lists_equal(c , [])


def example_2():
    """
    Solves a simple example.
    """
    g = io.load_generalized_from_file("../assets/strong parity/example_2.txt")
    (a,c) = gp.generalized_parity_solver(g)
    return op.are_lists_equal(a , [1, 3, 4, 2]) and op.are_lists_equal(c , [])


def example_3():
    """
    Solves a simple example.
    """
    g = io.load_generalized_from_file("../assets/strong parity/example_3.txt")
    (a,c) = gp.generalized_parity_solver(g)
    return op.are_lists_equal(a , [2, 1, 3, 4]) and op.are_lists_equal(c , [6, 7, 5])


def example_4():
    """
    Solves a simple example.
    """
    g = io.load_generalized_from_file("../assets/strong parity/example_4.txt")
    (a,c) = gp.generalized_parity_solver(g)
    return op.are_lists_equal(a , [2, 1, 5]) and op.are_lists_equal(c , [6, 3, 4])


def example_5():
    """
    Solves a simple example.
    """
    g = io.load_generalized_from_file("../assets/strong parity/example_5.txt")
    (a,c) = gp.generalized_parity_solver(g)
    return op.are_lists_equal(a , [2, 1, 5]) and op.are_lists_equal(c , [7, 6, 3, 4])


def worstcase1():
    """
    Solves a worst case graph G_n for n = 1.
    """
    g = io.load_generalized_from_file("../assets/strong parity/worstcase_1.txt")
    (a,c) = gp.generalized_parity_solver(g)
    return op.are_lists_equal(a , [1, 3, 4, 2, 0]) and op.are_lists_equal(c , [])


def worstcase2():
    """
    Solves a worst case graph G_n for n = 2.
    """
    g = io.load_generalized_from_file("../assets/strong parity/worstcase_2.txt")
    (a,c) = gp.generalized_parity_solver(g)
    return op.are_lists_equal(a , []) and op.are_lists_equal(c , [6, 8, 9, 7, 5, 4, 0, 2, 1, 3])

def double_priority():
    """
    Solves a graph in which the priorities are twice the same.
    """
    g = io.load_generalized_from_file("../assets/generalized parity/double_priority.txt")
    (a,c) = gp.generalized_parity_solver(g)
    return op.are_lists_equal(a , []) and op.are_lists_equal(c , [4, 5, 6, 7, 3, 1, 2])

def counter_example():
    """
    Solves a graph which is one of the counter examples for the naive algorithms.
    Player 1 cannot avoid cycling between nodes in which 3 will appear infinitely often
    according to one of the priority function.
    """
    g = io.load_generalized_from_file("../assets/generalized parity/counter_example.txt")
    (a,c) = gp.generalized_parity_solver(g)
    return op.are_lists_equal(a , []) and op.are_lists_equal(c , [1, 2, 3])

def simple_example():
    """
    Solves a graph which is a simple example for the algorithm.
    Player 1 can choose to cycle between two nodes, since center node has priorities (2,2),
    the path has maximal priority occurring infinitely often 2 for each priority function.
    """
    g = io.load_generalized_from_file("../assets/generalized parity/simple_example.txt")
    (a,c) = gp.generalized_parity_solver(g)
    return op.are_lists_equal(a , [1, 2, 3]) and op.are_lists_equal(c , [])

def complementary_priorities():
    """
    Solves a graph in which the priorities are complementary (one is odd, one is even).
    This means that player 1 looses from every node (can't have a path even for every priority function)
    """
    g = io.load_generalized_from_file("../assets/generalized parity/complementary_priorities.txt")
    (a,c) = gp.generalized_parity_solver(g)
    return op.are_lists_equal(a , []) and op.are_lists_equal(c , [6, 3, 4, 5, 7, 1, 2])

def t():
    """
    Launches all tests.
    :return: true if all tests succeeded.
    """
    return figure56() and example_1() and example_2() and example_3() and example_4() and example_5() and worstcase1() and worstcase2() and complementary_priorities() and double_priority() and counter_example()

print("------------------------------------------>"+str(figure56()))
print("------------------------------------------>"+str(example_1()))
print("------------------------------------------>"+str(example_2()))
print("------------------------------------------>"+str(example_3()))
print("------------------------------------------>"+str(example_4()))
print("------------------------------------------>"+str(example_5()))
print("------------------------------------------>"+str(worstcase1()))
print("------------------------------------------>"+str(worstcase2()))
print("------------------------------------------>"+str(double_priority()))
print("------------------------------------------>"+str(counter_example()))
print("------------------------------------------>"+str(simple_example()))
print("------------------------------------------>"+str(complementary_priorities()))