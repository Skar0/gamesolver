from collections import defaultdict, deque

from bitarray import bitarray

import reachability
from antichains.library_linker import winning_region_c
from graph import Graph
from tools import operations as ops
from tools.operations import transform_graph_into_c_spec, transform_graph_into_c
import ast

def strong_parity_solver(g):
    """
    Strong parity games solver. This is an implementation of the recursive algorithm used to solve parity games.
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
    Strong parity games solver. This is an implementation of the recursive algorithm used to solve parity games.
    This implementation does not compute the winning strategies (for comparison purpose with other algorithms
    which don't)
    :param g: the game to solve.
    :return: the solution in the following format : (W_0, sigma_0), (W_1, sigma_1).
    """
    W1 = []  # Winning region of player 0
    W2 = []  # Winning region of player 1

    # if the game is empty, return the empty regions
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

        # getting the attractor A and discarding the region for the opponent
        A, discard1 = reachability.attractor(g,U,j)

        # The subgame G\A is composed of the nodes not in the attractor, thus the nodes of the opposite player's region
        G_A = g.subgame(discard1)

        # Recursively solving the subgame G\A, solution comes as (W_0, W_1)
        sol_player1, sol_player2 = strong_parity_solver_no_strategies(G_A)

        # depending on which player we are considering, assign regions to the proper variables
        # W'_j is noted W_j, sigma'_j is noted sig_j; the same aplies for jbar
        if j == 0:
            W_j = sol_player1
            W_jbar = sol_player2
        else:
            W_j = sol_player2
            W_jbar = sol_player1

        # if W'_jbar is empty we update the regions depending on the current player
        # the region for the whole game for one of the players is empty
        if not W_jbar:
            if j == 0:
                W1.extend(A)
                W1.extend(W_j)
            else:
                W2.extend(A)
                W2.extend(W_j)
        else:
            # compute attractor B
            B, discard1 = reachability.attractor(g, W_jbar, opponent)
            # The subgame G\B is composed of the nodes not in the attractor, so of the opposite player's winning region
            G_B = g.subgame(discard1)

            # recursively solve subgame G\B, solution comes as (W_0, W_1)
            sol_player1_, sol_player2_ = strong_parity_solver_no_strategies(G_B)

            # depending on which player we are considering, assign regions to the proper variables
            # W''_j is noted W__j, sigma''_j is noted sig__j; the same aplies for jbar
            if j == 0:
                W__j = sol_player1_
                W__jbar = sol_player2_
            else:
                W__j = sol_player2_
                W__jbar = sol_player1_

            # the last step is to update the winning regions depending on which player we consider
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
    Strong parity games solver. This algorithm is an implementation of the recursive algorithm used to solve parity
    games. It uses a list of non-removed nodes as a way to track sub-games. The attractor computation also uses this
    technique. The value at position i in the list is true if node i is removed from the original game arena.
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
    # if every element in the list is true, every node is removed and the game is empty
    if removed.count(42) == len(g.nodes):
        return (W1, strat1), (W2, strat2)

    else:
        i = ops.max_priority_non_removed(g, removed)  # get max priority occurring in g, considering the removed nodes
        # determining which player we are considering, if i is even : player 0 and else player 1
        if i % 2 == 0:
            j = 0
        else:
            j = 1

        opponent = ops.opponent(j)  # getting the opponent of the player

        # target set for the attractor : nodes of priority i, considering the removed nodes
        U = ops.i_priority_node_non_removed(g, i, removed)

        # getting the attractor A and the attractor strategy tau and discarding the region and strategy for the opponent
        # using the attractor function which considers the non removed nodes
        (A, tau1), (discard1, discard2) = reachability.reachability_solver_non_removed(g, U, j, removed)

        # The subgame G\A is composed of the nodes not in the attractor, thus the nodes of the opposite player's region
        # Copy the bitarray and remove the nodes of the attractor by setting their value to True in the list
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


def strong_parity_antichain_based(graph, start_index):
    """
    Implementation of the antichain-based algorithm for parity games.
    Performs a check on the numbering used in the game graph before transforming it into a C graph
    Performs a call to a C function which implements the backward fixpoint algorithm to solve safety games
    using antichains.
    :param graph: the python game arena of the parity game we want to solve.
    :param start_index: the start index for the numbering of nodes in the game.
    :return: the solution of the parity game with game arena graph
    """
    if (start_index == 1):
        g, nbr_nodes = transform_graph_into_c(graph)
        return symbolic_strong_parity_solver(g, nbr_nodes,1)

    elif (start_index == 0):
        g, nbr_nodes = transform_graph_into_c_spec(graph)
        return symbolic_strong_parity_solver(g, nbr_nodes,0)


def symbolic_strong_parity_solver(graph, nbr_nodes,increment):
    """
    Solves the parity game with game arena graph. Requires the number of nodes in the game and an increment.
    This increment is used when nodes are re-indexed so their numbering starts with 0.
    :param nbr_nodes: number of nodes in the graph.
    :param graph: the game arena of the parity game in C format.
    :return: the winning regions W0 and W1 in the parity game.
    """
    W0 = []
    W1 = []

    res = winning_region_c(graph) # call to the C function which implements the backward fixpoint algorithm
    # The safety game obtained by reduction is solved symbolically using antichains.
    # This algorithm yields the winning regions in the parity game it takes as parameter.

    # winning regions returns an array of integers, 1 if node is won by player 0 and 0 if won by player 1
    for i in range(nbr_nodes):
        if res[i] == 1:
            W0.append(i+increment)
        elif res[i] == 0:
                W1.append(i+increment)
    return W0, W1


