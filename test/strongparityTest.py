from tools import fileHandler as io
from solvers import strongParity as sp
from subprocess import call
def fig47():
    fig47_graph = io.load_from_file("../assets/strong parity/fig47.txt")
    (a,b),(c,d) = sp.strongparity_solver2(fig47_graph)
    print (a == [2, 4, 1, 6]) and b =={2: 2, 4: 1} and c == [5, 3]and d == {5: 5}

fig47()

def example_1():
    g = io.load_from_file("../assets/strong parity/example_1.txt")
    (a,b),(c,d) = sp.strongparity_solver2(g)
    print (a == [1,3,2]) and b =={1: 1, 3: 3} and c == [] and d == {}

example_1()

def example_2():
    g = io.load_from_file("../assets/strong parity/example_2.txt")
    (a,b),(c,d) = sp.strongparity_solver2(g)
    print (a == [1,3,4,2]) and b =={1: 1, 3: 3, 4:4} and c == [] and d == {}

example_2()

def example_3():
    g = io.load_from_file("../assets/strong parity/example_3.txt")
    (a,b),(c,d) = sp.strongparity_solver2(g)
    print (a == [2,1,3,4]) and b =={4:4,2:4,1: 2} and c == [6,7,5] and d == {7:6,6:6,5:6}

example_3()


def example_4():
    g = io.load_from_file("../assets/strong parity/example_4.txt")
    (a,b),(c,d) = sp.strongparity_solver2(g)
    print a == [2, 1, 5] and b == {1: 2, 2: 2, 5: 5} and c ==[6, 3, 4] and d == {3: 6, 4: 3, 6: 6}

example_4()


def example_5():
    g = io.load_from_file("../assets/strong parity/example_5.txt")
    (a,b),(c,d) = sp.strongparity_solver2(g)
    print a == [2, 1, 5] and b =={1: 2, 2: 2, 5: 5}and c ==[7, 6, 3, 4] and d == {3: 6, 4: 3, 6: 6}

example_5()

def recursive_ladder_1():
    g = io.load_from_file("../assets/strong parity/recursive_ladder_1.txt")
    (a,b),(c,d) = sp.strongparity_solver2(g)
    print a == [1, 3, 4, 2, 0] and b == {1: 2, 3: 1} and c == [] and d == {}

recursive_ladder_1()

def recursive_ladder_2():
    g = io.load_from_file("../assets/strong parity/recursive_ladder_2.txt")
    (a,b),(c,d) = sp.strongparity_solver2(g)
    print a == [] and b == {} and c == [6, 8, 9, 7, 5, 4, 0, 2, 1, 3] and d == {0: 4, 2: 4, 4: 5, 6: 7, 8: 6}

recursive_ladder_2()