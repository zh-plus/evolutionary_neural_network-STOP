import random
import architecture_pb2


class Arch:
    OPTYPE = ['identical', 'sep_3x3', 'sep_5x5', 'sep_7x7', 'bn', 'dil_3x3', 'sep_1x7_7x1']

    def __init__(self, arch_proto=None):
        self.accuracy = 0
        self.id = 0
        self.arch = []
        if arch_proto:
            for cell_id, cell in enumerate(arch_proto.cells):
                self.arch.append(Cell(cell).nodes)
                self.accuracy = arch_proto.accuracy
            self.accuracy = arch_proto.accuracy
            self.id = arch_proto.id

    def to_proto(self):
        arch_proto = architecture_pb2.ArchProto()
        arch_proto.accuracy = self.accuracy
        arch_proto.id = self.id

        for cell_id, cell in enumerate(self.arch):
            ce = arch_proto.cells.add()    # type of ce is CellProto
            ce.CopyFrom(Cell.to_proto(cell))

        return arch_proto

    def random_arch(self):

        for i in range(0, 2):  # two different type cells
            self.arch.append(Cell.random_cell())


class Cell:

    def __init__(self, cell_proto=None):
        self.nodes = []
        if cell_proto:
            for node in cell_proto.nodes:
                self.nodes.append(Node(node).content)

    @staticmethod
    def to_proto(cell):
        cell_proto = architecture_pb2.CellProto()
        for node in cell:
            co = cell_proto.nodes.add()
            co.CopyFrom(Node.to_proto(node))
        return cell_proto

    @staticmethod
    def random_cell():
        nodes = []
        out = [True, True]  # first two must have output
        for x in range(5):
            out.append(False)

        for p in range(2, 7):  # every pairwise combinations
            node = Node.random_node(p)
            out[node[2]] = True
            out[node[3]] = True
            nodes.append(node)

        nodes.append([])  # node at seven
        for j in range(0, 7):
            if not out[j]:
                nodes[-1].append(str(j))
        return nodes


class Node:

    def __init__(self, node_proto=None):
        self.content = []
        if node_proto:
            for s in node_proto.content:
                self.content.append(s)

    @staticmethod
    def to_proto(content):

        node_proto = architecture_pb2.NodeProto()

        for p in content:
            node_proto.content.append(str(p))
        return node_proto

    @staticmethod
    def random_node(n):

            x, y = random.sample(range(n), k=2)

            left_op = random.choice(Arch.OPTYPE)
            right_op = random.choice(Arch.OPTYPE)

            return [left_op, right_op, x, y]





