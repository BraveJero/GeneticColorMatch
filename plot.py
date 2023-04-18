import os
from abc import ABC
from functools import reduce
from typing import List

import matplotlib.pyplot as plt
import numpy as np

from src.individual import MAX_FITNESS
from src.color import Color
from src.color_palette import ColorPalette
from src.crossover import OnePointCrossover
from src.generation_selection import UseAllGenerationSelection
from src.individual import Individual
from src.individual_factory import ColorProportionIndividualFactory
from src.mutation import UniformMutation
from src.mutation_method import ColorProportionRandomMutation
from src.selection_method import EliteSelection
from src.simulation import Simulation
from src.stop_condition import GenerationCountStopCondition

TEST_COUNT = 10
GENERATION_COUNT = 5
PALETTE_SIZE = 8
GENERATION_SIZE = 10
CHILDREN_SIZE = 5

OUTPUT_DIR = "figs/"


def _get_random_color() -> Color:
    return Color(
        np.random.randint(0, 255),
        np.random.randint(0, 255),
        np.random.randint(0, 255)
    )


class Plotter(ABC):
    def plot(self):
        color_goal: Color = _get_random_color()
        colors: List[Color] = []
        for _ in range(PALETTE_SIZE):
            colors.append(_get_random_color())
        color_palette: ColorPalette = ColorPalette(colors)
        s: Simulation = Simulation(
            n=GENERATION_SIZE,
            k=CHILDREN_SIZE,
            stop_condition=GenerationCountStopCondition(GENERATION_COUNT),
            selection_method=EliteSelection(),
            crossover_method=OnePointCrossover(),
            mutation=UniformMutation(0.1, ColorProportionRandomMutation()),
            individual_factory=ColorProportionIndividualFactory(goal=color_goal, palette=color_palette),
            generation_selection=UseAllGenerationSelection(EliteSelection(), GENERATION_SIZE)
        )

        generations: List[List[Individual]] = s.simulate()
        fitnesses = [
            [individual.fitness() for individual in generation] for generation in generations
        ]
        bests = list(map(
            lambda g: reduce(
                (lambda i1, i2: i1 if i1.fitness() >= i2.fitness() else i2),
                g
            ),
            generations
        ))
        plt.plot(range(len(bests)), list(map(lambda i: i.fitness(), bests)))
        print(list(map(lambda i: i.fitness(), bests)), sep="\n")
        plt.ylim([0, MAX_FITNESS])

        plt.savefig(OUTPUT_DIR + "linegraph.jpg")


if __name__ == "__main__":
    if not os.path.exists(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)

    Plotter().plot()

