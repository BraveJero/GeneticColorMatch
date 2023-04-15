import random
from abc import ABC

import numpy as np

from .chromosome import Chromosome
from .mutation_method import MutationMethod


class Mutation(ABC):
    def __init__(self, prob: float, method: MutationMethod):
        if prob < 0 or prob > 1:
            raise ValueError("Wrong probability")
        self._prob = prob
        self._method = method

    def mutate(self, ch: Chromosome):
        pass


class SingleGeneMutation(Mutation):
    def mutate(self, ch: Chromosome):
        if np.random.uniform(0, 1) < self._prob:
            index = np.random.randint(0, len(ch.information))
            self._method(ch.information[index])


class LimitedMultigeneMutation(Mutation):
    def mutate(self, ch: Chromosome):
        M = np.random.randint(0, len(ch.information))
        indexes = random.sample(range(len(ch.information)), M)
        for i in indexes:
            if np.random.uniform(0, 1) < self._prob:
                self._method(ch.information[i])


class UniformMutation(Mutation):
    def mutate(self, ch: Chromosome):
        for g in ch.information:
            if np.random.uniform(0, 1) < self._prob:
                self._method(g)


class CompleteMutation(Mutation):
    def mutate(self, ch: Chromosome):
        if np.random.uniform():
            for g in ch.information:
                self._method(g)
