from tsp import TSP
from population_rep import Population

if __name__ == "__main__":

    tsp = TSP.create_from_file("./data/ch150.tsp")

    pop = Population(size=5, tsp=tsp)
    pop.initialize()

    print("Population:")
    print(pop)
    print("\nBest individual:")
    print(pop.best_individual())
    print("\nAverage fitness:", pop.average_fitness())
