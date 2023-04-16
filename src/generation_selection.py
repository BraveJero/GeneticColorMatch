from abc import ABC, abstractmethod
from typing import List

from src.individual import Individual
from src.selection_method import SelectionMethod


class GenerationSelection(ABC):
    def __init__(self, method: SelectionMethod, n: int):
        self._method = method
        self._n = n

    @abstractmethod
    def get_next_generation(self, old: List[Individual], new: List[Individual]) -> List[Individual]:
        pass


class UseAllGenerationSelection(GenerationSelection):
    def get_next_generation(self, old: List[Individual], new: List[Individual]) -> List[Individual]:
        old.extend(new)
        return self._method.get_winners(old, self._n)


class NewOverActualGenerationSelection(GenerationSelection):
    def get_next_generation(self, old: List[Individual], new: List[Individual]) -> List[Individual]:
        if len(new) > self._n:
            return self._method.get_winners(new, self._n)
        else:
            new.extend(self._method.get_winners(old, self._n - len(new)))
            return new
