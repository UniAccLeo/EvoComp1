# q5.py
import random
from typing import List

class Selection:
    @staticmethod
    def fitness_proportional(population: List, k: int = 1): 
        fitnessVal = []
        for tour in population:
            fitnessVal.append(1/tour.fitness) #find the inverse value since u want the larger fitness values to be worse as fitness = distance 
        totalfitness = sum(fitnessVal)
        selected = []
        for _ in range(k):
            r = random.uniform(0, totalfitness)
            s = 0.0
            for i in range(len(population)):
                s += fitnessVal[i]
                if s >= r:
                    selected.append(population[i])
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
    