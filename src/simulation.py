from typing import List

import numpy as np

from src.crossover import Crossover
from src.individual import Individual
from src.individual_factory import IndividualFactory
from src.mutation import Mutation
from src.mutation_method import MutationMethod
from src.selection_method import SelectionMethod
from src.stop_condition import StopCondition


class Simulation:

    def __init__(self,
                 n: int,
                 k: int,
                 stop_condition: StopCondition,
                 selection_method: SelectionMethod,
                 crossover_method: Crossover,
                 mutation: Mutation,
                 individual_factory: IndividualFactory):
        self._n: int = n
        self._k = k - k % 1
        self._sc = stop_condition
        self._sm = selection_method
        self._cm = crossover_method
        self._mutation = mutation
        self._if: IndividualFactory = individual_factory

    def simulate(self) -> List[List[Individual]]:
        gen: List[Individual] = self._if.generate_random_population(self._n)
        ans = []

        iteration = 0
        while not self._sc(iteration, gen):
            iteration += 1
            parents: List[Individual] = self._sm.get_winners(gen, self._k)
            children: List[Individual] = []
            for i in range(self._k // 2):
                p1: Individual = parents[np.random.randint(0, len(parents))]
                p2: Individual = parents[np.random.randint(0, len(parents))]
                ch1, ch2 = self._cm.cross(p1.chromosome, p2.chromosome)
                self._mutation.mutate(ch1)
                self._mutation.mutate(ch2)
                # TODO: Check factory from chromosome
                child1, child2 = self._if.generate_from_chromosome(ch1), self._if.generate_from_chromosome(ch2)
                children.extend([child1, child2])

            # TODO: Use selection methods which consider children
            gen.extend(children)
            gen = self._sm.get_winners(gen, self._n)
            ans.append(gen)

        return ans
