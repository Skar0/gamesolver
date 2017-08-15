from collections import defaultdict

import reachability
from tools import operations as ops


def strong_parity_solver(g):
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

        sol_player1, sol_player2 = strong_parity_solver(G_A)

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
            sol_player1_, sol_player2_ = strong_parity_solver(G_B)

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


