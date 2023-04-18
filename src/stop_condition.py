from abc import ABC, abstractmethod
from typing import List

import time

from .individual import Individual, MAX_FITNESS


class StopCondition(ABC):
    @abstractmethod
    def __call__(self, generation_count: int, generation: List[Individual]) -> bool:
        pass


class GenerationCountStopCondition(StopCondition):
    def __init__(self, count: int):
        self._count = count

    def __call__(self, generation_count: int, generation: List[Individual]) -> bool:
        return generation_count >= self._count


class GoalIndividualStopCondition(StopCondition):
    def __init__(self, similitude=0.1):
        self.__similitude = similitude

    def __call__(self, generation_count: int, generation: List[Individual]) -> bool:
        for individual in generation:
            if individual.fitness() - MAX_FITNESS < self.__similitude:
                return True
        return False


def time_ms():
    return round(time.time() * 1000)


class TimeStopCondition(StopCondition):
    def __init__(self, running_time: int):
        self._running_time = running_time
        self._start = time_ms()

    def __call__(self, generation_count: int, generation: List[Individual]) -> bool:
        return self._running_time < (time_ms() - self._start)


class ContentStopCondition(StopCondition):
    def __init__(self, delta: float, unchanged_generations: int):
        self._delta = delta
        self._unchanged_generations = unchanged_generations
        self._unchanged = 0
        self._previous = 0

    def __call__(self, generation_count: int, generation: List[Individual]) -> bool:
        best = max([ind.fitness() for ind in generation])
        self._unchanged = self._unchanged + 1 if self._previous - self._delta <= best <= self._previous + self._delta \
            else 0
        self._previous = best
        return self._unchanged > self._unchanged_generations
