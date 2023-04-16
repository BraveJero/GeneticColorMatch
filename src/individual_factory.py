import random
from abc import ABC, abstractmethod
from typing import List

from .chromosome import Chromosome
from .color import Color
from .color_palette import ColorPalette
from .gene import ColorProportionGene
from .individual import Individual, ColorIndividual


class IndividualFactory(ABC):
    def generate_random_population(self, size: int) -> List[Individual]:
        ans = []
        while len(ans) < size:
            ind = self.generate_random()
            if ind is not None:
                ans.append(ind)
        return ans

    @abstractmethod
    def generate_random(self) -> Individual:
        pass

    @abstractmethod
    def generate_from_chromosome(self, chromosome: Chromosome) -> Individual:
        pass


class ColorProportionIndividualFactory(IndividualFactory):
    def __init__(self, goal: Color, palette: ColorPalette):
        self._goal: Color = goal
        self._palette: ColorPalette = palette

    def generate_random(self) -> Individual | None:
        ch = []
        for _ in range(len(self._palette)):
            ch.append(ColorProportionGene(0))
        ch[random.randint(0, len(self._palette) - 1)] = ColorProportionGene(1)
        # for _ in range(len(self._palette)):
        #     ch.append(ColorProportionGene.create_random())
        return self.generate_from_chromosome(Chromosome(ch))

    def generate_from_chromosome(self, chromosome: Chromosome) -> ColorIndividual | None:
        if all(gene.value == 0 for gene in chromosome.information):
            return None
        return ColorIndividual(chromosome, self._palette, self._goal)
