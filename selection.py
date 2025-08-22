# q5.py
import random
from typing import List

class Selection:
    @staticmethod
    def fitness_proportional(population: List, k: int = 1): #need to fix as its returning the wrong ones.
        total_fitness = sum(ind.fitness for ind in population)
        if total_fitness == 0:
            return random.sample(population, k)
        selected = []
        for _ in range(k):
            r = random.uniform(0, total_fitness)
            s = 0.0
            for ind in population:
                s += ind.fitness
                if s >= r:
                    selected.append(ind)
                    break
        return selected

    @staticmethod
    def tournament(population: List, k: int = 1, t_size: int = 3): #population list, number of individuals to select, tournament size
        selected = []
        for _ in range(k):
            competitors = random.sample(population, t_size)
            best = max(competitors, key=lambda ind: ind.fitness)
            selected.append(best)
        return selected

    @staticmethod
    def elitism(population: List, elite_size: int = 1):
        return sorted(population, key=lambda ind: ind.fitness, reverse=True)[:elite_size]
    