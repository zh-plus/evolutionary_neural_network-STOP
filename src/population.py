from architecture import *
from file_system import *


class Population:
    """Use file system to represent population"""

    def __init__(self, folder):

        # initial a List[arch] to contain all the model
        P = 1
        self.folder = folder
        self.individuals = []
        # load file
        for file in self.folder.history:
            if folder.alive(file):
                file_path = self.folder.file_path(file)
                arch_proto = read_file(file_path)
                arch = Arch(arch_proto)
                # add it to population
                self.individuals.append(arch)
                print("load file ", file,  "accuracy:", arch.accuracy, " ...")
        # the number of population is not enough
        for i in range(0, P - self.__len__()):
            # random architecture
            arch = Arch.random_arch()
            arch.id = self.folder.max_id + 1
            # add it to population
            self.individuals.append(arch)

    def __len__(self):
        return len(self.individuals)

    def add(self, arch):
        arch.id = self.folder.max_id+1
        self.individuals.append(arch)
        self.folder.add(arch)

    def dead(self):
        # remove the oldest one
        arch = self.individuals[0]
        self.individuals.pop(0)
        self.folder.dead(arch)







