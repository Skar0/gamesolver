from tools import fileHandler as io
from solvers import weakParity as wp


def example_1():
    g = io.load_from_file("../assets/weak parity/example_1.txt")
    (a,b),(c,d) = wp.weak_parity_solver(g)

    print a == [3] and b == {2:5,4:5} and c == [1, 4, 2, 5] and d == {1: 1, 3: 5, 5: 2}

example_1()

def fig51():
    g = io.load_from_file("../assets/weak parity/fig51.txt")
    (a,b),(c,d) = wp.weak_parity_solver(g)
    print a == [3, 6, 2] and b == {1: 5, 3: 3, 6: 1} and c == [8, 7, 4, 5, 1] and d =={8: 3, 5: 1, 7: 8}



fig51()