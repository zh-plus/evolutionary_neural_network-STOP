from typing import List

from dna import DNA


class Population():
    """May use file system to represent population, so using a independent class here."""

    def __init__(self, initial_population):
        self.individuals = initial_population  # type: List[DNA]

    def __len__(self):
        return len(self.individuals)

    def add(self, dna):
        self.individuals.append(dna)

    def kill(self, dna):
        pass