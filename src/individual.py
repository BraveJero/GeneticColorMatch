from __future__ import annotations

from abc import ABC, abstractmethod
from .chromosome import Chromosome
from .color_palette import ColorPalette
from .color import Color


class Individual(ABC):
    def __init__(self, chromosome: Chromosome):
        self._chromosome = chromosome

    @abstractmethod
    def fitness(self) -> float:
        pass

    @property
    def chromosome(self) -> Chromosome:
        return self._chromosome


class ColorIndividual(Individual):
    def __init__(self, chromosome: Chromosome, palette: ColorPalette, goal: Color):
        super().__init__(chromosome)
        self._chromosome = chromosome
        self._palette = palette
        self._goal = goal
        self._color = palette.from_proportions([g.value for g in self._chromosome.information])

    def fitness(self) -> float:
        return Color.distance(self._goal, self._color)

    def __str__(self):
        return self._color.__str__()

    def __repr__(self):
        return self.__str__()
