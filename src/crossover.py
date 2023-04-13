from abc import ABC, abstractmethod
from typing import Tuple, List

from .chromosome import Chromosome
import numpy as np
import math


def validate_length(par1: Chromosome, par2: Chromosome) -> int:
    if len(par1.information) != len(par2.information):
        raise ValueError("Genetic information length does not match")
    return len(par1.information)


def swap_sublist(l1: List, l2: List, left: int, right: int):
    for i in range(left, right):
        l1[i], l2[i] = l2[i], l1[i]


class Crossover(ABC):
    @staticmethod
    @abstractmethod
    def cross(par1: Chromosome, par2: Chromosome) -> Tuple[List, List]:
        pass


class OnePointCrossover(Crossover):
    @staticmethod
    def cross(par1: Chromosome, par2: Chromosome) -> Tuple[List, List]:
        length = validate_length(par1, par2)
        ch1 = [None] * length
        ch2 = [None] * length
        p = np.random.randint(0, length)
        for i in range(length):
            ch1[i] = par1.information[i] if i < p else par2.information[i]
            ch2[i] = par2.information[i] if i < p else par1.information[i]
        return ch1, ch2


class TwoPointCrossover(Crossover):
    @staticmethod
    def cross(par1: Chromosome, par2: Chromosome) -> Tuple[List, List]:
        length = validate_length(par1, par2)
        ch1 = [None] * length
        ch2 = [None] * length
        p1 = np.random.randint(0, length)
        p2 = np.random.randint(p1, length)
        for i in range(length):
            ch1[i] = par1.information[i] if i < p1 or i > p2 else par2.information[i]
            ch2[i] = par2.information[i] if i < p1 or i > p2 else par1.information[i]
        return ch1, ch2


class AnnularCrossover(Crossover):
    @staticmethod
    def cross(par1: Chromosome, par2: Chromosome) -> Tuple[List, List]:
        length = validate_length(par1, par2)
        ch1 = [None] * length
        ch2 = [None] * length
        p = 2  # np.random.randint(0, length)
        length = 2  # np.random.randint(0, math.ceil(length/2))
        p1 = math.min(p, (p + length) % length)
        p2 = p1 + length
        swap_sublist(ch1, ch2, p1, p2)
        return ch1, ch2
