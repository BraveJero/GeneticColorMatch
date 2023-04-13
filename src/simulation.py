from typing import Callable, List

import numpy as np

from src import individual_factory
from src.chromosome import Chromosome
from src.crossover import Crossover
from src.individual import Individual
from src.mutation import Mutation
from src.mutation_method import MutationMethod
from src.selection_method import SelectionMethod
from src.stop_condition import StopCondition


class Simulation:
    # n -> tamano poblacion
    # k -> cantidad de hijos
    # metodo de seleccion
    # metodo de mutacion genetica
    # metodo de mutacion cromosodfdshkajf
    # alguna forma de generar aleatoriamente(?)

    def __init__(self,
                 n: int,
                 k: int,
                 stop_condition: StopCondition,
                 fitness: Callable[[Individual], float],
                 selection_method: SelectionMethod,
                 crossover_method: Crossover,
                 mutation: Mutation,
                 mutation_method: MutationMethod):
        self._n = n
        self._k = k - k % 1
        self._stop_condition = stop_condition
        self._fitness = fitness
        self._selection_method = selection_method
        self._crossover_method = crossover_method
        self._mutation = mutation
        self._mutation_method = mutation_method
        self._individual_factory = individual_factory

    def simulate(self):
        gen: List[Individual] = []
        for i in range(self._n):
            gen.append(self._individual_factory.generate())  # TODO: Check factory

        iteration = 0
        # TODO: Check stop condition
        while not self._stop_condition(iteration, gen):
            iteration += 1
            parents: List[Individual] = self._selection_method.get_winners(gen, self._k, self._fitness)
            children: List[Individual] = []
            for i in range(self._k / 2):
                p1: int = np.random.randint(0, len(parents))
                p2: int = np.random.randint(0, len(parents))
                ch1, ch2 = self._crossover_method.cross(p1, p2)
                ch1, ch2 = self._mutation.mutate(ch1), self._mutation.mutate(ch2)
                # TODO: Check factory from chromosome
                child1, child2 = self._individual_factory(ch1), self._individual_factory(ch1)
                children.extend([child1, child2])

            gen = self._selection_method.get_winners(gen, self._n, self._fitness)

        print("Simulated.")
