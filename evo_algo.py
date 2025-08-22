#exercise 6
from tsp import TSP;
from operators import Operators
from selection import Selection
from population_rep import Population, Individual
from operators2 import Operators2   
import heapq

class Algorithm:

    @staticmethod
    def GA1(population_size: int, tspFile: TSP, generations: int):
        #algorithm 1 using OX and inversion 
        tsp = TSP.create_from_file(tspFile)
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
            parents = Selection.tournament(pop.individuals, 2, 3)

            #perform crossover 
            Op.OrderCrossover(parents)

            #perform mutation on the child

            




        

# if __name__ == "__main__":
#     Algoritham.GA1()  # run the GA1 setup

#     # Example test: check population size
#     tsp = TSP.create_from_file("data/eil101.tsp")
#     pop = Population(20, tsp)
#     pop.initialize()
#     assert len(pop.individuals) == 20, "Population size should be 20"

#     # Test: fitness is evaluated and positive
#     for ind in pop.individuals:
#         dist = ind.evaluate()
#         assert dist > 0, f"Distance should be positive, got {dist}"
    
#     # Test: priority queue ordering
#     pq = []
#     for ind in pop.individuals:
#         heapq.heappush(pq, (ind.fitness, ind))

#     # Pop all elements from heap and check order
#     last_fitness = -1
#     while pq:
#         fitness, ind = heapq.heappop(pq)
#         print(f"Tour distance: {fitness}")
#         assert last_fitness <= fitness, "Heap order incorrect"
#         last_fitness = fitness

#     print("All tests passed!")


            

