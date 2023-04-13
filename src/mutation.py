from abc import ABC

from .chromosome import Chromosome, ColorChromosome


class Mutation(ABC):
    def mutate(self, chromosome: Chromosome, dev: float, prob: float):
        """
        :param chromosome: chromosome to mutate
        :param dev: each allele mutates according to a Gaussian bell centered at its value with deviation dev
        :param prob: probability of mutating an allele to some othe random
        """
        pass



