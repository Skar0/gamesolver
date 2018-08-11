from collections import defaultdict, deque

from bitarray import bitarray

import reachability
from antichains.library_linker import winning_region_c
from graph import Graph
from tools import operations as ops


def strong_parity_solver(g):
    """
    Strong parity games solver. This is an implementation of the algorithm presented in chapter 5 of the report.
    :param g: the game to solve.
    :return: the solution in the following format : (W_0, sigma_0), (W_1, sigma_1).
    """
    W1 = []  # Winning region of player 0
    W2 = []  # Winning region of player 1
    strat1 = defaultdict(lambda: -1)  # Winning strategy of player 0
    strat2 = defaultdict(lambda: -1)  # Winning strategy of player 1

    # if the game is empty, return the empty regions and strategies
    if len(g.nodes) == 0:
        return (W1, strat1), (W2, strat2)

    else:
        i = ops.max_priority(g)  # get max priority occurring in g

        # determining which player we are considering, if i is even : player 0 and else player 1
        if i % 2 == 0:
            j = 0
        else:
            j = 1

        opponent = ops.opponent(j)  # getting the opponent of the player

        U = ops.i_priority_node(g, i)  # target set for the attractor : nodes of priority i

        # getting the attractor A and the attractor strategy tau and discarding the region and strategy for the opponent
        (A, tau1), (discard1, discard2) = reachability.reachability_solver(g, U, j)

        # The subgame G\A is composed of the nodes not in the attractor, thus the nodes of the opposite player's region
        G_A = g.subgame(discard1)

        # Recursively solving the subgame G\A, solution comes as (W_0, sigma_0), (W_1, sigma_1)
        sol_player1, sol_player2 = strong_parity_solver(G_A)

        # depending on which player we are considering, assign regions and strategies to the proper variables
        # W'_j is noted W_j, sigma'_j is noted sig_j; the same aplies for jbar
        if j == 0:
            W_j, sig_j = sol_player1
            W_jbar, sig_jbar = sol_player2
        else:
            W_j, sig_j = sol_player2
            W_jbar, sig_jbar = sol_player1

        # if W'_jbar is empty we update the strategies and regions depending on the current player
        # the region and strategy for the whole game for one of the players is empty
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
            # compute attractor B and strategy nu
            (B, nu), (discard1, discard2) = reachability.reachability_solver(g, W_jbar, opponent)
            # The subgame G\B is composed of the nodes not in the attractor, so of the opposite player's winning region
            G_B = g.subgame(discard1)

            # recursively solve subgame G\B, solution comes as (W_0, sigma_0), (W_1, sigma_1)
            sol_player1_, sol_player2_ = strong_parity_solver(G_B)

            # depending on which player we are considering, assign regions and strategies to the proper variables
            # W''_j is noted W__j, sigma''_j is noted sig__j; the same aplies for jbar
            if j == 0:
                W__j, sig__j = sol_player1_
                W__jbar, sig__jbar = sol_player2_
            else:
                W__j, sig__j = sol_player2_
                W__jbar, sig__jbar = sol_player1_

            # the last step is to update the winning regions and strategies depending on which player we consider
            if j == 0:
                W1 = W__j
                strat1 = sig__j

                W2.extend(W__jbar)
                W2.extend(B)
                # nu is defined on W_jbar and must be replaced on W_jbar by the strategy sig_jbar
                # the replacement is implicit because updating sig_jbar last will overwrite already defined strategy
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

    return (W1, strat1), (W2, strat2)

