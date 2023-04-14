import json
import logging
import sys

from menu import Menu


def get_stop_condition(genetic_settings):
    match genetic_settings["stop_condition"]["condition"]:
        case "time":
            return  # genetic_settings["stop_condition"]["parameter"] has the time
        case "generation":
            return
        case "acceptable_solution":
            return
        case _:
            raise ValueError("Unsupported stop condition")


def get_selection_method(genetic_settings):
    match genetic_settings["selection_method"]["method"]:
        case "elite":
            return
        case "roulette":
            return
        case "universal":
            return
        case "ranking":
            return
        case "boltzmann":
            return  # genetic_settings["stop_condition"]["parameter"] has the temperature
        case "tournament":
            return  # genetic_settings["selection_method"]["parameter"] has the "m"
        case _:
            raise ValueError("Unsupported selection method")


def get_crossover_method(genetic_settings):
    match genetic_settings["crossover_method"]:
        case "single_point":
            return
        case "two_point":
            return
        case "annular":
            return
        case "uniform":
            return
        case _:
            raise ValueError("Unsupported crossover method")


def get_mutation_method(genetic_settings):
    match genetic_settings["mutation_method"]:
        case "genome":
            return
        case "limited_multi-genome":
            return
        case "uniform_multi-genome":
            return
        case "complete":
            return
        case _:
            raise ValueError("Unsupported mutation method")


def get_new_generation_selection(genetic_settings):
    match genetic_settings["new_generation_selection"]:
        case "use_all":
            return
        case "new_over_actual":
            return
        case _:
            raise ValueError("Unsupported generation selection method")


def main():
    if len(sys.argv) < 2:
        print("Config file argument not found")
        exit(1)

    if sys.argv[1] == "menu":
        Menu().run()
        return

    config_path = sys.argv[1]

    with open(config_path, "r") as f:
        genetic_settings = json.load(f)


if __name__ == "__main__":
    main()
