import random
from typing import List

from src.crossover import Crossover
from src.generation_selection import GenerationSelection
from src.individual import Individual
from src.individual_factory import IndividualFactory
from src.mutation import Mutation
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
                 individual_factory: IndividualFactory,
                 generation_selection: GenerationSelection):
        self._n: int = n
        self._k = k - k % 1
        self._sc = stop_condition
        self._sm = selection_method
        self._cm = crossover_method
        self._mutation = mutation
        self._if: IndividualFactory = individual_factory
        self._generation_selection = generation_selection

    def simulate(self) -> List[List[Individual]]:
        gen: List[Individual] = self._if.generate_random_population(self._n)
        ans = [gen.copy()]
        
        iteration = 0
        while not self._sc(iteration, gen):
            iteration += 1
            parents: List[Individual] = self._sm.get_winners(gen, self._k)
            children: List[Individual] = []
            # Shuffle parents then pick in order to use them all
            random.shuffle(parents)
            for i in range(self._k // 2):
                p1: Individual = parents[2 * i]
                p2: Individual = parents[2 * i + 1]
                ch1, ch2 = self._cm.cross(p1.chromosome, p2.chromosome)
                self._mutation.mutate(ch1)
                self._mutation.mutate(ch2)
                child1, child2 = self._if.generate_from_chromosome(ch1), self._if.generate_from_chromosome(ch2)
                if child1 is not None:
                    children.append(child1)
                if child2 is not None:
                    children.append(child2)
            gen = self._generation_selection.get_next_generation(gen, children)
            ans.append(gen.copy())

        return ans
