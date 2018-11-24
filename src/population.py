from architecture import Arch
from file_system import *


class Population:
    """Use file system to represent population"""

    def __init__(self, folder):

        # initial a List[arch] to contain all the model
        P = 10
        self.folder = folder
        self.individuals = []

        for file in self.folder.history:
            if folder.alive(file):
                file_path = self.folder.file_path(file)
                arch_proto = read_file(file_path)
                self.individuals.append(Arch(arch_proto))
                print("load file ", file, " ...")

        for i in range(0, P-self.__len__()):
            arch = Arch()
            arch.id = self.folder.max_id + 1
            arch.random_arch()
            self.individuals.append(arch)
            folder.create_file(arch.to_proto())

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







