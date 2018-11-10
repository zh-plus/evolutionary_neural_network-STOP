import random


class Architecture:
    def __init__(self):
        self.arch = []  # normal(0) or reduction(1)


class Cell:
    def __init__(self):
        self.type = None  # normal(0) or reduction(1)
        self.nodes = self.initialize_nodes()

    def initialize_nodes(self):
        nodes = [Node(0), Node(0)]
        for x in range(5):
            nodes.append(Node(1))
        nodes.append(Node(2))
        return nodes


class Edge:
    OPTYPE = ['identical', 'sep_3x3', 'sep_5x5', 'sep_7x7', 'avg_3x3', 'max_3x3', 'dil_3x3', 'sep_1x7_7x1']

    def __init__(self, optype, node):
        self.op = optype
        self.enter_node = node


class Node:
    left_edge: Edge

    def __init__(self, type):
        self.type = type  # 0 for input, 1 for intermediate, 2 for output
        self.left_edge = None
        self.right_edge = None
        if type == 2:
            self.out_enter_edge = []
        self.out = None


def random_architecture():
    architecture = Architecture()

    for i in range(0, 5):  # five cells

        cell = Cell()
        if i % 2 == 0:
            cell.type = 0  # normal
        else:
            cell.type = 1  # reduction
        for p in range(2, 7):  # every pairwise combinations
            x, y = random.sample(range(p), k=2)
            node = cell.nodes[p]
            cell.nodes[x].out = True
            cell.nodes[y].out = True

            left_op = random.sample(Edge.OPTYPE, k=1)[0]
            node.left_edge = Edge(left_op, x)
            right_op = random.sample(Edge.OPTYPE, k=1)[0]
            node.right_edge = Edge(right_op, y)
            cell.nodes[p] = node

        for j in range(2, 7):
            if not cell.nodes[j].out:
                cell.nodes[-1].out_enter_edge.append(cell.nodes[j])

        architecture.arch.append(cell)

    return architecture


def mutate_arch(parent_arch):
    """Computes the architecture for a child of the given parent architecture.

    """
    return 0
