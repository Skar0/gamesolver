import copy

import reachability
from tools import operations as ops


def transform_game(g, k):
    """
    Transforms a game as a pre-processing to the generalized parity games solver.
    Every priority function is "complemented" (each priority is incremented by 1)
    :param g: the game to complement
    :param k:
    :return: the compemented game
    """
    g_copy = copy.deepcopy(g) # Deep copy of the game g
    descriptors = g_copy.get_nodes_descriptors() # Descriptors of the nodes (player, priority_1, ..., priority_k)
    # For each node, get the descriptor and update the descriptor by adding 1 to each priority
    for node in g_copy.get_nodes():
        current = descriptors[node]
        descriptors[node] = tuple([current[0]]+map(lambda x: x+1, current[1:]))
    return g_copy


def disj_parity_win2(g, maxValues, k, u):
    """
    Recursive solver for generalized parity games. Uses the algorithm presented in
    http://www2.eecs.berkeley.edu/Pubs/TechRpts/2006/EECS-2006-144.html
    This is used for testing purposes.
    :param g: the game to solve
    :param maxValues: the maximum value for each priority function
    :param k: the number of priority functions
    :param u: integer for testing purposes
    :return: W1, W2 the winning regions in the game for player 1 and player 2 (for the base game)
    """

    # Base case : all maxValues are 1 or the game is empty
    if all(value == 1 for value in maxValues) or len(g.nodes) == 0:
        #print(str(u*2*" ")+"it-"+str(u)+" return on base case")
        return g.get_nodes(), []


    for i in range(k):
        max = ops.max_priority(g)
        if max %2== 0:
            even = max
            attMaxOdd, compl_attMaxOdd = [], []
            #print(str(u*2*" ")+"it-"+str(u)+" maxOdd-"+str(maxValues[i])+" attMaxOdd-"+str(attMaxOdd)+" "+"complAttMaxOdd-"+str(compl_attMaxOdd))
            G1 = g
            attMaxEven, compl_attMaxEven = reachability.attractor(G1,  ops.i_priority_node_function_j(G1, max,i+1),1)
            #print(str(u*2*" ")+"it-"+str(u)+" maxEven-"+str(maxValues[i]-1)+" attMaxEven-"+str(attMaxEven)+" "+"complAttMaxEven-"+str(compl_attMaxEven))
            H1 = G1.subgame(compl_attMaxEven)
            j = 0
            #print(str(u*2*" ")+"it-"+str(u)+" G\n"+str(G1))
            #print(str(u*2*" ")+"it-"+str(u)+" H\n"+str(H1))
        else:
            even = max-1
            attMaxOdd, compl_attMaxOdd = reachability.attractor(g,
                                                                ops.i_priority_node_function_j(g, max, i + 1),
                                                                0)
            # print(str(u*2*" ")+"it-"+str(u)+" maxOdd-"+str(maxValues[i])+" attMaxOdd-"+str(attMaxOdd)+" "+"complAttMaxOdd-"+str(compl_attMaxOdd))
            G1 = g.subgame(compl_attMaxOdd)
            attMaxEven, compl_attMaxEven = reachability.attractor(G1,
                                                                  ops.i_priority_node_function_j(G1, max - 1,
                                                                                                 i + 1), 1)
            # print(str(u*2*" ")+"it-"+str(u)+" maxEven-"+str(maxValues[i]-1)+" attMaxEven-"+str(attMaxEven)+" "+"complAttMaxEven-"+str(compl_attMaxEven))
            H1 = G1.subgame(compl_attMaxEven)
            j = 0
            # print(str(u*2*" ")+"it-"+str(u)+" G\n"+str(G1))
            # print(str(u*2*" ")+"it-"+str(u)+" H\n"+str(H1))
        while True:

            j+=1
            copy_maxValues = copy.copy(maxValues)
            copy_maxValues[i] -= even-1
            W1, W2 = disj_parity_win2(H1, copy_maxValues, k,u+1)
            #print(str(u * 2 * " ") + "it-" + str(u)+"-"+str(j) + " W1-" + str(W1) + " W2-" + str(W2))

            #print("W1 "+str(W1))
            #print("W2 "+str(W2))
            #print("game " + str(g) + "att " + str(attMaxOdd) + "compl " + str(compl_attMaxOdd))
            #print("stop "+str(set(W2))+" "+str(set(H1.get_nodes()))+" val "+ str(set(W2) == set(H1.get_nodes())))
            #break

            # cette cond etait en dessous de lautre et lautre prennait precedence quand on avait les 2
            #print(len(G1.nodes))
            if len(G1.nodes) == 0:
                #print("G empty")
                break

            if set(W2) == set(H1.get_nodes()):
                #print("hello")
                B, compl_B = reachability.attractor(g,  G1.get_nodes(),1)
                W1, W2 = disj_parity_win2(g.subgame(compl_B), maxValues, k, u+1)
                #print("re "+str(B)+" "+str(W1)+" "+str(W2))
                B.extend(W2)
                return W1, B
            #break
            T, compl_T = reachability.attractor(G1, W1,0)
            G1 = G1.subgame(compl_T)
            E, compl_E = reachability.attractor(G1, ops.i_priority_node_function_j(g, even,i+1),0)
            H1 = G1.subgame(compl_E)
            #break
        #break
    return g.get_nodes(), []

