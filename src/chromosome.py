from __future__ import annotations

from abc import ABC
from copy import copy
from typing import List
from math import gcd


class Chromosome(ABC):
    def __init__(self):
        pass


class ColorChromosome(Chromosome):
    def __init__(self, proportions: List[int]):
        self._proportions = copy(proportions)  # TODO: check if deepcopy is necessary
        self._simplify()

    @property
    def proportions(self):
        return self._proportions

    # Simplifies proportions to simplest terms (i.e. [2, 4, 6] ---> [1, 2, 3])
    def _simplify(self):
        d = gcd(*self._proportions)
        self._proportions = [p // d for p in self._proportions]

    def __repr__(self):
        return self._proportions.__repr__()
