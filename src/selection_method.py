import math
import random
from abc import ABC
from typing import List, Callable

from src.individual import Individual


class SelectionMethod(ABC):
    def get_winners(self, population: List[Individual], k: int, fitness: Callable[[Individual], float]) \
            -> List[Individual]:
        pass


class EliteSelection(SelectionMethod):
    def get_winners(self, population: List[Individual], k: int, fitness: Callable[[Individual], float]) \
            -> List[Individual]:
        winners = []

        length = len(population)
        if length == 0:
            return winners

        population.sort(key=lambda ind: fitness(ind))

        for i, individual in enumerate(population):
            n = math.ceil((k - i) / length)
            for j in range(n):
                winners.append(individual)

        return winners


class RouletteWheelSelection(SelectionMethod):
    def get_winners(self, population: List[Individual], k: int, fitness: Callable[[Individual], float]) \
            -> List[Individual]:
        length = len(population)
        if length == 0:
            return []

        individual_fitness_list = [fitness(ind) for ind in population]
        return self.do_roulette(population, length, k, individual_fitness_list)

    def do_roulette(self, population: List[Individual], length: int, k: int, fitness_list: List[float]):
        winners = []

        fitness_sum = sum(fitness_list)

        for i in range(k):
            r = random.random()
            accumulated_fitness = 0
            for j in range(length):
                relative_fitness = fitness_list[j] / fitness_sum
                if accumulated_fitness < r <= accumulated_fitness + relative_fitness:
                    winners.append(population[j])
                    break
                accumulated_fitness += relative_fitness

        return winners


class UniversalSelection(SelectionMethod):
    def get_winners(self, population: List[Individual], k: int, fitness: Callable[[Individual], float]) \
            -> List[Individual]:
        winners = []

        length = len(population)
        if length == 0:
            return winners

        fitness_list = [fitness(ind) for ind in population]
        fitness_sum = sum(fitness_list)

        r = random.random()
        for i in range(k):
            ri = (r + i) / k
            accumulated_fitness = 0
            for j in range(length):
                relative_fitness = fitness_list[j] / fitness_sum
                if accumulated_fitness < r <= accumulated_fitness + relative_fitness:
                    winners.append(population[j])
                    break
                accumulated_fitness += relative_fitness

        return winners


class RankSelection(RouletteWheelSelection):
    def get_winners(self, population: List[Individual], k: int, fitness: Callable[[Individual], float]) \
            -> List[Individual]:
        length = len(population)
        if length == 0:
            return []

        population.sort(key=lambda ind: fitness(ind))
        individual_fitness_list = [(length - (idx + 1)) / length for idx, ind in enumerate(population)]

        return self.do_roulette(population, length, k, individual_fitness_list)


class EntropicBoltzmannSelection(SelectionMethod):
    def __init__(self, temperature: int):
        self._temperature = temperature

    def get_winners(self, population: List[Individual], k: int, fitness: Callable[[Individual], float]) \
            -> List[Individual]:
        pass


class DeterministicTournamentSelection(SelectionMethod):
    def __init__(self, m: int):
        self._m = m

    def get_winners(self, population: List[Individual], k: int, fitness: Callable[[Individual], float]) \
            -> List[Individual]:
        winners = []

        length = len(population)
        if len(population) == 0:
            return winners

        for i in range(k):
            best = population[random.randint(0, length - 1)]
            best_fitness = fitness(best)
            for j in range(1, self._m):
                chosen = population[random.randint(0, length - 1)]
                aux_fitness = fitness(chosen)
                if best_fitness < aux_fitness:
                    best = chosen
                    best_fitness = aux_fitness
            winners.append(best)

        return winners


class ProbabilisticTournamentSelection(SelectionMethod):
    def get_winners(self, population: List[Individual], k: int, fitness: Callable[[Individual], float]) \
            -> List[Individual]:
        winners = []

        length = len(population)
        if length == 0:
            return winners

        threshold = random.uniform(0.5, 1)
        length = len(population)

        for i in range(k):
            first = population[random.randint(0, length - 1)]
            second = population[random.randint(0, length - 1)]
            first_fitness = fitness(first)
            second_fitness = fitness(second)

            if first_fitness > second_fitness:
                best = first
                worst = second
            else:
                best = second
                worst = first

            r = random.uniform(0, 1)

            if r < threshold:
                winners.append(best)
            else:
                winners.append(worst)

        return winners
