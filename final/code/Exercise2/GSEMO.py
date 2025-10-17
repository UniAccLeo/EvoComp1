import ioh

f = ioh.get_problem(2100, problem_class=ioh.ProblemClass.GRAPH)

def fitness_function(x, problem):
    """
    Multi-objective fitness:
    - objective 1: submodular value from IOHprofiler
    - objective 2: cost (negative, since we want to minimize)
    """
    objValue = problem(x)
    cost = sum(x) #since each node has cost 1, you can just add all of it
    return (objValue, -cost)


