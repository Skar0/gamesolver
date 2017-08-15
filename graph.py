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

    def get_nodes(self):
        return self.nodes.keys()

    def get_node_player(self, node):
        return self.nodes[node][0]

    def get_node_priority(self, node):
        return self.nodes[node][1]

    def add_node(self, node, info):
        self.nodes[node] = info

    def remove_node(self, node):
        del self.nodes[node]

    def get_successors(self, node):
        return self.successors[node]

    def add_successor(self, node, successor):
        self.successors[node].append(successor)

    def remove_successor(self, node, successor):
        self.successors[node].remove(successor)

    def get_predecessors(self, node):
        return self.predecessors[node]

    def add_predecessor(self, node, predecessor):
        self.predecessors[node].append(predecessor)

    def remove_predecessor(self, node, predecessor):
        self.predecessors[node].remove(predecessor)

    def subgame(self, set):
        """
        Creates a subgame from the current game. The subgame will contain all nodes in the provided set.
        :param set: the list of nodes that the subgame will contain.
        :return: a subgame.
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
