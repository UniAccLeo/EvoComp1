import ioh
import random 

f = ioh.get_problem(2100, problem_class=ioh.ProblemClass.GRAPH)

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
    num_variables = problem.n_variables
    x = [0]*num_variables
    for i in range(0, num_variables-1):
        choice = random.randint(0,1)
        x[i] = choice

    #determine g(x)
    g_x = fitness(x, problem)
    
    #define population
    population = [(x, g_x)]
    

    
        
    
