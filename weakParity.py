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


def weakParity_solver(g):
    regions = defaultdict(lambda: -1)
    strategies = defaultdict(lambda: -1)

    h = g
    i = maxPriority(h)

    regions = defaultdict(lambda: -1)
    strategies = defaultdict(lambda: -1)

    for k in range(i, -1, -1):
        (Ak,Sk) = reachability.reachability_solver_updated(h, nodesmax(h, k), k % 2)
        #print "iter "+str(k)+" -- "+str(Ak)+" -- "+str(Sk)
        p = []
        for node in Ak:
            if Ak[node]  == k%2:
                regions[node] = k%2
                if h.get_node_player(node) == k%2:
                    strategies[node] = Sk[node]
            else:
                p.append(node)
        h = h.subgame(p)

    return regions, strategies

def opposite(j):
    if j == 1:
        return 0
    else:
        return 1
