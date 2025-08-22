import time
import os
from tsp import TSP
from evo_algo import Algorithm

def main():
    os.makedirs('results', exist_ok=True)
    path = os.path.join('results', 'GA1_Test.txt')

    problems = ["eil51", "eil76", "eil101", "st70", "kroa100",
                "kroc100", "krod100", "lin105", "pcb442", "pr2392", "usa13509"]

    population_sizes = [20, 50, 100, 200]
    checkpoints = [2000, 5000, 10000, 20000]  # always run full 20,000 gens

    total_runs = len(population_sizes) * len(problems)
    current_run = 0
    start_time = time.time()

    with open(path, 'w') as f:
        # Write the CSV header once at the top of the file
        f.write("Instance,PopulationSize,Generation,BestFitness\n")
        f.flush()

        for pop_size in population_sizes:
            for prob in problems:
                current_run += 1
                run_start = time.time()

                progress = (current_run / total_runs) * 100
                print(f"\n[{progress:.2f}%] Running {prob} | Pop={pop_size} | Gens=20000")

                try:
                    tsp_file = f"data/{prob}.tsp"
                    tsp_instance = TSP.create_from_file(tsp_file)

                    # NO HEADER HERE - We write a simple CSV line for each checkpoint
                    # Call the algorithm for a full 20,000 generations.
                    # It will log at generations 2000, 5000, 10000, 20000 internally.
                    result_pop = Algorithm.GA1(pop_size, tsp_instance, 20000, checkpoints, log_file=f)

                    # After the run is complete, you can also log the final result if you want.
                    best_individual = result_pop.individuals[0]
                    print(f"    ✅ Done. Final Fitness = {best_individual.fitness}")

                except Exception as e:
                    # Log errors in the CSV format too
                    f.write(f"{prob},{pop_size},Error,{e}\n")
                    f.flush()
                    print(f"    ❌ Error: {e}")

                # ETA calculation
                run_time = time.time() - run_start
                avg_time_per_run = (time.time() - start_time) / current_run
                remaining_time = avg_time_per_run * (total_runs - current_run)
                print(f"    ⏱ Time for this run: {run_time:.2f}s | ETA: {remaining_time/60:.2f} min")

    print("\n✅ All tests completed.")
    total_time = time.time() - start_time
    print(f"Total time: {total_time/60:.2f} minutes")


if __name__ == "__main__":
    main()