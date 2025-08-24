import time
import os
import statistics
import random
from typing import List
from tsp import TSP
from evo_algo import Algorithm  

def run_comprehensive_tests():
    """Run GA3 on all problems with different population sizes"""
    os.makedirs('results', exist_ok=True)
    
    problems = ["eil51", "eil76", "eil101", "st70", "kroA100", "kroc100", "krod100", "lin105", "pcb442", "pr2392"]
    population_sizes = [20, 50, 100, 200]
    checkpoints = [2000, 5000, 10000, 20000]
    
    algo_name = "GA3"
    algo_method = getattr(Algorithm, algo_name)
    results_file = os.path.join('results', f'{algo_name}_comprehensive.csv')
    
    total_runs = len(population_sizes) * len(problems)
    current_run = 0
    start_time = time.time()
    
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
                    
                    # Run GA3 - pass checkpoints and file handle for logging
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
    
    print("GA3 comprehensive test complete")


if __name__ == "__main__":
    print("\nDEBUG: test.py started")
    run_comprehensive_tests()
        
