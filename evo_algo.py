#exercise 6
from tsp import TSP;
from operators import Operators
from selection import Selection
from population_rep import Population, Individual

import heapq
import random

class Algorithm:

    @staticmethod
    def GA1(population_size: int, tspFile: TSP, generations: int, checkpoints=None, log_file=None):
        """
        Genetic Algorithm 1 (GA1):
        - Uses Order Crossover (OX) for crossover
        - Uses Inversion for mutation
        - Selection method: Tournament selection
        - Replacement:(μ + λ) selection)/elitism
        """
        tsp = tspFile
        #initialise population with given size
        pop = Population(population_size, tsp)
        #operator methods for crossover and mutation
        Op = Operators 
        #store the tour distance of each individual in the population 
        CurrGen = 0
        pop.initialize() #randomly initialise individuals

        #evaluate initial population fitness
        for ind in pop.individuals:
            ind.evaluate()
        
        #evo loop
        while(CurrGen < generations):
            children = []

            #generate new offspring until we reach the population size
            while(len(children) < pop.size):
                parents = Selection.tournament(pop.individuals, 2, 5) #picks two parents, from a tournament size of 5
                #perform crossover for both children
                children_pair = [
                    Op.OrderCrossover(parents[0].permutation, parents[1].permutation),
                    Op.OrderCrossover(parents[1].permutation, parents[0].permutation)
                ]
                #perform inversion mutation on both children & find the tour distacne of each child
                for child in children_pair:
                    temp = Individual(tsp)
                    child = Op.Inversion(child)
                    temp.permutation = child
                    temp.evaluate()#sould find the distance 
                    children.append(temp)
            #combine old and new individuals, sort by fitness and keep the best
            pop.individuals.extend(children)
            pop.individuals.sort(key = lambda ind: ind.fitness)
            pop.individuals = pop.individuals[:pop.size]
            CurrGen = CurrGen + 1

            #chcekpoint logging print and write to file 
            if checkpoints and CurrGen in checkpoints:
                best_ind = pop.best_individual()
                if log_file:
                    log_file.write(f"{tspFile.name},{population_size},{CurrGen},{best_ind.fitness}\n")
                    log_file.flush()
                print(f"Checkpoint {CurrGen}: Best fitness = {best_ind.fitness}")
        
        return pop
    
    @staticmethod
    def GA2(population_size: int, tspFile: TSP, generations: int, checkpoints=None, log_file=None):
        """
        Genetic Algorithm 2 (GA2):
        - Uses Edge Recombination for crossover
        - Uses Insert mutation with 30% probability
        - Selection: Tournament selection
        - Replacement:(μ + λ) selection)/eltisims
        """
        tsp = tspFile
        pop = Population(population_size, tsp)
        Op = Operators
        pop.initialize()
        CurrGen = 0 
        for ind in pop.individuals:
            ind.evaluate()

        #evo loop
        while(CurrGen < generations):
            print(CurrGen)
            children = []
            while(len(children) < pop.size):
                parents = Selection.tournament(pop.individuals, 2, 5) #picks two parents, from a tournament size of 5 migh tneed to adjust
                #perform crossover 
                child = Op.EdgeRecombination(parents[0].permutation, parents[1].permutation)
                #perform insert mutation with 30% probability 
                if random.random() < 0.3:
                    child = Op.Insert(child)

                #create and evaluate new child (only one)
                temp = Individual(tsp)
                temp.permutation = child
                temp.evaluate()
                children.append(temp)

            #combine and keep the best individual
            pop.individuals.extend(children)
            pop.individuals.sort(key = lambda ind: ind.fitness)
            pop.individuals = pop.individuals[:pop.size]
            CurrGen = CurrGen + 1

            if checkpoints and CurrGen in checkpoints:
                best_ind = pop.best_individual()
                if log_file:
                    log_file.write(f"{tspFile.name},{population_size},{CurrGen},{best_ind.fitness}\n")
                    log_file.flush()
                print(f"Checkpoint {CurrGen}: Best fitness = {best_ind.fitness}")
        
        return pop
            
    @staticmethod 
    def GA3(population_size: int, tspFile: TSP, generations: int, checkpoints=None, log_file=None):
        """
        Genetic Algorithm 3 (GA3):
        - Uses Cycle Crossover for crossover
        - Uses Swap mutation with 30% probability
        - Selection: Fitness Proportional Selection (FPS)
        - Elitism: Keeps the best individual from previous generation
        """
        tsp = tspFile
        pop = Population(population_size, tsp)
        Op = Operators
        pop.initialize()
        CurrGen = 0 

        for ind in pop.individuals:
            ind.evaluate()

        #evo loop
        while(CurrGen < generations):
            children = []
            #apply elitism: copy the best individual to next generation 
            bestChild = pop.best_individual() 
            tempElite = Individual(tsp)
            tempElite.permutation = bestChild.permutation.copy()
            tempElite.evaluate()
            children.append(tempElite)

            #generate remaining children
            while(len(children) < pop.size):
                #Fitness proprotional selction to select parents
                parents= Selection.fitness_proportional(pop.individuals, 2)
                #cycle crossover
                childPerm = Op.CycleCrossover(parents[0].permutation, parents[1].permutation)
                #swap mutation with 30% probability
                if(random.random() < 0.3):
                    childPerm = Op.Swap(childPerm)
                 # Create and evaluate child
                childInd = Individual(tsp)
                childInd.permutation = childPerm 
                childInd.evaluate()
                children.append(childInd)
        #generational repalcement by replacing the old population with the new one
            pop.individuals = children
            CurrGen = CurrGen + 1

            if checkpoints and CurrGen in checkpoints:
                best_ind = pop.best_individual()
                if log_file:
                    log_file.write(f"{tspFile.name},{population_size},{CurrGen},{best_ind.fitness}\n")
                    log_file.flush()
                print(f"Checkpoint {CurrGen}: Best fitness = {best_ind.fitness}")

        return pop
       


