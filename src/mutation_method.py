from abc import ABC

import numpy as np

from .gene import Gene, ColorProportionGene


class MutationMethod(ABC):
    def __call__(self, gene: Gene):
        pass


class ColorProportionGradientMutation(MutationMethod):
    def __init__(self, dev: float):
        self._dev = dev

    def __call__(self, gene: ColorProportionGene):
        val = np.random.normal(gene.value, self._dev)
        gene.value = np.clip(val, 0, 1)


class ColorProportionRandomMutation(MutationMethod):
    def __call__(self, gene: ColorProportionGene):
        gene.value = np.random.uniform(0, 1)