def up(node, priority, max_counter):
    """
    Up function as defined in the reduction from parity to safety games.
    :param node: the counters of a node (a list [counter_1, ..., counter_k])
    :param priority: the priority we consider
    :param max_counter: the maximum value for each counter
    :return: the result of up(node, priority)
    """
    # Getting the concerned counter
    concerned_counter = priority // 2

    if (priority % 2 == 0):
        # even priority resets the first few counters to 0
        succ = (concerned_counter)*[0]+node[concerned_counter:]
    else:
        if (node[concerned_counter] == max_counter[concerned_counter]):
            # Counter is in overflow, the result is the overflow special value
            return "-"
        else:
            succ = node[:concerned_counter] + [int(node[concerned_counter])+1] + node[concerned_counter+1:]

    return succ


def createSafetyGame(previous_graph,start_nodes, max_counter):
    """
    Creates the safety game obtained by the reduction from parity to safety games.
    :param previous_graph: the game arena of the parity game
    :type previous_graph: Graph
    :param start_nodes: the starting set of nodes for the construction
    :param max_counter: the maximum value for each counters in the safety game obtained by the reduction
    :return: the arena of the safety game obtained by the reduction
    """
    # node ids in the safety game is the str representation of their list [node_id, counter_1, ..., counter_k]
    queue = deque() # used to track newly added nodes
    size = len(max_counter)
    fill = defaultdict(lambda: -1)  # used to track nodes which are already created
    g = Graph() # the graph of the safety game
    g.add_node("-",(0,0)) # the graph contains the special value used for overflows
    for node_safety in start_nodes:
        queue.append(node_safety) # Adds the node from the starting set to the queue
        node_safety_st = str(node_safety) # String representation of the node ([node_id, counter_1, ..., counter_k])
        fill[node_safety_st] = 1 # the nodes have already been considered
    while queue:
        node_safety = queue.popleft() # remove a node from the queue
        node_parity = int(node_safety[0]) # get the node id in the parity game
        node_safety_st = str(node_safety) # get the string representation of the node in the safety game
        g.add_node(node_safety_st,previous_graph.get_nodes_descriptors()[node_parity]) # Adds the node to the safety game

        # consider every successor of the node using the up function and its successors in the parity game
        for succ in previous_graph.get_successors(node_parity):
            successor_safety_counter = up(node_safety[1:],previous_graph.get_node_priority(node_parity), max_counter)
            # performs the up function on the counters (position 0 is the node id) and correct priority in the safety game
            if (successor_safety_counter == "-"):
                successor_safety = successor_safety_counter
            else:
                # If not the infinity sink and not already considered in the queue
                successor_safety = str([succ] + successor_safety_counter)

                if (fill[successor_safety] != 1):
                    fill[successor_safety] = 1 # if it was not already created, it is now and it is added to the queue
                    queue.append([succ]+successor_safety_counter)

            # adds the newly created successor
            g.add_successor(node_safety_st, successor_safety)
            g.add_predecessor(successor_safety, node_safety_st)
    return g



def reduction_to_safety_parity_solver(graph):
    """
    Main function which solves a parity game by reduction to a safety game
    :param graph: the arena of the parity game
    :return: the winning regions in the parity game
    """
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

    # counts every odd priority
    for node in graph.get_nodes():
        if (graph.get_node_priority(node) % 2 != 0):
            position = graph.get_node_priority(node) // 2
            max_counter[position] = max_counter[position]+1

    # Then we build the start counter for each node, we only build the part reachable from (v, 0, ..., 0) for all v
    # For convenience, we label the nodes using the str representation of their list  : [v, c_1, c_2, ..., c_k]
    # This is a unique identifier for each node.
    # The overflow is simply written "-"

    # Start nodes for construction : (v, 0, ..., 0)
    start_nodes = []
    for node in graph.get_nodes():
        start_nodes.append([node]+[0]*nbr_counters)
    transformed_graph = createSafetyGame(graph, start_nodes, max_counter) # creates the safety game from the start nodes

    W1bis, W2bis = reachability.attractor(transformed_graph,["-"],1) # attractor for player 2 of the nodes in overflow
    W1 = []
    W2 = []

    empty_counters = [0]*nbr_counters # [0, ..., 0]
    # checks if the nodes [v, 0, ..., 0] belongs to the attractor or not and creates the winning regions
    for node in W1bis:
        if node != "-":
            node_list = ast.literal_eval(node)
            if node_list[-nbr_counters:] == empty_counters:
                W2.append(node_list[0])
    for node in W2bis:
        if node != "-":
            node_list = ast.literal_eval(node)
            if node_list[-nbr_counters:] == empty_counters:
                W1.append(node_list[0])
    return W1, W2