def strong_parity_solver_no_strategies(g):
    """
    Strong parity games solver. This is an implementation of the algorithm presented in chapter 5 of the report.
    :param g: the game to solve.
    :return: the solution in the following format : (W_0, sigma_0), (W_1, sigma_1).
    """
    W1 = []  # Winning region of player 0
    W2 = []  # Winning region of player 1

    # if the game is empty, return the empty regions and strategies
    if len(g.nodes) == 0:
        return W1, W2

    else:
        i = ops.max_priority(g)  # get max priority occurring in g

        # determining which player we are considering, if i is even : player 0 and else player 1
        if i % 2 == 0:
            j = 0
        else:
            j = 1

        opponent = ops.opponent(j)  # getting the opponent of the player

        U = ops.i_priority_node(g, i)  # target set for the attractor : nodes of priority i

        # getting the attractor A and the attractor strategy tau and discarding the region and strategy for the opponent
        A, discard1 = reachability.attractor(g,U,j)

        # The subgame G\A is composed of the nodes not in the attractor, thus the nodes of the opposite player's region
        G_A = g.subgame(discard1)

        # Recursively solving the subgame G\A, solution comes as (W_0, sigma_0), (W_1, sigma_1)
        sol_player1, sol_player2 = strong_parity_solver_no_strategies(G_A)

        # depending on which player we are considering, assign regions and strategies to the proper variables
        # W'_j is noted W_j, sigma'_j is noted sig_j; the same aplies for jbar
        if j == 0:
            W_j = sol_player1
            W_jbar = sol_player2
        else:
            W_j = sol_player2
            W_jbar = sol_player1

        # if W'_jbar is empty we update the strategies and regions depending on the current player
        # the region and strategy for the whole game for one of the players is empty
        if not W_jbar:
            if j == 0:
                W1.extend(A)
                W1.extend(W_j)
            else:
                W2.extend(A)
                W2.extend(W_j)
        else:
            # compute attractor B and strategy nu
            B, discard1 = reachability.attractor(g, W_jbar, opponent)
            # The subgame G\B is composed of the nodes not in the attractor, so of the opposite player's winning region
            G_B = g.subgame(discard1)

            # recursively solve subgame G\B, solution comes as (W_0, sigma_0), (W_1, sigma_1)
            sol_player1_, sol_player2_ = strong_parity_solver_no_strategies(G_B)

            # depending on which player we are considering, assign regions and strategies to the proper variables
            # W''_j is noted W__j, sigma''_j is noted sig__j; the same aplies for jbar
            if j == 0:
                W__j = sol_player1_
                W__jbar = sol_player2_
            else:
                W__j = sol_player2_
                W__jbar = sol_player1_

            # the last step is to update the winning regions and strategies depending on which player we consider
            if j == 0:
                W1 = W__j

                W2.extend(W__jbar)
                W2.extend(B)

            else:
                W2 = W__j

                W1.extend(W__jbar)
                W1.extend(B)

    return W1, W2

