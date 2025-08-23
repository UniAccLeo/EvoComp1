import time
import os
import statistics
import random
from typing import List
from tsp import TSP
from evo_algo import Algorithm  

def run_statistical_analysis():
    os.makedirs('results', exist_ok=True)
    results_file = os.path.join('results', 'best_algorithm_stats.txt')
    
    problems = ["eil51", "eil76", "eil101", "st70", "kroA100", 
                "kroC100", "kroD100", "lin105", "pcb442", "pr2392"]  
    
    pop_size = 50
    generations = 20000
    num_runs = 30
    
    with open(results_file, 'w') as f:
        f.write("Instance,AverageCost,StandardDeviation,MinCost,MaxCost\n")
        f.flush()
        
        for prob in problems:
            print(f"\nRunning {prob} {num_runs} times...")
            all_results = []
            
            for run in range(num_runs):
                try:
                    tsp_file = f"data/{prob}.tsp"
                    tsp_instance = TSP.create_from_file(tsp_file)
                    
                    #best algo is GA2
                    result_pop = Algorithm.GA2(pop_size, tsp_instance, generations)
                    
                    # Get best individual 
                    result_pop.individuals.sort(key=lambda ind: ind.fitness)
                    best_individual = result_pop.individuals[0]
                    best_fitness = best_individual.fitness
                    all_results.append(best_fitness)
                    
                    print(f"  Run {run+1}/{num_runs}: {best_fitness}")
                    
                except Exception as e:
                    print(f"  Run {run+1} failed: {e}")
                    continue
            
            if all_results:
                avg_cost = statistics.mean(all_results)
                std_dev = statistics.stdev(all_results) if len(all_results) > 1 else 0
                min_cost = min(all_results)
                max_cost = max(all_results)
                
                f.write(f"{prob},{avg_cost},{std_dev},{min_cost},{max_cost}\n")
                f.flush()
                
                print(f"  {prob} - Avg: {avg_cost:.2f}, Std: {std_dev:.2f}, Min: {min_cost}, Max: {max_cost}")
    
    print("Statistical analysis completed")

def run_comprehensive_tests():
    """Run all algorithms on all problems with different population sizes"""
    os.makedirs('results', exist_ok=True)
    
    problems = ["eil51", "eil76", "eil101", "st70", "kroA100", "kroc100", "krod100", "lin105", "pcb442", "pr2392"]
    population_sizes = [20, 50, 100, 200]
    algorithms = ["GA1", "GA2", "GA3"]
    checkpoints = [2000, 5000, 10000, 20000]
    
    total_runs = len(algorithms) * len(population_sizes) * len(problems)
    current_run = 0
    start_time = time.time()

    for algo_name in algorithms:
        algo_method = getattr(Algorithm, algo_name)
        results_file = os.path.join('results', f'{algo_name}_comprehensive.csv')
        
        with open(results_file, 'w') as f:
            f.write("Instance,PopulationSize,Generation,BestFitness\n")
            f.flush()
            
            for pop_size in population_sizes:
                for prob in problems:
                    current_run += 1
                    run_start = time.time()
                    
                    progress = (current_run / total_runs) * 100
                    print(f"[{progress:.2f}%] {algo_name} | {prob} | Pop={pop_size}")
                    
                    try:
                        tsp_file = f"data/{prob}.tsp"
                        tsp_instance = TSP.create_from_file(tsp_file)
                        
                        # Run algorithm - pass checkpoints and file handle for logging
                        result_pop = algo_method(pop_size, tsp_instance, 20000, checkpoints, f)
                        
                        # Get final result
                        result_pop.individuals.sort(key=lambda ind: ind.fitness)
                        best_individual = result_pop.individuals[0]
                        print(f"    Final fitness: {best_individual.fitness}")
                        
                    except Exception as e:
                        print(f" Error: {e}")
                        # Log error to file
                        f.write(f"{prob},{pop_size},Error,{e}\n")
                        f.flush()
                    
                    # ETA calculation
                    run_time = time.time() - run_start
                    avg_time = (time.time() - start_time) / current_run
                    remaining = avg_time * (total_runs - current_run)
                    print(f"    This run: {run_time:.1f}s | ETA: {remaining/60:.1f} min")

    print("test complete")



if __name__ == "__main__":    
    # # Then run the comprehensive analysis
    # print("\nStarting statistical analysis...")
    # run_statistical_analysis()
    
    # #Uncomment to run comprehensive tests (takes much longer)
    print("\nStarting comprehensive tests...")
    run_comprehensive_tests()