import math
from typing import List, Tuple, Dict, Optional
from tsp import TSP
import io
import random
from typing import List

class Individual:
    def __init__(self, tsp: 'TSP'):
        self.tsp = tsp
        self.num_cities = int(tsp.dimension)
        self.permutation: List[int] = []
        self.fitness: float = None

    def random_init(self):
        #randomizer O(N)
        self.permutation = list(range(self.num_cities))
        for i in range(self.num_cities - 1, 0, -1):
            j = random.randint(0, i)
            self.permutation[i], self.permutation[j] = self.permutation[j], self.permutation[i]

    def evaluate(self):
        #calc the total distance using the tsp matrix
        distance = 0
        for i in range(self.num_cities):
            a = self.permutation[i]
            b = self.permutation[(i + 1) % self.num_cities] #go back to the start
            distance += self.tsp.distance_matrix[a][b]
        self.fitness = distance
        return distance

    def __str__(self):
        return f"Tour: {self.permutation} | Fitness: {self.fitness}"


class Population:
    def __init__(self, size: int, tsp: 'TSP'):
        self.size = size
        self.tsp = tsp
        self.individuals: List[Individual] = []

    def initialize(self):
        #create random population
        self.individuals = []
        for _ in range(self.size):
            ind = Individual(self.tsp)
            ind.random_init()
            ind.evaluate()
            self.individuals.append(ind)

    def best_individual(self):
        #return the minimum tour length
        return min(self.individuals, key=lambda ind: ind.fitness)

    def average_fitness(self):
        #return the average tour length in the pop
        return sum(ind.fitness for ind in self.individuals) / self.size

    def __str__(self):
        return "\n".join(str(ind) for ind in self.individuals)