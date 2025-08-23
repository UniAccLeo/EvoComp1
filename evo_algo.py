#exercise 6
from tsp import TSP;
from operators import Operators
from selection import Selection
from population_rep import Population, Individual
from operators2 import Operators2   
import heapq
import random

class Algorithm:

    @staticmethod
    def GA1(population_size: int, tspFile: TSP, generations: int, checkpoints=None, log_file=None):
        #algorithm 1 using OX and inversion 
        tsp = tspFile
        #load the population
        pop = Population(population_size, tsp)
        #instantiate instance of operator class
        Op = Operators
        #store the tour distance of each individual in the population 
        CurrGen = 0
        pop.initialize()
        for ind in pop.individuals:
            ind.evaluate()
        #select the two parents
        while(CurrGen < generations):
            #print(CurrGen) --> for debugging 
            children = []
            while(len(children) < pop.size):
                parents = Selection.tournament(pop.individuals, 2, 5) #picks two parents, from a tournament size of 5 migh tneed to adjust
                #perform crossover 
                children_pair = [
                    Op.OrderCrossover(parents[0].permutation, parents[1].permutation),
                    Op.OrderCrossover(parents[1].permutation, parents[0].permutation)
                ]
                #perform mutation on both children & find the legnth of each child
                for child in children_pair:
                    temp = Individual(tsp)
                    child = Op.Inversion(child)
                    temp.permutation = child
                    temp.evaluate()#sould find the distance 
                    children.append(temp)
            #keep best population_size solution
            pop.individuals.extend(children)
            pop.individuals.sort(key = lambda ind: ind.fitness)
            pop.individuals = pop.individuals[:pop.size]
            CurrGen = CurrGen + 1

            #print fitness at the generation checkpoints 2000, 5000,10000, 20000
            if checkpoints and CurrGen in checkpoints:
                best_ind = pop.best_individual()
                if log_file:
                    log_file.write(f"{tspFile.name},{population_size},{CurrGen},{best_ind.fitness}\n")
                    log_file.flush()
                print(f"Checkpoint {CurrGen}: Best fitness = {best_ind.fitness}")
        
        return pop
    
    @staticmethod
    def GA2(population_size: int, tspFile: TSP, generations: int, checkpoints=None, log_file=None):
        tsp = tspFile
        pop = Population(population_size, tsp)
        Op = Operators
        pop.initialize()
        CurrGen = 0 
        for ind in pop.individuals:
            ind.evaluate()

        while(CurrGen < generations):
            #print(CurrGen)
            children = []
            while(len(children) < pop.size):
                parents = Selection.tournament(pop.individuals, 2, 5) #picks two parents, from a tournament size of 5 migh tneed to adjust
                #perform crossover 
                child = Op.EdgeRecombination(parents[0].permutation, parents[1].permutation)
                #perform mutation on child
                if random.random() < 0.3:
                    child = Op.Insert(child)
                temp = Individual(tsp)
                temp.permutation = child
                temp.evaluate()#sould find the distance 
                children.append(temp)
            #keep best population_size solution
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
        tsp = tspFile
        pop = Population(population_size, tsp)
        Op = Operators
        pop.initialize()
        CurrGen = 0 
        for ind in pop.individuals:
            ind.evaluate()

        while(CurrGen < generations):
            children = []

            bestChild = pop.best_individual() #bestChild is a reference
            tempElite = Individual(tsp)
            tempElite.permutation = bestChild.permutation.copy()
            tempElite.evaluate()
            children.append(tempElite)

            while(len(children) < pop.size):
                #FPS
                parents= Selection.fitness_proportional(pop.individuals, 2)
                #cycle crossover
                childPerm = Op.CycleCrossover(parents[0].permutation, parents[1].permutation)
                #swap mutation 
                if(random.random() < 0.3):
                    childPerm = Op.Swap(childPerm)
                 # Create and evaluate child
                childInd = Individual(tsp)
                childInd.permutation = childPerm 
                childInd.evaluate()
                children.append(childInd)
        #generational replacement
            pop.individuals = children
            CurrGen = CurrGen + 1

            if checkpoints and CurrGen in checkpoints:
                best_ind = pop.best_individual()
                if log_file:
                    log_file.write(f"{tspFile.name},{population_size},{CurrGen},{best_ind.fitness}\n")
                    log_file.flush()
                print(f"Checkpoint {CurrGen}: Best fitness = {best_ind.fitness}")

        return pop
       

def testAlgo():
    populationSize = 200
    generationSize = 20000
    tsp_file = "data/eil51.tsp"

    tsp = TSP.create_from_file(tsp_file)

    result_pop = Algorithm.GA1(populationSize, tsp, generationSize)

    # Get final best individual
    best_individual = result_pop.best_individual()
    print(f"Best tour length: {best_individual.fitness}")
    print(f"Best tour: {best_individual.permutation}")
    
    return result_pop

def testAlgo2():
    populationSize = 200
    generationSize = 2000
    tsp_file = "data/eil51.tsp"

    tsp = TSP.create_from_file(tsp_file)

    result_pop = Algorithm.GA2(populationSize, tsp, generationSize)

    # Get final best individual
    best_individual = result_pop.individuals[0]  # Population is already sorted
    print(f"GA2 - Best tour length: {best_individual.fitness}")
    print(f"GA2 - Best tour: {best_individual.permutation}")
    
    return result_pop

def testAlgo3():
    populationSize = 200
    generationSize = 2000
    tsp_file = "data/eil51.tsp"

    tsp = TSP.create_from_file(tsp_file)

    result_pop = Algorithm.GA3(populationSize, tsp, generationSize)

    # Get final best individual
    best_individual = result_pop.individuals[0]  # Population is already sorted
    print(f"GA3 - Best tour length: {best_individual.fitness}")
    print(f"GA3 - Best tour: {best_individual.permutation}")
    
    return result_pop

if __name__ == "__main__":
    testAlgo3()

