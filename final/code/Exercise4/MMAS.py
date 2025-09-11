import numpy as np
import sys
import math
import random
from ioh import get_problem, ProblemClass
from ioh import logger

class MMAS:
    def __init__(self, n, rho, is_star=False):
        self.n = n                     # bitstring length
        self.rho = rho              # evaporation rate P
        self.is_star = is_star         # MMAS* if True, else MMAS
        self.tau = np.full(n, 0.5)     # initial pheromones (prob of choosing 1)

    def construct(self):
        """Construct a solution x based on current pheromones τ"""
        x = []
        for i in range(self.n):
            randomProb = random.random() 
            if(randomProb <= self.tau[i]):
                x.append(1)
            else:
                x.append(0)
        return x

    def update(self, x_best):
        """Update pheromones towards best solution found"""
        for i in range(len(x_best)):
            if(x_best[i] == 1):        #if in the path == 1
                self.tau[i] = min((1-self.rho) * self.tau[i] + self.rho, 1-1/self.n)
            else:
                self.tau[i] = max((1-self.rho) * self.tau[i], 1/self.n)


    def run(self, fitness_function, budget=100000):
        """Main loop"""
        f_opt = -sys.maxsize
        x_best = self.construct()
        f_best = fitness_function(x_best)

        self.update(x_best)  # first pheromone update

        for _ in range(budget):
            x = self.construct()
            f_x = fitness_function(x)

            if (self.is_star and f_x > f_best) or (not self.is_star and f_x >= f_best):
                x_best = x
                f_best = f_x

            self.update(x_best)

        return f_best, x_best

def run_mmas(fitness_function, n, rho, is_star, budget=100000, n_runs=10):
    """Run MMAS algorithm for multiple runs"""
    for run in range(n_runs):
        obj = MMAS(n=n, rho=rho, is_star=is_star)
        f_best, x_best = obj.run(fitness_function, budget=budget)
        print(f"  Run {run+1}: Best fitness = {f_best}")

problemIds = [1, 2, 3, 18, 23, 24, 25]

for pid in problemIds:
    for rho in [1, 1/np.sqrt(100), 1/100]:
        for is_star in [False, True]:
            name = "MMAS*" if is_star else "MMAS"
            
            problem = get_problem(
                fid=pid,
                dimension=100,
                instance=1,
                problem_class=ProblemClass.PBO
            )
            
            l = logger.Analyzer(
                root="data",
                folder_name=f"Exercise4/problem_{pid}_{name}_rho_{rho:.4f}",
                algorithm_info=f"Exercise 4 {name}, rho={rho:.4f}",
                algorithm_name=name
            )
            
            problem.attach_logger(l)
            
            print(f"Running problem {pid}, {name}, rho={rho:.4f}")
            run_mmas(problem, problem.meta_data.n_variables, rho, is_star, budget=100000, n_runs=10)
            
        del l