from collections import deque
from copy import copy

from architecture import *
from file_system import *
from nn_tools import *
from model import Model


class Population:
    """Use file system to represent population"""

    def __init__(self, folder, population_size_setpoint):

        # initial a List[arch] to contain all the model
        self.population_size_setpoint = population_size_setpoint
        self.folder = folder
        self.individuals = deque()
        self.gen_num = 0
        # load file
        for file in self.folder.history:
            if folder.alive(file):
                file_path = self.folder.file_path(file)
                arch_proto = read_file(file_path)
                arch = Arch(arch_proto)
                # add it to population
                self.individuals.append(arch)
                print("load file ", file, "accuracy:", arch.accuracy, " ...")
            else:
                self.gen_num += 1

        # the number of population is not enough
        for i in range(0, population_size_setpoint - self.__len__()):
            # random architecture
            arch = Arch.random_arch()
            arch.accuracy = train_and_eval(Model(arch))
            # add it to population
            self.add(arch)

    def get_best(self):
        best = Arch
        best.accuracy = 0
        self.folder.update()
        self.individuals = deque()
        # load file
        for file in self.folder.history:
            print("update file:", file)
            # alive file
            if self.folder.alive(file):
                file_path = self.folder.file_path(file)
                arch_proto = read_file(file_path)
                arch = Arch(arch_proto)
                print("accuracy:",arch.accuracy)
                if arch.accuracy > best.accuracy:
                    best = copy(arch)
            # dead file
            else:
                dead_file_path = self.folder.dead_file_path(file)
                arch_proto = read_file(dead_file_path)
                arch = Arch(arch_proto)
                print("accuracy:",arch.accuracy)
                if arch.accuracy > best.accuracy:
                    best = copy(arch)
        return best

    def __len__(self):
        return len(self.individuals)

    def add(self, arch):
        arch.id = self.folder.max_id + 1
        self.individuals.append(arch)
        self.folder.add(arch)

    def dead(self):
        # remove the oldest one
        arch = self.individuals[0]
        self.individuals.popleft()
        self.folder.dead(arch)

    def get_history(self):
        return self.folder.history
