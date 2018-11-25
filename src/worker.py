import torch

import random
from collections import deque

from architecture import Arch
from population import Population
from model import Model
from nn_tools import *


class Worker():
    """Used to select, mutate, evolve populations"""

    def __init__(self, population, population_size_setpoint):
        """

        :type population: Population
        """
        self._population_size_setpoint = population_size_setpoint
        self.population = population

    def _population_size(self):
        return len(self.population)

    def select(self):
        """
        Return the available individuals.
        :rtype: DNA
        """
        pass

    def _edge_mutation(self):
        pass

    def _vertex_mutation(self):
        pass

    def mutation(self, dna):
        """
        Return the mutated dna.
        :rtype: DNA
        """
        pass

    def evolve(self):
        total_population_num = self._population_size_setpoint
        cycles = 50
        sample_size = 5

        population = deque()
        history = []

        while len(history) < cycles:
            sample = random.sample(population, sample_size)
            parent = max(sample, key=lambda x: x.accuracy)
            child = Model(self.mutation(parent.dna))
            child.accuracy = train_and_eval(child)

            population.append(child)
            history.append(child)
            # reserve best //TODO
            # 轮盘
            population.popleft()

        return max(history, key=lambda x: x.accuracy)


def test(a):
    print("training", a.id)
    model = Model(a.arch, 1)
    acc = train_and_eval(model)
    return acc


if __name__ == '__main__':
    a = Arch.random_arch()

    acc = test(a)
    print(acc)

    # out = cell(data1, data2)
    # print(out)
