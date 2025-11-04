import ioh
import random 
from ioh import logger
import os          
import pandas as pd 

def fitness(x, problem):
    """
    Multi-objective fitness:
    - objective 1: submodular value from IOHprofiler
    - objective 2: cost (negative, since we want to minimize)
    """
    objValue = problem(x)
    cost = sum(x) #since each node has cost 1, you can just add all of it
    return (objValue, -cost)


def GSEMO(problem, budget=10000):
    #choose x uniformly at random
    num_variables = problem.meta_data.n_variables
    x = [0]*num_variables
    for i in range(num_variables):
        choice = random.randint(0,1)
        x[i] = choice

    #determine g(x)
    g_x = fitness(x, problem)
    
    #define population
    population = [(x, g_x)]

    #run loop
    num_eval = 1
    while num_eval < budget:
        if num_eval % 1000 == 0:
            print(f"{num_eval} completed!")
        parent, parent_fit = random.choice(population)
        #mutation
        n = len(parent)
        child = parent.copy()
        for i in range(n):
            if(random.random() < 1/n):
                child[i] = 1 - child[i] #flip the bit either 0 to 1 or 1 - 0
        child_fitness = fitness(child, problem)
        num_eval += 1
        f_value = child_fitness[0]
        neg_cost = child_fitness[1]
        #for multi objective optimisation, A dominates B if
        #1) A is no worse in all objectives
        #2) A is strictly better in at least one objective
        isDominate = False
        
        for pop, pop_fitness in population:
            fpop_value, popneg_cost = pop_fitness
            if(fpop_value >= f_value and popneg_cost >= neg_cost) and (fpop_value > f_value or popneg_cost > neg_cost): 
                isDominate = True
                break
        if(not isDominate):
            new_population = []
            #iterate population vector and for all fitness values that are less
            for pop in population:
                z, g_z = pop
                zpop_value, zpopneg_cost = g_z
                if not (f_value >= zpop_value and neg_cost >= zpopneg_cost and (f_value > zpop_value or neg_cost > zpopneg_cost)):
                    new_population.append(pop)
            new_population.append((child, child_fitness))   
            population = new_population

    return population
                    
# --- Run GSEMO on all problem instances ---    
all_problem_ids = [2202,2203]
n_runs = 30
budget = 100000
root_data_folder = "C:/Users/USER/Desktop/Evocomp/EvoComp1/data"

for problem_id in all_problem_ids:
    print(f"Running GSEMO on problem {problem_id}...")

    # Create folder for this problem
    problem_folder = os.path.join(root_data_folder, f"Exercise4/Problem_{problem_id}")
    os.makedirs(problem_folder, exist_ok=True)

    # Create a single analyzer for all runs
    l = logger.Analyzer(
        root=root_data_folder,
        folder_name=f"Exercise4/Problem_{problem_id}",
        algorithm_name="GSEMO",
        algorithm_info="GSEMO multiobjective",
    )

    # Create the problem once
    problem = ioh.get_problem(problem_id, problem_class=ioh.ProblemClass.GRAPH)
    problem.attach_logger(l)

    all_tradeoffs = []

    for run in range(n_runs):
        # Run GSEMO
        population = GSEMO(problem, budget=budget)
        tradeoff = [(fit[0], fit[1], run + 1) for _, fit in population]
        all_tradeoffs.extend(tradeoff)

        # Reset the problem for the next run
        problem.reset()

    # Save CSV
    df = pd.DataFrame(all_tradeoffs, columns=["submodular_value", "neg_cost", "run"])
    tradeoff_file = os.path.join(problem_folder, f"GSEMO_{problem_id}_all_runs_tradeoff.csv")
    df.to_csv(tradeoff_file, index=False)

    # Detach logger and clean up
    problem.detach_logger()
    del l
