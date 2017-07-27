from collections import defaultdict

import reachability


def init_out(g):
    out = defaultdict(int)
    for node in g.get_nodes():
        for pred in g.get_predecessors(node):
            out[pred] += 1
    return out


def maxPriority(g):
    nodes = g.nodes
    m = max(nodes.items(), key=lambda (k, v): v[1])[1][1]
    return m

def nodesmax(g,i):
    nodes = g.nodes
    c = filter(lambda (k, v): v[1] == i,nodes.items())
    l = []
    for e in c :
        l.append(e[0])
    return l


def strongparity_solver(g):
    """
      @type g: Graph
      """
    regions = defaultdict(lambda: -1)
    strategies = defaultdict(lambda: -1)

    if len(g.nodes) == 0:
        return regions, strategies
    else:
        i = maxPriority(g)

        if i % 2 == 0:
            j = 0
        else:
            j = 1

        U = nodesmax(g,i)

        A, t1 = reachability.reachability_solver_updated(g,U,j)

        subGame = []
        #nodes to stay in the subgame ie not in the attractor ie region assigned is opposite
        for node in A:
            if A[node] == opposite(j):
                subGame.append(node)
        g_A = g.subgame(subGame)

        regions1, strategies1 = strongparity_solver(g_A)

        print t1, strategies1
        # check if region is empty
        flag = False
        W1 = []
        for node in regions1:
            if regions1[node] == opposite(j):
                flag = True
                W1.append(node)

        if flag:
            #sinon
            B,v = reachability.reachability_solver_updated(g,W1,opposite(j))
            subGame = []
            # nodes to stay in the subgame ie not in the attractor ie region assigned is opposite
            for node in B:
                if B[node] == j:
                    subGame.append(node)
            g_B = g.subgame(subGame)
            regions2, strategies2 = strongparity_solver(g_B)
            for node in regions2:
                if regions2[node] == j:
                    regions[node] = j
                else :
                    regions[node] = opposite(j)
            for node in B:
                if B[node] == opposite(j):
                    regions[node] = opposite(j)


            for node in v:
                if g.get_node_player(node) == opposite(j):
                    strategies[node] = v[node]
            for node in strategies2:
                    strategies[node] = strategies2[node]
            for node in strategies1:
                if g.get_node_player(node) == opposite(j):
                    strategies[node] = strategies1[node]

        else:
            #vide so add attractor and region on subgame
            for elem in regions1:
                regions[elem] = regions1[elem]
            for elem in A:
                regions[elem] = j
            for node in strategies1:
                if g.get_node_player(node) == j:
                    strategies[node] = strategies1[node]
            for node in t1:
                if g.get_node_player(node) == j:
                    strategies[node] = t1[node]

    print regions, strategies
    return regions, strategies

def opposite(j):
    if j == 1:
        return 0
    else:
        return 1
