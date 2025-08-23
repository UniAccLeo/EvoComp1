#setting up the environment
import math
from typing import List, Tuple, Dict, Optional
from tsp import TSP #importing the tsp solution to the first question
import io
import random

#represents a  individual solution or a tour for TSP
class Individual:
    def __init__(self, tsp: 'TSP'):
        self.tsp = tsp  # we need tsp to calculate the distance
        self.num_cities = int(tsp.dimension)   #number of cities in the problem
        self.permutation: List[int] = [] #list for the permutations
        self.fitness: float = None  #stores the total distance of the tour

    #Initialises a random tour
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
            #uses the % to loop back to the first city making it a cyclic tour
            distance += self.tsp.distance_matrix[a][b]
        self.fitness = distance
        #the distance is then stored in self.fitness
        return distance
    #just provides a readable string representation for printing an Individual
    #shows both the order of cities and the tour length
    def __str__(self):
        return f"Tour: {self.permutation} | Fitness: {self.fitness}"


# represents a group of soltuions for TSP
class Population:
    def __init__(self, size: int, tsp: 'TSP'):
        self.size = size #the amount of individuals in the population
        self.tsp = tsp #list storing all the individual objects
        self.individuals: List[Individual] = []

    #Creatres n number of random tours and then evals them
    def initialize(self):
        #everytime initiallize is called the population resets
        #create random population
        self.individuals = []
        for _ in range(self.size):
            ind = Individual(self.tsp)
            ind.random_init()
            #each individual is immediately evaluated so that its fitness is ready for selection
            ind.evaluate()
            self.individuals.append(ind)

    #Return the individual with the smallest tour

    def best_individual(self):
        #return the minimum tour length
        return min(self.individuals, key=lambda ind: ind.fitness) #inbuilt min function used to calc the shortest

    #Computes the average tour length of the population
    def average_fitness(self):
        #return the average tour length in the pop
        return sum(ind.fitness for ind in self.individuals) / self.size

    #String output showing te individuals in the population
    def __str__(self):
        return "\n".join(str(ind) for ind in self.individuals)