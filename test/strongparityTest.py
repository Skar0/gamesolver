from tools import fileHandler as io
from solvers import strongParity as sp

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