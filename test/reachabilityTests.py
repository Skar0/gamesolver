from tools import fileHandler as io
from solvers import reachability as rs


def fig32():
    fig32_graph = io.load_from_file("../assets/reachability/fig32.txt")
    regions, strategies = rs.reachability_solver(fig32_graph, [1], 0)
    expected_regions = {1: 0, 2: 0, 3: 0, 4: 1, 5: 0, 6: 1}
    expected_strategies = {1: 1, 2: 1, 4: 6, 5: 2, 6: 4}
    print regions == expected_regions and strategies == expected_strategies


def fig51():
    fig51_graph = io.load_from_file("../assets/reachability/fig51.txt")
    regions, strategies = rs.reachability_solver(fig51_graph, [8], 1)
    expected_regions = {1: 0, 2: 0, 3: 0, 4: 1, 5: 0, 6: 0, 7: 1, 8: 1}
    expected_strategies = {8: 3, 1: 5, 3: 3, 6: 5, 7: 8}
    print regions == expected_regions and strategies == expected_strategies

def fig32_tuple():
    fig32_graph = io.load_from_file("../assets/reachability/fig32.txt")
    (W0, sig0), (W1, sig1) = rs.reachability_solver_tuples(fig32_graph, [1], 0)
    print W0 == [1,2,3,5] and sig0 == {1: 1, 2: 1, 5: 2} and W1 == [4,6] and sig1 == {4: 6, 6: 4}


def fig51_tuple():
    fig51_graph = io.load_from_file("../assets/reachability/fig51.txt")
    (W1, sig1), (W0, sig0) = rs.reachability_solver_tuples(fig51_graph, [8], 1)
    print W1 == [8,7,4] and sig1 == {8: 3, 7: 8} and W0 == [1,2,3,5,6] and sig0 == {1: 5, 3: 3, 6: 5}


fig32()
fig51()

fig32_tuple()
fig51_tuple()
