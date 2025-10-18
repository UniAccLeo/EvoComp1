from ioh import get_problem, ProblemClass
from ioh import logger
import sys
import numpy as np
import heapq
import random

def my_EA(fitness_function, population_size = 10, budget = 100000, n_runs = 10):
  if fitness_function.meta_data.problem_id == 18 and fitness_function.meta_data.n_variables == 32:
    optimum = 8
  else:
    optimum = fitness_function.optimum.y
  print(optimum)

  random_chance = float(1/fitness_function.meta_data.n_variables)

  for _ in range(n_runs):
    #initialise population
    population = []
    x_opt = []
    f_opt = sys.float_info.min
    for _ in range(population_size):
      x = np.random.randint(2, size=fitness_function.meta_data.n_variables)
      f = fitness_function(x)
      if(f > f_opt):
        f_opt=f
        x_opt=x.copy()
      heapq.heappush(population, (f, tuple(x)))

    #run iterations
    for _ in range(budget):
      nums = random.sample(range(population_size), 2)
      _, p1 = population[nums[0]]
      _, p2 = population[nums[1]]
      p1 = np.array(p1)
      p2 = np.array(p2)
      x = p1.copy()
      for i in range(fitness_function.meta_data.n_variables):
        if random.random() < random_chance :
          x[i] = np.random.randint(2)
        elif random.random() < 0.5 :
          x[i] = p2[i]
      f =fitness_function(x)
      if(f > f_opt):
        f_opt=f
        x_opt=x.copy()
        if(f >= optimum):
          break
      heapq.heappush(population, (f, tuple(x)))
      heapq.heappop(population)
    fitness_function.reset()
  return f_opt, x_opt

problemIds = [2100, 2101,2102,2103,2200,2201,2202,2203,2300,2301,2302]
for pid in problemIds: 
  l = logger.Analyzer(
  root="data",
  folder_name=f"Exercise1/run/problem_{pid}_myEA",
  algorithm_info=f"Exercise 1",
  algorithm_name="my_EA"
  )   
  problem = get_problem(pid, problem_class=ProblemClass.GRAPH)
  problem.attach_logger(l)
  my_EA(fitness_function=problem, population_size=10, budget=10000, n_runs=30)

del l

# zip -r Ex3run-1.zip data/Exercise3/run-1