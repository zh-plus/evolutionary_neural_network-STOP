import torch

import random
from collections import deque

from architecture import Arch
from population import Population
from model import Model
from nn_tools import *
from file_system import Folder, load_path, read_file, test_dir
from mutation import Mutation


class Worker:
    """Used to select, mutate, evolve populations"""

    def __init__(self, population_size_setpoint):
        self._population_size_setpoint = population_size_setpoint
        self.population = self.initialize_population(population_size_setpoint)
        self.history = self.population.get_history()

    def select(self):
        """
        Return the available individuals.
        :rtype: DNA
        """
        pass

    def mutation(self, dna):
        mutations = [Mutation.hidenStateMutate, Mutation.opMutate]
        mutation = random.choice(mutations)
        return mutation(dna)

    @staticmethod
    def initialize_population(population_size_setpoint):
        print("Welcome to auto-ML!")
        # deal with path
        path = "Store"
        test_dir(path)
        folder = Folder(path)
        p = Population(folder, population_size_setpoint)

        return p

    def evolve(self):
        cycles = 7
        sample_size = 2

        population = self.population
        history = self.history
        print("the generation number is:", population.gen_num)
        while population.gen_num < cycles:
            sample = random.sample(population.individuals, sample_size)
            parent_architecture = max(sample, key=lambda x: x.accuracy)
            lowest = min(population.individuals, key=lambda x: x.accuracy)

            # mutation

            while True:
                child_architecture = self.mutation(parent_architecture)
                child_model = Model(child_architecture)
                child_model.accuracy = train_and_eval(child_model)
                child_architecture.accuracy = child_model.accuracy
                # check whether it is acceptable
                if child_model.accuracy >= lowest.accurancy:
                    break

            population.add(child_architecture)
            history.append(child_architecture)
            # reserve best //TODO
            # 轮盘
            population.dead()
            population.gen_num += 1


if __name__ == '__main__':
    worker = Worker(4)
    worker.evolve()
    best = worker.population.get_best()
    print(best.arch)
    print(best.accuracy)
