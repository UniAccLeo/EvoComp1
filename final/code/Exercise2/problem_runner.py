from ioh import get_problem, ProblemClass
from ioh import logger
import sys
import numpy as np

def problem_runner(mutation_function, fitness_function, budget = None, n_runs = 10):
  if budget is None:
      budget = int(fitness_function.meta_data.n_variables * fitness_function.meta_data.n_variables * 50)

  if fitness_function.meta_data.problem_id == 18 and fitness_function.meta_data.n_variables == 32:
      optimum = 8
  else:
      optimum = fitness_function.optimum.y
  print(optimum)
  for r in range(n_runs):
    f_opt = sys.float_info.min
    x_opt = None
    f = sys.float_info.min
    x = np.random.randint(2, size = fitness_function.meta_data.n_variables)
    for i in range(budget):
      x_new = mutation_function(x, fitness_function.meta_data.n_variables)
      f_new = fitness_function(x_new)
      if f_new > f :
        f = f_new
        x = x_new
        if f > f_opt:
          f_opt = f
          x_opt = x
        if f_opt >= optimum:
          break
    fitness_function.reset()
  return f_opt, x_opt

def random_search(x, size):
  return np.random.randint(2, size)

def RLS(x, size):
  x_copy = x.copy()
  flip_idx = np.random.randint(size)
  x_copy[flip_idx] = 1 - x_copy[flip_idx]
  return x_copy

def OnePlusOne(x, size):
  flip_chance = float(1/size)
  x_copy = x.copy()
  for s in range(size):
    if(np.random.rand() < flip_chance):
      x_copy[s] = 1- x_copy[s]
  return x_copy