def disj_parity_win(g, maxValues, k, u):
    """
    Recursive solver for generalized parity games. Implements the classical algorithm which solves generalized parity
    games.
    :param g: the game to solve
    :param maxValues: the maximum value according to each priority function
    :param k: the number of priority functions
    :param u: integer for testing purposes
    :return: W1, W2 the winning regions in the game for player 1 and player 2 (for the original game, without complement)
    """

    # Base case : all maxValues are 1 or the game is empty
    if all(value == 1 for value in maxValues) or len(g.nodes) == 0:
        return g.get_nodes(), []


    for i in range(k):
        attMaxOdd, compl_attMaxOdd = reachability.attractor(g, ops.i_priority_node_function_j(g, maxValues[i],i+1),0)
        G1 = g.subgame(compl_attMaxOdd)
        attMaxEven, compl_attMaxEven = reachability.attractor(G1,  ops.i_priority_node_function_j(G1, maxValues[i]-1,i+1),1)
        H1 = G1.subgame(compl_attMaxEven)
        j = 0
        while True:
            j+=1
            copy_maxValues = copy.copy(maxValues)
            copy_maxValues[i]-=2
            W1, W2 = disj_parity_win(H1, copy_maxValues, k,u+1)

            if len(G1.nodes) == 0:
                break

            if set(W2) == set(H1.get_nodes()):
                B, compl_B = reachability.attractor(g,  G1.get_nodes(),1)
                W1, W2 = disj_parity_win(g.subgame(compl_B), maxValues, k, u+1)
                B.extend(W2)
                return W1, B

            T, compl_T = reachability.attractor(G1, W1,0)
            G1 = G1.subgame(compl_T)
            E, compl_E = reachability.attractor(G1, ops.i_priority_node_function_j(g, maxValues[i]-1,i+1),0)
            H1 = G1.subgame(compl_E)
    return g.get_nodes(), []


def generalized_parity_solver(g):
    """
    Generalized parity games solver. This is an implementation of the classical algorithm used to solve generalized
    parity games. This is the wrapper function which complements every priority and calls the actual algorithm.
    :param g: the arena of the generalized parity game
    :return: the solution in the following format : W_0, W_1
    """

    # nbr of functions is the length of the descriptor minus 1 (because the descriptor contains the player)
    nbrFunctions = len(g.get_nodes_descriptors()[g.get_nodes()[0]])-1
    # Transforming the game
    transformed = transform_game(g, nbrFunctions)
    # Initializing the max values list
    maxValues = [0]*nbrFunctions

    # Getting the maximum value according to each priority function
    descriptors = transformed.get_nodes_descriptors()

    # Get the maximal priority in the game according to every priority function.
    for node in transformed.get_nodes():
        current = descriptors[node]
        for i in range(1,nbrFunctions+1):
            if current[i] > maxValues[i-1]:
                maxValues[i-1] = current[i]

    # Max values need to be odd, if some are even, add 1
    for i in range(0, nbrFunctions ):
        if maxValues[i] % 2 == 0:
            maxValues[i]+=1

    return disj_parity_win(transformed,maxValues, nbrFunctions,0)

def generalized_parity_solver_nocall(g):
    """
    Generalized parity games solver. This is an implementation of the classical algorithm used to solve generalized
    parity games. This is the wrapper function which complements every priority but does not calls the actual algorithm.
    This is used for benchmarking purposes
    :param g: the arena of the generalized parity game
    :return: the solution in the following format : W_0, W_1
    """

    # nbr of functions is the length of the descriptor minus 1 (because the descriptor contains the player)
    nbrFunctions = len(g.get_nodes_descriptors()[g.get_nodes()[0]])-1
    # Transforming the game
    transformed = transform_game(g, nbrFunctions)
    # Initializing the max values list
    maxValues = [0]*nbrFunctions

    # Getting the maximum value according to each priority function
    descriptors = transformed.get_nodes_descriptors()

    for node in transformed.get_nodes():
        current = descriptors[node]
        for i in range(1,nbrFunctions+1):
            if current[i] > maxValues[i-1]:
                maxValues[i-1] = current[i]

    # Max values need to be odd, if some is even, add 1
    for i in range(0, nbrFunctions ):
        if maxValues[i] % 2 == 0:
            maxValues[i]+=1

    return transformed,maxValues, nbrFunctions,0