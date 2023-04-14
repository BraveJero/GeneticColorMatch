from abc import ABC, abstractmethod
from typing import List

from .individual import Individual


class StopCondition(ABC):
    @abstractmethod
    def __call__(self, generation_count: int, generation: List[Individual]) -> bool:
        pass


class GenerationCountStopCondition(StopCondition):
    def __init__(self, count: int):
        self._count = count

    def __call__(self, generation_count: int, generation: List[Individual]) -> bool:
        return generation_count >= self._count
