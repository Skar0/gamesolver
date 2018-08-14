from collections import defaultdict


class Graph(object):
    """
    Class holding the data structure representing the game graph and implementing a few useful operations on that graph.
    """

    def __init__(self):
        """
        Graphs are represented by predecessors list (a dictionary whose keys are the nodes and values are a list of
        successors of a nodes). Access in a dictionary is O(1) in average and O(n) in worst case because it uses a
        hash table. Python lists provide O(1) retrieval. The same applies to successors list. Nodes are stored in a
        dictionary where the key is the node id and the value is a tuple (player, priority).
        """
        self.predecessors = defaultdict(list)
        self.successors = defaultdict(list)
        self.nodes = defaultdict(tuple)

    def get_nodes_descriptors(self):
        """
        :return: the dictionary containing the node information
        """
        return self.nodes

    def get_nodes(self):
        """
        :return: returns the list of every node in the games
        """
        return self.nodes.keys()

    def get_node_player(self, node):
        """
        :param node: a node id
        :return: the player to which a node belongs
        """
        return self.nodes[node][0]

    def get_node_priority(self, node):
        """
        :param node: a node id
        :return: the priority of the node (or the first one in case of generalized parity)
        """
        return self.nodes[node][1]

    def get_node_priority_function_i(self, node, i):
        """
        Retrieves the priority of a node according to priority function i.
        :param node: the node id
        :param i: the priority function (1 to k)
        :return: the priority of the node according to priority function i
        """
        return self.nodes[node][i]

    def add_node(self, node, info):
        """
        :param node: a node id
        :param info: a tuple (player, priority) or (player, priority_1, ..., priority_k)
        """
        self.nodes[node] = info

    def remove_node(self, node):
        del self.nodes[node]

    def get_successors(self, node):
        """
        :param node: a node id
        :return: the list of successors of the node
        """
        return self.successors[node]

    def add_successor(self, node, successor):
        self.successors[node].append(successor)

    def remove_successor(self, node, successor):
        self.successors[node].remove(successor)

    def get_predecessors(self, node):
        """
        :param node: a node id
        :return: the list of predecessors of the node
        """
        return self.predecessors[node]

    def add_predecessor(self, node, predecessor):
        self.predecessors[node].append(predecessor)

    def remove_predecessor(self, node, predecessor):
        self.predecessors[node].remove(predecessor)

    def subgame(self, set):
        """
        Creates a sub-game from the current game. The sub-game will contain all nodes in the provided set.
        :param set: the list of nodes that the sub-game will contain.
        :return: a sub-game.
        """
        sub = self.__class__()
        for n in set:
            sub.nodes[n] = self.nodes[n]
        for n in sub.nodes:
            for succ in self.successors[n]:
                if succ in sub.nodes:
                    sub.successors[n].append(succ)
                    sub.predecessors[succ].append(n)
        return sub

    def __str__(self):
        rep = ""
        for node in self.nodes:
            rep += str(node) + " " + str(self.nodes[node]) + "\n" + str(node) + " -> "
            for succ in self.successors[node]:
                rep += str(succ) + ", "
            rep += "\n"
        return rep
