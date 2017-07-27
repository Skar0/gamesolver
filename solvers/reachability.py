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
        # print("considering node "+str(s))
        for sbis in g.get_predecessors(s):
            # print("--considering predecessor " + str(sbis)+" "+str(g.get_node_player(sbis)))
            if g.get_node_region(sbis) == -1:
                if g.get_node_player(sbis) == j:
                    queue.append(sbis)
                    g.set_node_region(sbis, j)
                    g.set_node_strategy(sbis, s)
                elif g.get_node_player(sbis) == opponent:
                    out[sbis] -= 1
                    if out[sbis] == 0:
                        queue.append(sbis)
                        g.set_node_region(sbis, j)
                        # print("---- current regions "+str(g.get_regions()))
                        # print("---- current strat "+str(g.get_strategies()))

    for node in g.get_nodes():
        if g.get_node_region(node) != j:
            g.set_node_region(node, opponent)
            for predecessor in g.get_predecessors(node):
                if g.get_node_region(predecessor) != j and g.get_node_player(predecessor) == opponent:
                    g.set_node_strategy(predecessor, node)
                    # print("---- current regions " + str(g.get_regions()))
                    # print("---- current strat " + str(g.get_strategies()))


def reachability_solver_updated(g, U, j):
    out = init_out(g)
    queue = []
    regions = defaultdict(lambda: -1)
    strategies = defaultdict(lambda: -1)
    opponent = opposite(j)

    for node in U:
        queue.append(node)
        regions[node] = j
        if g.get_node_player(node) == j:
            strategies[node] = g.get_successors(node)[0]

    while len(queue) != 0:
        s = queue[0]
        queue = queue[1:]
        # print("considering node "+str(s))
        for sbis in g.get_predecessors(s):
            # print("--considering predecessor " + str(sbis)+" "+str(g.get_node_player(sbis)))
            if regions[sbis] == -1:
                if g.get_node_player(sbis) == j:
                    queue.append(sbis)
                    regions[sbis] = j
                    strategies[sbis] = s
                elif g.get_node_player(sbis) == opponent:
                    out[sbis] -= 1
                    if out[sbis] == 0:
                        queue.append(sbis)
                        regions[sbis] = j
                        # print("---- current regions "+str(g.get_regions()))
                        # print("---- current strat "+str(g.get_strategies()))

    for node in g.get_nodes():
        if regions[node] != j:
            regions[node] = opponent
            for predecessor in g.get_predecessors(node):
                if regions[predecessor] != j and g.get_node_player(predecessor) == opponent:
                    strategies[predecessor] = node
                    # print("---- current regions " + str(g.get_regions()))
                    # print("---- current strat " + str(g.get_strategies()))
    return regions, strategies


def opposite(j):
    if j == 1:
        return 0
    else:
        return 1
