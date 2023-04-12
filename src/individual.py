from abc import ABC
from .chromosome import Chromosome, ColorChromosome


class Individual(ABC):
    def __init__(self, chromosome: Chromosome):
        pass


class ColorIndividual(Individual):
    def __init__(self, chromosome: ColorChromosome):
        self._chromosome = chromosome

