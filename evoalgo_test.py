import os
import statistics
from evo_algo import Algorithm
from tsp import TSP

def run_statistical_analysis():
    os.makedirs('results', exist_ok=True)
    results_file = os.path.join('results', 'evo.txt')

    #tsp instances
    problems = ["eil51", "eil76", "eil101", "st70", "kroA100", 
                "kroC100", "kroD100", "lin105", "pcb442", "pr2392", "usa13509"]  
    
    #genetic algorihtm parameters
    pop_size = 50           #population size of all runs
    generations = 20000     #number of generations to evolve
    num_runs = 30           #number of runs per problem
    
    # Preload TSP instances to save loading 29 time by storing into hashmap
    print("Preloading TSP instances for statistical analysis...")
    tsp_instances = {}
    for prob in problems:
        try:
            tsp_file = f"data/{prob}.tsp"
            tsp_instances[prob] = TSP.create_from_file(tsp_file)
        except Exception as e:
            print(f"Failed to load {prob}: {e}")
            tsp_instances[prob] = None

    #open the results folder and write the csv header titles
    with open(results_file, 'w') as f:
        f.write("Instance,AverageCost,StandardDeviation,MinCost,MaxCost\n")
        
        #process each TSP problem
        for prob in problems:
            print(f"\nRunning {prob} {num_runs} times...")
            all_results = [] #store results for the current problem
            tsp_instance = tsp_instances[prob]
                
            for run in range(num_runs):
                try:
                    #run GA2 which is best performing algorithm
                    result_pop = Algorithm.GA2(pop_size, tsp_instance, generations)
                    best_fitness = result_pop.individuals[0].fitness
                    all_results.append(best_fitness)
                    print(f"Run {run+1}/{num_runs}: {best_fitness}")
                    
                except Exception as e:
                    print(f"Run {run+1} failed: {e}")
                    continue
            #calculate the statistics if we have successful runs 
            if all_results:
                avg_cost = statistics.mean(all_results)
                std_dev = statistics.stdev(all_results) 
                min_cost = min(all_results)
                max_cost = max(all_results)
                #write results to the file and print in terminal
                f.write(f"{prob},{avg_cost},{std_dev},{min_cost},{max_cost}\n")
                print(f"Summary - Avg: {avg_cost:.2f}, Std: {std_dev:.2f}, Min: {min_cost}, Max: {max_cost}")

def run_tests():
    #this function tests all three GA algorihtms across different population sizes and problem instances, testing GA1,GA2 and GA3 performance
    os.makedirs('results', exist_ok=True)
    problems = ["eil51", "eil76", "eil101", "st70", "kroA100", 
                "kroC100", "kroD100", "lin105", "pcb442", "pr2392", "usa13509"]  
    population_sizes = [20, 50, 100, 200]
    algorithms = ["GA1", "GA2", "GA3"]
    checkpoints = [2000, 5000, 10000, 20000]
    
    # Preload TSP instances
    print("Preloading TSP instances for comprehensive tests...")
    tsp_instances = {}
    for prob in problems:
        try:
            tsp_file = f"data/{prob}.tsp"
            tsp_instances[prob] = TSP.create_from_file(tsp_file)
        except Exception as e:
            print(f"Failed to load {prob}: {e}")
            tsp_instances[prob] = None
    #testing each algorithm
    for algo_name in algorithms:
        algo_method = getattr(Algorithm, algo_name)
        results_file = os.path.join('results', f'{algo_name}_test.csv')
        
        #create results file
        with open(results_file, 'w') as f:
            f.write("Instance,PopulationSize,Generation,BestFitness\n")
            
            #test all population sizes
            for pop_size in population_sizes:
                #test all problem instances
                for prob in problems:
                    tsp_instance = tsp_instances[prob]
                        
                    try:
                        #run the algorihtm with checkpoint logging
                        print(f"Running {algo_name}, pop={pop_size}, on {prob}...")
                        result_pop = algo_method(pop_size, tsp_instance, 20000, checkpoints, f)
                        final_fitness = result_pop.individuals[0].fitness
                        f.write(f"{prob},{pop_size},Final,{final_fitness}\n")
                        
                    except Exception as e:
                        print(f"Error running {prob} with {algo_name}: {e}")
                        f.write(f"{prob},{pop_size},Error,{e}\n")

if __name__ == "__main__":    
    run_statistical_analysis()
    run_tests()