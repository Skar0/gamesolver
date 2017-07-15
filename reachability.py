from collections import defaultdict


def init_out(g):
    out = defaultdict(int)
    for node in g.get_nodes():
        for pred in g.get_predecessors(node):
            out[pred] += 1
    return out


def reachability_solver(g, U, j):
    out = init_out(g)
    queue = []

    opponent = opposite(j)

    for node in U:
        queue.append(node)
        g.set_node_region(node, j)
        g.set_node_strategy(node, g.get_successors(node)[0])

    while len(queue) != 0:
        s = queue[0]
        queue = queue[1:]
        for sbis in g.get_predecessors(s):
            if g.get_node_region(sbis) == 0:
                if g.get_node_player(sbis) == str(j):
                    queue.append(sbis)
                    g.set_node_region(sbis, j)
                    g.set_node_strategy(sbis, s)
                elif (g.get_node_player(sbis) == str(opponent)):
                    out[sbis] -= 1
                    if out[sbis] == 0:
                        queue.append(sbis)
                        g.set_node_region(sbis, j)

    for node in g.get_nodes():
        if g.get_node_region(node) != 1:
            g.set_node_region(node, opponent)
            for predecessor in g.get_predecessors(node):
                if g.get_node_region(predecessor) != 1:
                    g.set_node_strategy(predecessor, node)


def opposite(j):
    if j == 1:
        return 2
    else:
        return 1
