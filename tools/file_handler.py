from graph import Graph

"""
This module handles file reading (to load graph) and writing (to write the solution).
"""

def load_from_file(path):
    """
    Loads a game graph from a file specified by the path.
    The file must be in PGSolver format.
    :param path: path to the file.
    :return: a Graph g corresponding to the game graph in the file.
    """
    with open(path, 'r') as f:
        g = Graph()
        next(f)
        for line in f:
            split_line = line.split(" ")
            node = int(split_line[0])
            priority = int(split_line[1])

            if split_line[2] == "0":
                g.add_node(node, (0, priority))
            else:
                g.add_node(node, (1, priority))

            for succ in split_line[3].split(","):
                g.add_successor(node, int(succ))
                g.add_predecessor(int(succ), node)

    return g

def load_generalized_from_file(path):
    """
    Loads a generalized parity game graph from a file specified by the path.
    The file must be in PGSolver format for generalized parity.
    :param path: path to the file.
    :return: a Graph g corresponding to the game graph in the file.
    """
    with open(path, 'r') as f:
        g = Graph()
        next(f)
        for line in f:
            split_line = line.split(" ")
            node = int(split_line[0])
            priorities = []
            for prio in split_line[1].split(","):
                priorities += [int(prio)]
            if split_line[2] == "0":
                g.add_node(node, tuple([0]+priorities))
            else:
                g.add_node(node, tuple([1]+priorities))

            for succ in split_line[3].split(","):
                g.add_successor(node, int(succ))
                g.add_predecessor(int(succ), node)

    return g

def write_solution_to_file(g, solution, player, path):
    """
    Writes the solution of a game in dot format to a file specified by the path.
    Winning region and strategy of player 0 (1) is in blue (green).
    Nodes belonging to player 0 (1) are circles (squares).
    :param g: the game Graph.
    :param solution: if player is 0, expected solution format is (W_0, sigma_0),(W_1, sigma_1). If player is 1, invert.
    :param player: the player to which the first tuple in the solution belongs.
    :param path: the path to the file in which we write the solution.
    """

    if player == 0:
        (W_0, sigma_0), (W_1, sigma_1) = solution
    else :
        (W_1, sigma_1), (W_0, sigma_0) = solution

    with open(path, 'w') as f:
        f.write("digraph G {\n")
        f.write("splines=true;\nsep=\"+10,10\";\noverlap=scale;\nnodesep=0.6;\n")
        for node in W_0:
            to_write = str(node) + "[label=\"v" + str(node) + " " + str(g.get_node_priority(node)) + "\""
            if g.get_node_player(node) == 0:
                to_write += ",shape=circle"
            elif g.get_node_player(node) == 1:
                to_write += ",shape=square"
            else:
                pass
                # error

            to_write += ",color=blue3"
            to_write += "];\n"
            f.write(to_write)

            for succ in g.successors[node]:
                to_write += str(node) + " -> " + str(succ)

                if succ == sigma_0[node]:
                    to_write += '[color=blue3];\n'
                elif succ == sigma_1[node]:
                    to_write += '[color=forestgreen];\n'
                else:
                    to_write += ";\n"
            f.write(to_write)

        for node in W_1:
            to_write = str(node) + "[label=\"v" + str(node) + " " + str(g.get_node_priority(node)) + "\""
            if g.get_node_player(node) == 0:
                to_write += ",shape=circle"
            elif g.get_node_player(node) == 1:
                to_write += ",shape=square"
            else:
                pass
                # error

            to_write += ",color=forestgreen"
            to_write += "];\n"
            f.write(to_write)

            for succ in g.successors[node]:
                to_write += str(node) + " -> " + str(succ)

                if succ == sigma_1[node]:
                    to_write += '[color=forestgreen];\n'
                elif succ == sigma_0[node]:
                    to_write += '[color=blue3];\n'
                else:
                    to_write += ";\n"
            f.write(to_write)

        f.write('}')

