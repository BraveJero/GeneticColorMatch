from __future__ import annotations

from abc import ABC
from .chromosome import Chromosome
from .color_palette import ColorPalette
from .color import Color


class Individual(ABC):
    def __init__(self, chromosome: Chromosome):
        self._chromosome = chromosome


class ColorIndividual(Individual):
    def __init__(self, chromosome: Chromosome, palette: ColorPalette, goal: Color):
        super(chromosome)
        self._chromosome = chromosome
        self._palette
