import copy
import random
from architecture import *


class Mutation(object):
    OPTYPE = ['identical', 'sep_3x3', 'sep_5x5', 'sep_7x7', 'bn', 'dil_3x3', 'sep_1x7_7x1']

    @staticmethod
    def opMutate(architecture):
        choose_cell = random.randint(0, 1)
        mutated_cell = architecture.arch[choose_cell]
        choose_node = random.randint(0, 4)
        mutated_nodes = mutated_cell[choose_node]
        op = ''
        p = random.random() * 100
        if p <= 5:
            op = Mutation.OPTYPE[0]
        else:
            ran = random.randint(1, 6)
            op = Mutation.OPTYPE[ran]

        mutated_nodes[random.randint(0, 1)] = op

    @staticmethod
    def hidenStateMutate(architecture):
        arch = architecture.arch
        choose_cell = random.randint(0, 1)
        mutated_cell = arch[choose_cell]
        choose_node = random.randint(0, 4)
        mutated_nodes = mutated_cell[choose_node]
        select_Hiden_num = random.randint(2, 3)
        get_orgin_num = mutated_nodes[select_Hiden_num]
        change_num = random.randint(0, choose_node + 1)
        while get_orgin_num == change_num:
            change_num = random.randint(0, choose_node + 1)
        mutated_nodes[select_Hiden_num] = change_num
        # change node7
        if change_num in mutated_cell[-1]:
            mutated_cell[-1].remove(change_num)
        # whether orgin_num in node
        is_point_to_node7 = True
        for i in mutated_cell:
            if get_orgin_num in i:
                is_point_to_node7 = False
                break
        if is_point_to_node7:
            mutated_cell[-1].append(get_orgin_num)