def strong_parity_solver_non_removed(g, removed):
    """
    Strong parity games solver. This algorithm uses a list of non-removed nodes as a way to track sub-games. The
    attractor computation also uses this technique. This is an implementation of the algorithm presented in chapter 5
    of the report.
    :param removed: the removed nodes.
    :param g: the game to solve.
    :return: the solution in the following format : (W_0, sigma_0), (W_1, sigma_1).
    """

    W1 = []  # Winning region of player 0
    W2 = []  # Winning region of player 1
    strat1 = defaultdict(lambda: -1)  # Winning strategy of player 0
    strat2 = defaultdict(lambda: -1)  # Winning strategy of player 1

    # if the game is empty, return the empty regions and strategies
    # removed is a bitarray, count(42) counts the occurrences of True
    if removed.count(42) == len(g.nodes):
        return (W1, strat1), (W2, strat2)

    else:
        i = ops.max_priority_non_removed(g, removed)  # get max priority occurring in g
        # determining which player we are considering, if i is even : player 0 and else player 1
        if i % 2 == 0:
            j = 0
        else:
            j = 1

        opponent = ops.opponent(j)  # getting the opponent of the player

        U = ops.i_priority_node_non_removed(g, i, removed)  # target set for the attractor : nodes of priority i

        # getting the attractor A and the attractor strategy tau and discarding the region and strategy for the opponent
        (A, tau1), (discard1, discard2) = reachability.reachability_solver_non_removed(g, U, j, removed)

        # The subgame G\A is composed of the nodes not in the attractor, thus the nodes of the opposite player's region
        copy_removed1 = bitarray(removed)
        for nodes in A:
            copy_removed1[nodes] = True
        # Recursively solving the subgame G\A, solution comes as (W_0, sigma_0), (W_1, sigma_1)
        sol_player1, sol_player2 = strong_parity_solver_non_removed(g, copy_removed1)

        # depending on which player we are considering, assign regions and strategies to the proper variables
        # W'_j is noted W_j, sigma'_j is noted sig_j; the same aplies for jbar
        if j == 0:
            W_j, sig_j = sol_player1
            W_jbar, sig_jbar = sol_player2
        else:
            W_j, sig_j = sol_player2
            W_jbar, sig_jbar = sol_player1

        # if W'_jbar is empty we update the strategies and regions depending on the current player
        # the region and strategy for the whole game for one of the players is empty
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
            # compute attractor B and strategy nu
            (B, nu), (discard1, discard2) = reachability.reachability_solver_non_removed(g, W_jbar, opponent, removed)
            # The subgame G\B is composed of the nodes not in the attractor, so of the opposite player's winning region
            copy_removed2 = bitarray(removed)
            for nodes in B:
                copy_removed2[nodes] = True

            # recursively solve subgame G\B, solution comes as (W_0, sigma_0), (W_1, sigma_1)
            sol_player1_, sol_player2_ = strong_parity_solver_non_removed(g, copy_removed2)

            # depending on which player we are considering, assign regions and strategies to the proper variables
            # W''_j is noted W__j, sigma''_j is noted sig__j; the same aplies for jbar
            if j == 0:
                W__j, sig__j = sol_player1_
                W__jbar, sig__jbar = sol_player2_
            else:
                W__j, sig__j = sol_player2_
                W__jbar, sig__jbar = sol_player1_

            # the last step is to update the winning regions and strategies depending on which player we consider
            if j == 0:
                W1 = W__j
                strat1 = sig__j

                W2.extend(W__jbar)
                W2.extend(B)
                # nu is defined on W_jbar and must be replaced on W_jbar by the strategy sig_jbar
                # the replacement is implicit because updating sig_jbar last will overwrite already defined strategy
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

    return (W1, strat1), (W2, strat2)


def symbolic_strong_parity_solver(graph, nbr_nodes,increment):
    """
    Solves the parity game g symbolically using antichains.
    :param nbr_nodes: number of nodes in the graph.
    :param graph: a game graph in C format.
    :return: the winning regions W0 and W1 in g.
    """
    W0 = []
    W1 = []

    res = winning_region_c(graph)

    # winning regions returns an array of integers, 1 if node is won by player 0 and 0 if won by player 1
    for i in range(nbr_nodes):
        if res[i] == 1:
            W0.append(i+increment)
        elif res[i] == 0:
                W1.append(i+increment)
    return W0, W1


def up(node, priority, max_counter):
    # When doing up function we need to return something special when the node is in overflow
    concerned_counter = priority // 2

    if (priority % 2 == 0):
        # reset the first to 0
        succ = (concerned_counter)*"0"+node[concerned_counter:]
    else:
        # First value is the node so we need to offset to get the counters, if max counter we return
        if (node[concerned_counter] == max_counter[concerned_counter]):
            # The overflow node is this, its a sink
            return "-"
        else:
            succ = node[:concerned_counter] + str(int(node[concerned_counter])+1) + node[concerned_counter+1:]

    return succ
print(up("0",2,"2"))


