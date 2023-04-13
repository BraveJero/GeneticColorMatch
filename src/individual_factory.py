from abc import ABC, abstractmethod
from typing import List

from .chromosome import Chromosome
from .color import Color
from .color_palette import ColorPalette
from .individual import Individual, ColorIndividual
from .gene import ColorProportionGene


class IndividualFactory(ABC):
    def generate_random_population(self, size: int) -> List[Individual]:
        ans = []
        for _ in range(size):
            ans.append(self.generate_random())
        return ans

    @abstractmethod
    def generate_random(self) -> Individual:
        pass

    @abstractmethod
    def generate_from_chromosome(self, chromosome: Chromosome) -> Individual:
        pass


class ColorProportionIndividualFactory(IndividualFactory):
    def __init__(self, goal: Color, palette: ColorPalette):
        self._goal = goal
        self._palette = palette

    def generate_random(self) -> Individual:
        ch = []
        for _ in range(len(self._palette)):
            ch.append(ColorProportionGene.create_random())
        return ColorIndividual(ch, self._goal, self._palette)

    def generate_from_chromosome(self, chromosome: Chromosome) -> ColorIndividual:
        return ColorIndividual(chromosome, self._goal, self._palette)
