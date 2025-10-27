from ioh import get_problem, ProblemClass
from ioh import logger

import sys
import numpy as np
import heapq
import random
import os

from final.code.Exercise1.my_EA import my_EA

root_data_folder = "C:/Users/USER/Desktop/Evocomp/EvoComp1/data"

problem_ids = [2100, 2101,2102,2103,2200,2201,2202,2203]
for pid in problem_ids: 
  problem_folder = os.path.join(root_data_folder, f"Exercise4/Problem_{pid}_EA")
  os.makedirs(problem_folder, exist_ok=True)
  l = logger.Analyzer(
  root=root_data_folder,
  folder_name=f"Exercise4/Problem_{pid}_EA",
  algorithm_info=f"Exercise 4",
  algorithm_name="my_EA"
  )   
  problem = get_problem(pid, problem_class=ProblemClass.GRAPH)
  problem.attach_logger(l)
  my_EA(fitness_function=problem, population_size=10, budget=100000, n_runs=30)

del l

# zip -r Ex3run-1.zip data/Exercise3/run-1