def write_solution_to_file_no_strategies(g, W1, W2, path):
    """
    Writes the solution of a parity game in dot format to a file specified by the path.
    Winning region of player 0 (1) is in blue (green).
    Nodes belonging to player 0 (1) are circles (squares).
    :param g: the game Graph.
    :param W1: winning region of player 0 (1).
    :param W2: winning region of player 1 (2).
    :param path: the path to the file in which we write the solution.
    """

    with open(path, 'w') as f:
        f.write("digraph G {\n")
        f.write("splines=true;\nsep=\"+10,10\";\noverlap=scale;\nnodesep=0.6;\n")
        for node in W1:
            to_write = str(node) + "[label=\"v" + str(node) + " " + str(g.get_node_priority(node)) + "\""
            if g.get_node_player(node) == 0:
                to_write += ",shape=circle"
            elif g.get_node_player(node) == 1:
                to_write += ",shape=square"
            else:
                pass
                # error

            to_write += ",color=blue3"
            to_write += "];\n"
            f.write(to_write)

            for succ in g.successors[node]:
                to_write += str(node) + " -> " + str(succ)
                to_write += ";\n"
            f.write(to_write)

        for node in W2:
            to_write = str(node) + "[label=\"v" + str(node) + " " + str(g.get_node_priority(node)) + "\""
            if g.get_node_player(node) == 0:
                to_write += ",shape=circle"
            elif g.get_node_player(node) == 1:
                to_write += ",shape=square"
            else:
                pass
                # error

            to_write += ",color=forestgreen"
            to_write += "];\n"
            f.write(to_write)

            for succ in g.successors[node]:
                to_write += str(node) + " -> " + str(succ)
                to_write += ";\n"
            f.write(to_write)

        f.write('}')

def write_generalized_solution_to_file(g, W1, W2, path):
    """
    Writes the solution of a generalized parity game in dot format to a file specified by the path.
    Winning region of player 0 (1) is in blue (green).
    Nodes belonging to player 0 (1) are circles (squares).
    :param g: the game Graph.
    :param W1: winning region of player 0 (1).
    :param W2: winning region of player 1 (2).
    :param path: the path to the file in which we write the solution.
    """

    with open(path, 'w') as f:
        f.write("digraph G {\n")
        f.write("splines=true;\nsep=\"+10,10\";\noverlap=scale;\nnodesep=0.6;\n")
        for node in W1:
            to_write = str(node) + "[label=\"v" + str(node) + " " + str(g.nodes[node][1:]) + "\""
            if g.get_node_player(node) == 0:
                to_write += ",shape=circle"
            elif g.get_node_player(node) == 1:
                to_write += ",shape=square"
            else:
                pass
                # error

            to_write += ",color=blue3"
            to_write += "];\n"
            f.write(to_write)

            for succ in g.successors[node]:
                to_write += str(node) + " -> " + str(succ)
                to_write += '[color=black];\n'
            f.write(to_write)

        for node in W2:
            to_write = str(node) + "[label=\"v" + str(node) + " " + str(g.nodes[node][1:]) + "\""
            if g.get_node_player(node) == 0:
                to_write += ",shape=circle"
            elif g.get_node_player(node) == 1:
                to_write += ",shape=square"
            else:
                pass
                # error

            to_write += ",color=forestgreen"
            to_write += "];\n"
            f.write(to_write)

            for succ in g.successors[node]:
                to_write += str(node) + " -> " + str(succ)
                to_write += '[color=black];\n'
            f.write(to_write)

        f.write('}')

def write_graph_to_file(g, path):
    """
    Writes a game graph to a file specified by the path in dot format.
    :param g: a game Graph.
    :param path: the file to which we write the graph.
    """

    with open(path, 'w') as f:
        f.write("digraph G {\n")
        for node in g.get_nodes():
            to_write = str(node) + "[label=\"" + str(node) + " " + str(g.get_node_priority(node)) + "\""
            if g.get_node_player(node) == 0:
                to_write += ",shape=circle"
            elif g.get_node_player(node) == 1:
                to_write += ",shape=square"
            else:
                pass
                # error

            to_write += "];\n"

            for succ in g.successors[node]:
                to_write += str(node) + " -> " + str(succ) + ";\n"

            f.write(to_write)

        f.write('}')

"""
g = load_generalized_from_file("../assets/generalized parity/simple_example3.txt")
W1 = [1,2,3]
W2 = [4,5,6]
write_generalized_solution_to_file(g,W1,W2,"test.dot")
"""