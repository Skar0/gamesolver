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


fig32()
fig51()
