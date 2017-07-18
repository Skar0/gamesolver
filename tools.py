from graph import Graph


def load_from_file(path):
    with open(path, 'r') as f:
        g = Graph()
        next(f)
        for line in f:
            split_line = line.split(" ")
            node = int(split_line[0])
            priority = int(split_line[1])

            if split_line[2] == "0":
                g.add_node(node, (1, priority))
            else:
                g.add_node(node, (2, priority))

            for succ in split_line[3].split(","):
                g.add_successor(node, int(succ))
                g.add_predecessor(int(succ), node)

    return g


def write_solution_to_file(g, path):
    with open(path, 'w') as f:
        f.write("digraph G {\n")
        for node in g.get_nodes():
            to_write = str(node) + "[label=\"" + str(node) + " " + str(g.get_node_priority(node)) + "\""
            if g.get_node_player(node) == 1:
                to_write += ",shape=circle"
            elif g.get_node_player(node) == 2:
                to_write += ",shape=square"
            else:
                pass
                # error

            if g.get_node_region(node) == 1:
                to_write += ",color=blue3"
            elif g.get_node_region(node) == 2:
                to_write += ",color=forestgreen"
            else:
                pass
                # error

            to_write += "];\n"

            for succ in g.successors[node]:
                to_write += str(node) + " -> " + str(succ)

                if succ == g.get_node_strategy(node):
                    if g.get_node_player(node) == 1:
                        to_write += '[color=blue3]\n'
                    elif g.get_node_player(node) == 2:
                        to_write += '[color=forestgreen]\n'
                    else:
                        pass
                        # error
                else:
                    to_write += ";\n"
            f.write(to_write)

        f.write('}')


def write_graph_to_file(g, path):
    with open(path, 'w') as f:
        f.write("digraph G {\n")
        for node in g.get_nodes():
            to_write = str(node) + "[label=\"" + str(node) + " " + str(g.get_node_priority(node)) + "\""
            if g.get_node_player(node) == 1:
                to_write += ",shape=circle"
            elif g.get_node_player(node) == 2:
                to_write += ",shape=square"
            else:
                pass
                # error

            to_write += "];\n"

            for succ in g.successors[node]:
                to_write += str(node) + " -> " + str(succ) + ";\n"

            f.write(to_write)

        f.write('}')
