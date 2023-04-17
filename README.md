# Genetic Algorithm for Color Mixing

This project is a Python implementation of a genetic algorithm that determines the combination of colors needed to
create a specific color. The input is the RGB values of the desired color and the palette of colors from where to get
the proportions, and the output is the combination of colors from the palette needed to create it, and the similarity
between this combination and the original color.

### Requirements

- Python3
- pip3
- [pipenv](https://pypi.org/project/pipenv/)

### Instalation

Run

```sh
pipenv install
```

to install the necesary dependencies

## Run

```sh
pipenv run python main.py [config_file]
```

### Configuration File

To configure the execution of the program a `.json` configuration file with a specific format is needed. The specific
format is as follows

- `plot`: configure if program should plot or no -- Options(never_ask, ask)
- `stop_condition`: configuration about the stop condition method to use
    - `condition`: name of the method to use -- Options(time, generation, acceptable_solution)
    - `parameter`: parameter the method uses as limit (time, number of generations, similitude to solution)
- `selection_method`: configure the selection method to use
    - `method`: name of the method to use -- Options(elite, roulette, universal, ranking, boltzmann,
      probabilistic_tournament, deterministic_tournament)
    - `parameter`: parameter the method uses (m for deterministic tournament, TODO for boltzmann)
- `crossover_method`: method to use for crossover -- Options(single_point, two_point, annular, uniform)
- `mutation_method`: configure the mutation method
    - `method`: method to choose when to mutate
        - `name`: name of the method to use -- Options(random, gradient)
        - `parameter`: parameter the method uses (deviation to use for gradient)
    - `probability`: mutation probability
    - `mutation`: mutation method to apply -- Options(single_genome, limited_multi-genome, uniform_multi-genome,
      complete)
- `generation_selection`: method for how to choose new generation -- Options(use_all, new_over_actual)
- `n`: number of individuals in a generation
- `k`: number of children to create for the next generation
- `goal`: string describing the goal color with format `r,g,b`
- `palette`: string describing the initial palette of colors separated with `;` for example "
  0,0,0;0,0,255;0,255,0;0,255,255;255,0,0;255,0,255;255,255,0;255,255,255"

A [configuration file](./config_genetic_example.json) is provided as an example

## How it Works

The program generates a population of potential solutions that are combinations of colors in varying proportions. The
fitness of each solution is determined by how close its resulting color is to the desired color. The genetic algorithm
involves the following steps:

1. Initialize a population of potential solutions.
2. Evaluate the fitness of each solution.
3. Select the fittest solutions to reproduce.
4. Generate offspring through crossover and mutation.
5. Evaluate the fitness of the offspring.
6. Select the fittest offspring to form the next generation.
7. Repeat steps 3-6 until a satisfactory solution is found or a maximum number of generations is reached.

The program uses NumPy to generate random numbers and Matplotlib to visualize the fitness of each generation.

## Limitations

This implementation has several limitations:

- It assumes that the colors are a combination of red, green, and blue channels.
- It only considers combinations of colors, whereas other factors such as brightness and saturation can also affect the
  resulting color.
- It may converge to a suboptimal solution if the population size or number of generations is too small, or even if the
  color palette is not adequate.
