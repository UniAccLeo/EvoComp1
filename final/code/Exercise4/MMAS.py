import numpy as np
import sys
import math
import random
from ioh import get_problem, ProblemClass
from ioh import logger

class MMAS:
    def __init__(self, n, p, is_star=False):
        self.n = n                     # bitstring length
        self.p = p              # evaporation rate P
        self.is_star = is_star         # MMAS* if True, else MMAS
        self.pheromones = np.full(n, 0.5)     # initial pheromones(prob of choosing a 1)

    def construct(self):
        #create a solution x using the current known pheromone values
        x = []
        for i in range(self.n):
            #current pheromone weight for choosing 1 and 0 at bit i
            phero_weight_1 = self.pheromones[i]
            phero_weight_0 = 1.0 - self.pheromones[i]
            #normalise
            total = phero_weight_0 + phero_weight_1
            p1 = phero_weight_1/total

            #sample a bit using probabilites
            randomProb = random.random() 
            if(randomProb <= p1):
                x.append(1)
            else:
                x.append(0)
        return x

    def update(self, x_best):
        #Update pheromones towards best solution found
        for i in range(len(x_best)):
            if(x_best[i] == 1):        #if in the path == 1
                self.pheromones[i] = min((1-self.p) * self.pheromones[i] + self.p, 1-1/self.n)
            else:
                self.pheromones[i] = max((1-self.p) * self.pheromones[i], 1/self.n)


    def run(self, fitness_function, budget=100000):
       #main loop
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
    
def run_mmas(problem, n, p, is_star, budget=100000, n_runs=10, name="MMAS", l=None):
    #Run MMAS algorithm for 10 runs in same file
    for run in range(1, n_runs+1):
        if l is not None:
            l.start_run() # start run in logger
        problem.reset()         

        obj = MMAS(n=n, p=p, is_star=is_star)
        f_best, x_best = obj.run(problem, budget=budget)
        print(f"  Run {run}: Best fitness = {f_best}")

        if l is not None:
            l.end_run()# end run in logger


problemIds = [1, 2, 3, 18, 23, 24, 25]
for pid in problemIds:
    for p in [1, 1/np.sqrt(100), 1/100]:
        for is_star in [False, True]:
            name = "MMASstar" if is_star else "MMAS"
            problem = get_problem(
                fid=pid,
                dimension=100,
                instance=1,
                problem_class=ProblemClass.PBO
            )
            l = logger.Analyzer(
                root="data",
                folder_name=f"Exercise4/problem_{pid}_{name}_p_{p:.4f}",
                algorithm_info=f"Exercise 4 {name}, p={p:.4f}",
                algorithm_name=name
            )
            problem.attach_logger(l)
            run_mmas(problem, problem.meta_data.n_variables, p, is_star, budget=100000, n_runs=10, name=name)
            problem.detach_logger()
            del l
            del problem
