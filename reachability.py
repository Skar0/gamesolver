graph = {1: [2, 3], 2: [3, 4, 5], 3: [5], 4: [6], 5: [4, 6], 6: [4, 5]}
players = [0, 0, 1, 1, 0, 1]


def initOut(graph):
    out = [0] * len(graph)
    for node in graph:
        for node2 in graph[node]:
            out[node2 - 1] += 1
    return out


def reachabilitySolver(graph, players, U, j):
    marq = [0] * len(graph)
    strat = [0] * len(graph)
    out = initOut(graph)
    queue = []

    for node in U:
        queue.append(node)
        marq[node - 1] = 1

    while len(queue) != 0:
        s = queue[0]
        queue = queue[1:]
        for sbis in graph[s]:
            if marq[sbis - 1] == 0:
                if players[sbis - 1] == j:
                    queue.append(sbis)
                    marq[sbis - 1] = 1
                    strat[sbis - 1] = s - 1
                else:
                    out[sbis - 1] -= 1
                    if out[sbis - 1] == 0:
                        queue.append(sbis)
                        marq[sbis - 1] = 1
                        strat[sbis - 1] = s - 1

    for node in graph:
        if marq[node - 1] == 0:
            for predecessor in graph[node]:
                if marq[predecessor - 1] == 0:
                    strat[predecessor - 1] = node - 1

    return marq, strat


res = reachabilitySolver(graph, players, [1], 0)


def cleanStrat(strat):
    t = []
    for elem in strat:
        t.append(elem + 1)
    return t


print(cleanStrat(res[1]))
