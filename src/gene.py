from abc import ABC
from __future__ import annotations

import numpy as np

class Gene(ABC):
    @property
    def value(self):
        pass

    @value.setter
    def value(self, value):
        pass

    @staticmethod
    def create_random() -> Gene:
        pass


class ColorProportionGene(Gene):
    def __init__(self, proportion: float):
        if proportion < 0 or proportion > 1:
            raise ValueError("Proportion must be in the range [0, 1]")
        self._proportion = proportion

    @property
    def value(self):
        return self._proportion

    @value.setter
    def value(self, value):
        self._proportion = value

    def __repr__(self):
        return str(self._proportion)

    @staticmethod
    def create_random() -> ColorProportionGene:
        return ColorProportionGene(np.random.uniform(0, 1))