def createSafetyGame(previous_graph,start_nodes, max_counter):
    """

    :param previous_graph: Needed for priorities + node info
    :type previous_graph: Graph
    :param start_nodes: start of the algo
    :param nbr_counters: needed for operations
    :return:
    """
    #overlfow node is in it by default
    queue = deque()
    #append
    #popleft
    fill = defaultdict(lambda: -1)
    g = Graph()
    g.add_node("-",(0,0))
    for node_safety in start_nodes:
        queue.append(node_safety)
        fill[node_safety] = 1
    while queue:
        node_safety = queue.popleft()
        node_parity = int(node_safety[0])
        g.add_node(node_safety,previous_graph.get_nodes_descriptors()[node_parity])

        for succ in previous_graph.get_successors(node_parity):
            successor_safety_counter = up(node_safety[1:],previous_graph.get_node_priority(node_parity), max_counter)
            if (successor_safety_counter == "-"):
                successor_safety = successor_safety_counter
            else:
                # If not the infinity sink and not already considered in the queue (this is not opti)
                successor_safety = str(succ) + successor_safety_counter

                if (fill[successor_safety] != 1):
                    fill[successor_safety] = 1
                    queue.append(successor_safety)

            g.add_successor(node_safety, successor_safety)
            g.add_predecessor(successor_safety, node_safety)
    return g



def reduction_to_safety_parity_solver(graph):
    # First we find out the number of counters necessary
    maximum = -1

    for node in graph.get_nodes():
        if (graph.get_node_priority(node) > maximum):
            maximum = graph.get_node_priority(node)
    if maximum%2 == 0:
        maxOdd = maximum-1
    else:
        maxOdd = maximum

    nbr_counters = (maxOdd//2)+1

    max_counter = [0]*nbr_counters

    for node in graph.get_nodes():
        if (graph.get_node_priority(node) % 2 != 0):
            position = graph.get_node_priority(node) // 2
            max_counter[position] = max_counter[position]+1

    # Then we build the start counter for each node, we only build the part reachable by (v, 0, ..., 0) for all v
    # For convenience, we label the nodes as follows : (v, c_1, c_2, ..., c_d) is labeled vc_1c_2...c_d
    # nodes are string isntead of int so we can get access with [index]
    # This is a unique identifier for each node. The overflow is simply written "-" and added to the target set directly

    # Max counter is also a string
    max_counter = ''.join(str(x) for x in max_counter)

    start_nodes = []
    for node in graph.get_nodes():
        start_nodes.append(str(node)+"0"*nbr_counters)
    print("max "+str(max_counter))
    transformed_graph = createSafetyGame(graph, start_nodes, max_counter)

    W1bis, W2bis = reachability.attractor(transformed_graph,["-"],1)
    W1 = []
    W2 = []

    empty_counters = "0"*nbr_counters
    for node in W1bis:
        if node[1:] == empty_counters:
            W1.append(int(node[0]))
    for node in W2bis:
        if node[1:] == empty_counters:
            W2.append(int(node[0]))
    return W1, W2
    # We solve this safety game by computing the attractor of the nodes in overflow for player 2.

    # We check if (v, 0, ..., 0) is in the attractor, if so player 2 wins else player 1 wins

g =  Graph()
g.add_node(3,(0,1))
g.add_node(1,(1,1))
g.add_node(2,(0,2))
g.add_successor(3,1)
g.add_predecessor(1,3)

g.add_successor(1,3)
g.add_predecessor(3,1)

g.add_successor(2,1)
g.add_predecessor(1,1)

g.add_successor(1,2)
g.add_predecessor(2,1)
import tools.file_handler as io

g = io.load_from_file("../assets/strong parity/example_3.txt")
#return (a == [2, 1, 3, 4]) and b == {4: 4, 2: 4, 1: 2} and c == [6, 7, 5] and d == {7: 6, 6: 6, 5: 6}

test = reduction_to_safety_parity_solver(g)
print( test)
"""
from tools.file_handler import load_from_file
from tools.operations import are_lists_equal

g = load_from_file("../assets/strong parity/example_3.txt")
graph, nbr_nodes = ops.transform_graph_into_c(g)

solution_symbolic = symbolic_strong_parity_solver(graph, nbr_nodes)
solution_regular = strong_parity_solver_no_strategies(g)
print(str(are_lists_equal(solution_regular[0], solution_symbolic[0]))+" | "+str(are_lists_equal(solution_regular[1], solution_symbolic[1])))
"""


