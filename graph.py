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

        # TODO remove as this is created by the solving algorithms
        self.regions = defaultdict(lambda: -1)
        self.strategies = defaultdict(lambda: -1)

    def get_nodes(self):
        return self.nodes.keys()

    def get_node_player(self, node):
        return self.nodes[node][0]

    def get_node_priority(self, node):
        return self.nodes[node][1]

    def get_regions(self):
        return self.regions

    def get_node_region(self, node):
        return self.regions[node]

    def set_node_region(self, node, player):
        self.regions[node] = player

    def get_node_strategy(self, node):
        return self.strategies[node]

    def set_node_strategy(self, node, move):
         self.strategies[node] = move

    def get_strategies(self):
        return self.strategies

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
            rep+=str(node)+" "+str(self.nodes[node])+"\n"+str(node)+" -> "
            for succ in self.successors[node]:
                rep+= str(succ)+", "
            rep+="\n"
        return rep
