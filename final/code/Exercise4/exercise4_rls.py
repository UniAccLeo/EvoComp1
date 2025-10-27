from ioh import get_problem, ProblemClass, logger
import os
import sys
import numpy as np
from final.code.Exercise1.problem_runner import problem_runner, rls

problem_ids = [2100, 2101, 2102, 2103, 2200, 2201, 2202, 2203] 
root_data_folder = "C:/Users/USER/Desktop/Evocomp/EvoComp1/data"
n_runs = 30
budget = 100000

for pid in problem_ids:
    print(f"\nRunning One-Plus-One on problem {pid}")
    problem = get_problem(pid, problem_class=ProblemClass.GRAPH)
    
    l = logger.Analyzer(
        root=root_data_folder,
        folder_name=f"Exercise4/Problem_{pid}_rls",
        algorithm_info="Exercise 4",
        algorithm_name="rls"
    )
    problem.attach_logger(l)

    problem_runner(
        mutation_function=rls,
        fitness_function=problem,
        budget=budget,
        n_runs=n_runs
    )

    problem.detach_logger()
    del l
