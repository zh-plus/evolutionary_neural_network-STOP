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
        last_path = load_path()
        response = None
        if last_path != '':
            print("Notice the last visited path is: ", last_path)
            while response not in ('y', 'n'):
                response = input("Do you want to use that?(y/n): ").lower()
            if response == 'y':
                last_path = test_dir(last_path)
        if response == 'n' or last_path == '' or response is None:
            last_path = input("Please choose a new path: ")
            last_path = test_dir(last_path)

        last_path = test_dir(last_path)
        folder = Folder(last_path)
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
            child_architecture = self.mutation(parent_architecture)
            child_model = Model(child_architecture)
            child_model.accuracy = train_and_eval(child_model)

            population.add(child_architecture)
            history.append(child_architecture)
            # reserve best //TODO
            # 轮盘
            population.dead()
            population.gen_num += 1


def test(a):
    print("training", a.id)
    model = Model(a.arch, 1)
    acc = train_and_eval(model)
    return acc


if __name__ == '__main__':
    worker = Worker(4)
    worker.evolve()
    best = worker.population.get_best()
    print(best.arch)
    print(best.accuracy)
