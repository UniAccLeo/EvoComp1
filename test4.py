import time
import os
import statistics
import random
from typing import List
from tsp import TSP
from evo_algo import Algorithm  


def run_statistical_analysis():
    os.makedirs('results', exist_ok=True)
    results_file = os.path.join('results', 'best_algorithm_stats4.txt')
    
    problems = ["usa13509"]  
    
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


if __name__ == "__main__":
    run_statistical_analysis()