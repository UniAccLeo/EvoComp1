import os
import sys
import random
import numpy as np
from ioh import get_problem, ProblemClass
from ioh import logger

class ACO:
    def __init__(self, n, n_ants=10, rho=0.1, q=1.0, local_search=True):
        self.n = n 
        self.n_ants = n_ants
        self.rho = rho  #Evaporation rate         
        self.q = q      #Phermone intensity

        #Initialise phermone values       
        self.tau = np.full(n, 0.5, dtype=float)  
        self.local_search = local_search

        #Min and max phermone limits
        self.tau_min = 1.0 / (self.n * 10)
        self.tau_max = 1.0 - self.tau_min

    def prob_from_tau(self):
        return np.clip(self.tau, self.tau_min, self.tau_max)

    #Construct a solution based on phermone prob
    def construct_solution(self):
        probs = self.prob_from_tau()
        #Randomly assign 1 if rand < tau_i
        return (np.random.rand(self.n) < probs).astype(np.int32)

    #Local search to improve a solution 
    def local_search_improve(self, x, fitness_function):
        f_current = fitness_function(x)
        improved = True

        #Loop until no improvement is found
        while improved:
            improved = False
            for i in range(self.n):
                x_try = x.copy()
                x_try[i] = 1 - x_try[i]
                f_try = fitness_function(x_try)
                if f_try > f_current:
                    x, f_current = x_try, f_try
                    improved = True
                    break  
        return x, f_current

    #Update phermone levels based on best solution 
    def update_pheromones(self, x_best, f_best):
        #Evaporation 
        self.tau = (1.0 - self.rho) * self.tau
        
        #Deposit
        increment = self.rho * self.q * f_best  
        self.tau += x_best.astype(float) * increment

        #Apply phermone limits 
        self.tau = np.clip(self.tau, self.tau_min, self.tau_max)

    def run(self, fitness_function, budget=100000):
        f_best, x_best = -sys.maxsize, None
        evals = 0 #No of evaluations 

        #Continue until eval budget used 
        while evals < budget:
            solutions, fitnesses = [], []

            for _ in range(self.n_ants):
                sol = self.construct_solution()
                f = fitness_function(sol)
                evals += 1
                solutions.append(sol)
                fitnesses.append(f)

                #Track global best solution 
                if f > f_best:
                    f_best, x_best = f, sol.copy()

                if evals >= budget:
                    break
            #Local search on iteration bests solution 
            if self.local_search and evals < budget:
                iter_best_idx = int(np.argmax(fitnesses))
                sol_ls, f_ls = self.local_search_improve(solutions[iter_best_idx], fitness_function)
                if f_ls > f_best:
                    f_best, x_best = f_ls, sol_ls

            #Phermone update
            if x_best is not None:
                self.update_pheromones(x_best, f_best)

        return f_best, x_best



def run_aco_experiment(problem, folder_name, n_ants=10, budget=100000, n_runs=10):
    
    root = "data"
    os.makedirs(root, exist_ok=True)

    l = logger.Analyzer(
        root=root,
        folder_name=folder_name,
        algorithm_info=f"Exercise 5 ACO with {n_ants} ants, rho=0.1, local_search",
        algorithm_name="ACO"
    )
    problem.attach_logger(l)

    try:
        for run in range(n_runs):
            
            aco = ACO(n=problem.meta_data.n_variables, n_ants=n_ants, rho=0.1,q=1.0, local_search=True)
            f_best, x_best = aco.run(problem, budget=budget)
            print(f"[{folder_name}] Run {run+1}/{n_runs} best fitness = {f_best}")
            try:
                problem.reset()
            except Exception:
                pass
    finally:
        if hasattr(l, "close"):
            try:
                l.close()
            except Exception:
                pass
        if hasattr(problem, "detach_logger"):
            try:
                problem.detach_logger(l)
            except Exception:
                pass
        del l

    full_path = os.path.join(root, folder_name)
    print("Log folder created at:", full_path)
    if os.path.exists(full_path):
        files = os.listdir(full_path)
        print(f"  Files in {full_path} (first 20):", files[:20])
    else:
        print("  Warning: folder does not exist after run.")

if __name__ == "__main__":
    problemIds = [1, 2, 3, 18, 23, 24, 25]

    for pid in problemIds:
        problem = get_problem(
            fid=pid,
            dimension=100,
            instance=1,
            problem_class=ProblemClass.PBO
        )

        folder_name = f"Exercise5/problem_{pid}_ACO10"
        print(f"Running ACO on problem {pid}, logs -> data/{folder_name}")
        run_aco_experiment(problem, folder_name, n_ants=10, budget=100000, n_runs=10)
