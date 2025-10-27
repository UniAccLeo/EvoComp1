from ioh import get_problem, ProblemClass, logger
import os
import pandas as pd
from final.code.Exercise2.GSEMO import GSEMO  


problem_ids = [2100, 2101, 2102, 2103, 2200, 2201, 2202, 2203]  
n_runs = 30
budget = 100000  
root_data_folder = "C:/Users/USER/Desktop/Evocomp/EvoComp1/data"

for pid in problem_ids:
    print(f"\n🚀 Running GSEMO on problem {pid}...")

    problem_folder = os.path.join(root_data_folder, f"Exercise4/Problem_{pid}_GSEMO")
    os.makedirs(problem_folder, exist_ok=True)

    # Create IOH logger
    l = logger.Analyzer(
        root=root_data_folder,
        folder_name=f"Exercise4/Problem_{pid}_GSEMO",
        algorithm_name="GSEMO",
        algorithm_info="Exercise 4 - Multiobjective GSEMO",
    )

    # Load problem instance
    problem = get_problem(pid, problem_class=ProblemClass.GRAPH)
    problem.attach_logger(l)

    all_tradeoffs = []

    # Run 30 independent runs
    for run in range(n_runs):
        population = GSEMO(problem, budget=budget)
        tradeoff = [(fit[0], fit[1], run + 1) for _, fit in population]
        all_tradeoffs.extend(tradeoff)
        problem.reset()

    # Save results to CSV
    df = pd.DataFrame(all_tradeoffs, columns=["submodular_value", "neg_cost", "run"])
    csv_path = os.path.join(problem_folder, f"GSEMO_{pid}_all_runs_tradeoff.csv")
    df.to_csv(csv_path, index=False)
    print(f"✅ Results saved to: {csv_path}")

    # Cleanup
    problem.detach_logger()
    del l

print("\n🎯 All GSEMO runs completed successfully!")
