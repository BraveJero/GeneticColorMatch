import json
import sys

import numpy as np

from src.color import Color
from src.color_palette import ColorPalette
from src.crossover import Crossover, OnePointCrossover, TwoPointCrossover, AnnularCrossover, UniformCrossover
from src.generation_selection import UseAllGenerationSelection, NewOverActualGenerationSelection
from src.individual_factory import ColorProportionIndividualFactory
from src.mutation import Mutation, SingleGeneMutation, LimitedMultigeneMutation, UniformMutation, CompleteMutation
from src.mutation_method import MutationMethod, ColorProportionRandomMutation, ColorProportionGradientMutation
from src.selection_method import SelectionMethod, ProbabilisticTournamentSelection, EliteSelection, \
    RouletteWheelSelection, UniversalSelection, RankSelection, DeterministicTournamentSelection, \
    EntropicBoltzmannSelection
from src.simulation import Simulation
from src.stop_condition import GenerationCountStopCondition, StopCondition, GoalIndividualStopCondition, \
    TimeStopCondition
from utils import plot_data


def get_stop_condition(genetic_settings) -> StopCondition:
    match genetic_settings["stop_condition"]["condition"]:
        case "time":
            return TimeStopCondition(int(genetic_settings["stop_condition"]["parameter"]))
        case "generation":
            return GenerationCountStopCondition(int(genetic_settings["stop_condition"]["parameter"]))
        case "acceptable_solution":
            return GoalIndividualStopCondition(float(genetic_settings["stop_condition"]["parameter"]))
        case _:
            raise ValueError("Unsupported stop condition")


def get_selection_method(genetic_settings) -> SelectionMethod:
    match genetic_settings["selection_method"]["method"]:
        case "elite":
            return EliteSelection()
        case "roulette":
            return RouletteWheelSelection()
        case "universal":
            return UniversalSelection()
        case "ranking":
            return RankSelection()
        case "boltzmann":
            parameter = genetic_settings["selection_method"]["parameter"]
            t0 = float(parameter["initial_temp"])
            tc = float(parameter["final_temp"])
            k = float(parameter["k_value"])
            return EntropicBoltzmannSelection(t0, tc, k)
        case "probabilistic_tournament":
            return ProbabilisticTournamentSelection()
        case "deterministic_tournament":
            return DeterministicTournamentSelection(int(genetic_settings["selection_method"]["parameter"]))
        case _:
            raise ValueError("Unsupported selection method")


def get_crossover_method(genetic_settings) -> Crossover:
    match genetic_settings["crossover_method"]:
        case "single_point":
            return OnePointCrossover()
        case "two_point":
            return TwoPointCrossover()
        case "annular":
            return AnnularCrossover()
        case "uniform":
            return UniformCrossover()
        case _:
            raise ValueError("Unsupported crossover method")


def get_mutation_method(method) -> MutationMethod:
    match method["name"]:
        case "random":
            return ColorProportionRandomMutation()
        case "gradient":
            return ColorProportionGradientMutation(float(method["parameter"]))
        case _:
            raise ValueError("Unsupported mutation method")


def get_mutation(genetic_settings) -> Mutation:
    mutation_method = get_mutation_method(genetic_settings["mutation_method"]["method"])
    mutation_probability = float(genetic_settings["mutation_method"]["probability"])
    match genetic_settings["mutation_method"]["mutation"]:
        case "single_genome":
            return SingleGeneMutation(prob=mutation_probability, method=mutation_method)
        case "limited_multi-genome":
            return LimitedMultigeneMutation(prob=mutation_probability, method=mutation_method)
        case "uniform_multi-genome":
            return UniformMutation(prob=mutation_probability, method=mutation_method)
        case "complete":
            return CompleteMutation(prob=mutation_probability, method=mutation_method)
        case _:
            raise ValueError("Unsupported mutation method")


def get_generation_selection(genetic_settings, selection_method):
    match genetic_settings["generation_selection"]:
        case "use_all":
            return UseAllGenerationSelection(selection_method, int(genetic_settings["n"]))
        case "new_over_actual":
            return NewOverActualGenerationSelection(selection_method, int(genetic_settings["n"]))
        case _:
            raise ValueError("Unsupported generation selection method")


def main():
    if len(sys.argv) < 2:
        print("Config file argument not found")
        exit(1)

    config_path = sys.argv[1]

    with open(config_path, "r") as f:
        genetic_settings = json.load(f)

    color_goal_list = np.array(genetic_settings["goal"].split(","), dtype=int)
    if len(color_goal_list) != 3:
        raise ValueError("Invalid goal color")
    color_goal = Color(color_goal_list[0], color_goal_list[1], color_goal_list[2])

    color_palette = ColorPalette([])
    for color in np.mat(genetic_settings["palette"]).tolist():
        color_palette.add_color(Color(color[0], color[1], color[2]))

    selection_method = get_selection_method(genetic_settings)

    sim = Simulation(
        n=int(genetic_settings["n"]),
        k=int(genetic_settings["k"]),
        stop_condition=get_stop_condition(genetic_settings),
        selection_method=selection_method,
        crossover_method=get_crossover_method(genetic_settings),
        mutation=get_mutation(genetic_settings),
        individual_factory=ColorProportionIndividualFactory(goal=color_goal, palette=color_palette),
        generation_selection=get_generation_selection(genetic_settings, selection_method)
    )

    generations = sim.simulate()

    print("Would you like to plot the data? It may take some time. [y/n]")
    try:
        if genetic_settings["plot"] == "never_ask" or input() == 'y':
            generational_data = []
            for (i, generation) in enumerate(generations):
                generational_data.append([])
                for (j, individual) in enumerate(generation):
                    generational_data[i].append([])
                    generational_data[i][j].append(individual.color.r / 255)
                    generational_data[i][j].append(individual.color.g / 255)
                    generational_data[i][j].append(individual.color.b / 255)

            plot_data(generational_data, color_goal)
    except:
        print("bruh.")


if __name__ == "__main__":
    main()
