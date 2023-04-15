import math
from abc import ABC, abstractmethod
from typing import Tuple, List

import numpy as np

from .chromosome import Chromosome
from .gene import Gene


def validate_length(par1: Chromosome, par2: Chromosome) -> int:
    if len(par1.information) != len(par2.information):
        raise ValueError("Genetic information length does not match")
    return len(par1.information)


def swap_sublist(l1: List[Gene], l2: List[Gene], left: int, right: int) -> Tuple[Chromosome, Chromosome]:
    ch1: List[Gene | None] = [None] * len(l1)
    ch2: List[Gene | None] = [None] * len(l2)
    for i in range(len(l1)):
        ch1[i] = l1[i] if i < left or i > right else l2[i]
        ch2[i] = l2[i] if i < left or i > right else l1[i]
    return Chromosome(ch1), Chromosome(ch2)


class Crossover(ABC):
    def __init__(self, uniform=0.5):
        self._uniform = uniform

    @abstractmethod
    def cross(self, par1: Chromosome, par2: Chromosome) -> Tuple[Chromosome, Chromosome]:
        pass


class OnePointCrossover(Crossover):
    def cross(self, par1: Chromosome, par2: Chromosome) -> Tuple[Chromosome, Chromosome]:
        length = validate_length(par1, par2)
        p = np.random.randint(0, length)
        return swap_sublist(par1.information, par2.information, p, length - 1)


class TwoPointCrossover(Crossover):
    def cross(self, par1: Chromosome, par2: Chromosome) -> Tuple[Chromosome, Chromosome]:
        length = validate_length(par1, par2)
        left = np.random.randint(0, length)
        right = np.random.randint(left, length)
        return swap_sublist(par1.information, par2.information, left, right)


class AnnularCrossover(Crossover):
    def cross(self, par1: Chromosome, par2: Chromosome) -> Tuple[Chromosome, Chromosome]:
        length = validate_length(par1, par2)
        p = np.random.randint(0, length)
        L = np.random.randint(0, math.ceil(length / 2))
        if L == 0:
            left = 0
            right = length
        elif p + L < length:
            left = p
            right = p + L - 1
        else:
            left = (p + L) % length
            right = p - 1
        return swap_sublist(par1.information, par2.information, left, right)


class UniformCrossover(Crossover):
    def cross(self, par1: Chromosome, par2: Chromosome) -> Tuple[Chromosome, Chromosome]:
        length = validate_length(par1, par2)
        ch1: List[Gene | None] = [None] * length
        ch2: List[Gene | None] = [None] * length
        for i in range(length):
            p = np.random.uniform(0, 1)
            ch1[i] = par1.information[i] if p < self._uniform else par2.information[i]
            ch2[i] = par2.information[i] if p < self._uniform else par1.information[i]
        return Chromosome(ch1), Chromosome(ch2)
