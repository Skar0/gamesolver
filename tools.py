from graph import Graph


# def load_from_file2(self, path):
#     with open(path, 'r') as f:
#         for line in f:
#             split_line = line.strip().strip(";").replace(" ", "").split("->")
#             if (split_line[0] != '}' and split_line[0] != "digraphG{"):
#                 print(split_line)
#                 self.add_predecessor(split_line[1], split_line[0])
#                 self.add_successor(split_line[0], split_line[1])
#         self.nodes = self.successors.keys()
#         f.close()


def load_from_file(path):
    with open(path, 'r') as f:
        g = Graph()
        for line in f:
            if (line == "#\n"):
                break
            else:
                split_line = line.strip().split(" ")
                g.add_node(split_line[0], (split_line[1], split_line[2]))
        for line in f:
            split_line = line.strip().split("->")
            for succ in split_line[1].split(","):
                g.add_successor(split_line[0], succ)
                g.add_predecessor(succ, (split_line[0]))

    return g


def write_to_file(g, path):
    with open(path, 'w') as f:
        f.write("digraph G {\n")
        for node in g.get_nodes():
            print(g.get_node_player(node))
            to_write = str(node) + "[label=\"" + str(node) + " " + g.get_node_priority(node)+"\""
            if g.get_node_player(node) == "1":
                to_write += ",shape=circle"
            elif g.get_node_player(node) == "2":
                to_write += ",shape=box"
            else:
                pass
                # error

            if g.get_node_region(node) == "1":
                to_write += ",color=blue"
            elif g.get_node_region(node) == "2":
                to_write += ",color=green"
            else:
                pass
                # error

            to_write += "];\n"

            for succ in g.successors[node]:
                to_write += str(node) + " -> " + str(succ)

                if succ == g.get_node_strategy(node):
                    if g.get_node_player(node) == "1":
                        to_write += '[color=blue]\n'
                    elif g.get_node_player(node) == "2":
                        to_write += '[color=green]\n'
                    else:
                        pass
                        #error
                else:
                    to_write += ";\n"
            f.write(to_write)

        f.write('}')


# def write_to_file2(self, path):
#     with open(path, 'w') as f:
#         f.write("digraph G {\n")
#         for node in self.successors.keys():
#             if (self.regions[node] == 0):
#                 f.write(str(node) + '[color=blue];\n')
#             else:
#                 f.write(str(node) + '[shape=box,color=green];\n')
#
#             for succ in self.successors[node]:
#                 to_write = str(node) + " -> " + str(succ)
#
#                 is_in_strategy = succ in self.strategies[node]
#                 # ajouter le joueur auquel il appartient
#                 if (is_in_strategy):
#                     to_write += '[color=blue];\n'
#                 else:
#                     to_write += '[color=green];\n'
#                 f.write(to_write)
#
#         f.write('}')



#g = load_from_file("assets/reachability/fig32.txt")
#write_to_file(g,"assets/trash/test3.dot")
