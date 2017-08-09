from collections import defaultdict

import reachability
from tools import operations as ops


def strongparity_solver(g):
    """
      @type g: Graph
      """
    regions = defaultdict(lambda: -1)
    strategies = defaultdict(lambda: -1)

    if len(g.nodes) == 0:
        return regions, strategies
    else:
        i = ops.max_priority(g)

        if i % 2 == 0:
            j = 0
        else:
            j = 1

        U = ops.i_priority_node(g,i)

        A, t1 = reachability.reachability_solver(g, U, j)

        subGame = []
        #nodes to stay in the subgame ie not in the attractor ie region assigned is opposite
        for node in A:
            if A[node] == ops.opponent(j):
                subGame.append(node)
        g_A = g.subgame(subGame)

        regions1, strategies1 = strongparity_solver(g_A)

        print t1, strategies1
        # check if region is empty
        flag = False
        W1 = []
        for node in regions1:
            if regions1[node] == ops.opponent(j):
                flag = True
                W1.append(node)

        if flag:
            #sinon
            B,v = reachability.reachability_solver(g, W1, ops.opponent(j))
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
                    regions[node] = ops.opponent(j)
            for node in B:
                if B[node] == ops.opponent(j):
                    regions[node] = ops.opponent(j)


            for node in v:
                if g.get_node_player(node) == ops.opponent(j):
                    strategies[node] = v[node]
            for node in strategies2:
                    strategies[node] = strategies2[node]
            for node in strategies1:
                if g.get_node_player(node) == ops.opponent(j):
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


def strongparity_solver2(g):
    """
      @type g: Graph
      """
    W1 = []
    W2 = []
    strat1 = defaultdict(lambda: -1)
    strat2 =  defaultdict(lambda: -1)

    if len(g.nodes) == 0:
        return (W1, strat1), (W2, strat2)
    else:
        i = ops.max_priority(g)
        #joueur 0 1 pcq c'est plus facile avec mod 2
        if i % 2 == 0:
            j = 0
        else:
            j = 1

        opponent = ops.opponent(j)

        U = ops.i_priority_node(g,i)

        (A, tau1), (discard1, discard2) = reachability.reachability_solver_tuples(g, U, j)
        #nodes to stay in the subgame ie not in the attractor ie region assigned is opposite

        G_A = g.subgame(discard1)

        sol_player1, sol_player2 = strongparity_solver2(G_A)

        if j == 0:
            W_j, sig_j = sol_player1
            W_jbar, sig_jbar = sol_player2
        else:
            W_j, sig_j = sol_player2
            W_jbar, sig_jbar = sol_player1


        if not W_jbar:
            if j == 0:
                W1.extend(A)
                W1.extend(W_j)
                strat1.update(tau1)
                strat1.update(sig_j)
            else:
                W2.extend(A)
                W2.extend(W_j)
                strat2.update(tau1)
                strat2.update(sig_j)
        else:
            (B,nu), (discard1, discard2) = reachability.reachability_solver_tuples(g, W_jbar, opponent)
            G_B = g.subgame(discard1)
            sol_player1_, sol_player2_ = strongparity_solver2(G_B)

            if j == 0:
                W__j, sig__j = sol_player1_
                W__jbar, sig__jbar = sol_player2_
            else:
                W__j, sig__j = sol_player2_
                W__jbar, sig__jbar = sol_player1_

            if j == 0:
                W1 = W__j
                strat1 = sig__j

                W2.extend(W__jbar)
                W2.extend(B)
                strat2.update(nu)
                strat2.update(sig__jbar)
                strat2.update(sig_jbar)

            else:
                W2 = W__j
                strat2 = sig__j

                W1.extend(W__jbar)
                W1.extend(B)
                strat1.update(nu)
                strat1.update(sig__jbar)
                strat1.update(sig_jbar)

    #print (W1,strat1),(W2, strat2)
    return (W1,strat1),(W2, strat2)


