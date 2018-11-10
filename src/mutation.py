import copy
import random
from architecture import *
from worker import *

OPTYPE = ['identical', 'sep_3x3', 'sep_5x5', 'sep_7x7', 'avg_3x3', 'max_3x3', 'dil_3x3', 'sep_1x7_7x1']


class OpMutation(object):

    def mutate(self, architecture):
        arch = architecture.arch
        mutaed_cell = arch[random.randint(0, 1)]
        mutaed_nodes = mutaed_cell.nodes[random.randint(2, 7)]
        mutaed_edge = self.getMutationEdge(mutaed_nodes)
        print('mutate op:', mutaed_edge.op if mutaed_edge else 'None')
        mutaed_edge.op = self.getMutationOp(mutaed_edge)
        print('mutated op', mutaed_edge.op)

    def getMutationEdge(self, mutaed_pairwise):
        s = random.randint(0, 1)
        edge = None
        if s == 0:
            edge = mutaed_pairwise.left_edge
        else:
            edge = mutaed_pairwise.right_edge
        return edge

    def getMutationOp(self, mutaed_edge):
        a = random.choice(OPTYPE)
        while mutaed_edge.op and a == mutaed_edge.op:
            a = random.choice(OPTYPE)
        return a


class HidenStateMutation(object):

    def mutate(self, architecture):
        arch = architecture.arch
        mutaed_cell = arch[random.randint(0, 1)]
        mutaed_nodes = mutaed_cell.nodes[random.randint(2, 7)]
        mutaed_edge = self.getMutationEdge(mutaed_nodes)
        get_orgin_node = mutaed_edge.enter_node
        mutaed_edge.enter_node = self.getMutationNode(mutaed_edge, mutaed_cell)

    def getMutationEdge(self, mutaed_pairwise):
        s = random.randint(0, 1)
        edge = None
        if s == 0:
            edge = mutaed_pairwise.left_edge
        else:
            edge = mutaed_pairwise.right_edge
        return edge

    def getMutationNode(self, mutaed_edge, cell):
        a = random.randint(0, 6)
        while cell.nodes[a] == mutaed_edge.enter_node:
            a = random.randint(0, 6)
        node = cell.nodes[a]
        return node