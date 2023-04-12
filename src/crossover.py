from abc import ABC, abstractmethod

from .chromosome import Chromosome, ColorChromosome


class Crossover(ABC):
    @staticmethod
    @abstractmethod
    def cross(ch1: Chromosome, ch2: Chromosome) -> Chromosome:
        pass
