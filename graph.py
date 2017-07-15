from collections import defaultdict


class Graph(object):
    """
    Class holding the data structure representing the graph and implementing a few useful operations
    """

    def __init__(self):
        """
        Graphs are represented by predecessor list (a dictionary whose keys are the nodes and values are a list of
        successors of a nodes). Access in a dictionnary is O(1) in average and O(n) in worst case because it uses a
        hash table. Python lists provide O(1) retrieval. Nodes are stored in a dictionary with the key being the node id
        and the value being the priority of the node (which defaults to 0 if none is provided).
        """
        self.predecessors = defaultdict(list)
        self.successors = defaultdict(list)
        self.nodes = defaultdict(tuple)

        self.regions = defaultdict(lambda: -1)
        self.strategies = defaultdict(list)

    def get_nodes(self):
        return self.nodes.keys()

    def get_node_player(self, node):
        return self.nodes[node][0]

    def get_node_priority(self, node):
        return self.nodes[node][1]

    def get_node_region(self, node):
        return self.regions[node]

    def get_node_strategy(self, node):
        return self.strategies[node]

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
