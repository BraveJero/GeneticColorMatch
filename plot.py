import os
from abc import ABC
from functools import reduce
from numbers import Number
from statistics import mean, stdev
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
from src.selection_method import EliteSelection, RankSelection, UniversalSelection, DeterministicTournamentSelection, \
    RouletteWheelSelection, EntropicBoltzmannSelection, ProbabilisticTournamentSelection
from src.simulation import Simulation
from src.stop_condition import GenerationCountStopCondition, GoalIndividualStopCondition

TEST_COUNT = 100
GENERATION_COUNT = 50
PALETTE_SIZE = 8
GENERATION_SIZE = 10
CHILDREN_SIZE = 5

OUTPUT_DIR = "figs/"


GOAL_COLOR: Color = Color(255//2, 255//2, 255//2)

COLOR_PALETTE: ColorPalette = ColorPalette([
    Color(0, 0, 0),
    Color(0, 0, 255),
    Color(0, 255, 0),
    Color(0, 255, 255),
    Color(255, 0, 0),
    Color(255, 0, 255),
    Color(255, 255, 0),
    Color(255, 255, 255),
])


def line_plot():
    ans = []
    for _ in range(TEST_COUNT):
        s: Simulation = Simulation(
            n=GENERATION_SIZE, # 10
            k=CHILDREN_SIZE, # 5
            stop_condition=GenerationCountStopCondition(GENERATION_COUNT),
            selection_method=ProbabilisticTournamentSelection(),
            crossover_method=OnePointCrossover(),
            mutation=UniformMutation(0.001, ColorProportionRandomMutation()),
            individual_factory=ColorProportionIndividualFactory(goal=GOAL_COLOR, palette=COLOR_PALETTE),
            generation_selection=UseAllGenerationSelection(EliteSelection(), GENERATION_SIZE)
        )

        generations: List[List[Individual]] = s.simulate()
        ans.append(generations)

    # ans: List[List[List[Individuals]]]
    list_of_max_fitness: List[List[Number]] = [
        [max([individual.fitness() for individual in generation]) for generation in simulation] for simulation in
        ans
    ]
    means: List[Number] = [
        mean([list_of_max_fitness[test][generation] for test in range(TEST_COUNT)]) for generation in
        range(GENERATION_COUNT)
    ]
    stds: List[Number] = [
        stdev([list_of_max_fitness[test][generation] for test in range(TEST_COUNT)]) for generation in
        range(GENERATION_COUNT)
    ]
    plt.errorbar(range(len(means)), means, yerr=stds, label='')
    plt.ylim([0, MAX_FITNESS])

    plt.title("ProbabilisticTournamentSelection")
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.show()
    plt.savefig(OUTPUT_DIR + "linegraph.jpg")


def bar_plot():
    map_name_selection = {
        "Elite": EliteSelection(),
        "RouletteWheel": RouletteWheelSelection(),
        "Universal": UniversalSelection(),
        "Rank": RankSelection(),
        "EntropicBoltzmann": EntropicBoltzmannSelection(MAX_FITNESS, 0, 0.01),
        "DeterministicTournament": DeterministicTournamentSelection(CHILDREN_SIZE),
        "ProbabilisticTournament": ProbabilisticTournamentSelection()
    }
    ans = {}
    for selection_name in map_name_selection.keys():
        ans[selection_name] = []

    for _ in range(TEST_COUNT):
        for selection_name in map_name_selection.keys():
            generation_count: int = len(Simulation(
                n=GENERATION_SIZE,
                k=CHILDREN_SIZE,
                stop_condition=GoalIndividualStopCondition(50),
                selection_method=map_name_selection[selection_name],
                crossover_method=OnePointCrossover(),
                mutation=UniformMutation(0.001, ColorProportionRandomMutation()),
                individual_factory=ColorProportionIndividualFactory(goal=GOAL_COLOR, palette=COLOR_PALETTE),
                generation_selection=UseAllGenerationSelection(EliteSelection(), GENERATION_SIZE)
            ).simulate())

            ans[selection_name].append(generation_count)

    means = []
    stds = []
    for selection_name in map_name_selection.keys():
        means.append(mean(ans[selection_name]))
        stds.append(stdev(ans[selection_name]))

    plt.bar(map_name_selection.keys(), means, yerr=stds)
    plt.title("Selection methods")
    plt.xticks(rotation=45)
    plt.ylabel("Generation till accepted solution")
    plt.ylim([0, 1300])
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    if not os.path.exists(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)

    bar_plot()
