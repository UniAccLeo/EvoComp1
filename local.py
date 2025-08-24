from tsp import TSP
import statistics
import random 

#Calculate total tour cost using the distance matrix 
def tour_cost(tour, dist_matrix):
    cost = 0
    for i in range(len(tour)):
        cost += dist_matrix[tour[i]][tour[(i+1) % len(tour)]]
    return cost


# Find neighbours and costs (w/ first improvement)

# Jump Neighbour
def jump_neighbour(tour, dist_matrix, current_cost):
    n = len(tour)
    for i in range(n):
        for j in range(n):
            if i == j:
                continue

            # Create new tour with node at i moved to position j
            new_tour = tour[:]
            node = new_tour.pop(i)
            new_tour.insert(j, node)

            #compute change in cost for the move
            delta = 0
            i_prev, i_next = tour[i-1], tour[(i+1) % n]
            delta -= dist_matrix[i_prev][tour[i]] + dist_matrix[tour[i]][i_next]
            delta += dist_matrix[i_prev][i_next]

            j_prev, j_next = new_tour[j-1], new_tour[(j+1) % n]
            delta -= dist_matrix[j_prev][j_next]
            delta += dist_matrix[j_prev][node] + dist_matrix[node][j_next]

            # Return on first improvement 
            if delta < 0:
                return new_tour, current_cost + delta
    return None, current_cost # No improvement 


# Exchange Neighbour 
def exchange_neighbour(tour, dist_matrix, current_cost):
    n = len(tour)
    for i in range(n):
        for j in range(i+1, n):
            new_tour = tour[:]
            #Swap two cities
            new_tour[i], new_tour[j] = new_tour[j], new_tour[i]

            #Calcualte change in cost
            delta = 0
            for idx in [i, j]:
                prev, nxt = new_tour[idx-1], new_tour[(idx+1) % n]
                node = new_tour[idx]
                delta += (dist_matrix[prev][node] + dist_matrix[node][nxt]) - \
                         (dist_matrix[prev][tour[idx]] + dist_matrix[tour[idx]][nxt])
            
            # Return on first improvement 
            if delta < 0:
                return new_tour, current_cost + delta
    return None, current_cost # No improvement 


# 2-opt Neighbour
def two_op_neighbour(tour, dist_matrix, current_cost):
    n = len(tour)
    for i in range(n - 1):
        for j in range(i+2, n):
            if j - i == 1:
                continue

            # Reverse segment between node i+1 and j
            new_tour = tour[:i+1] + tour[i+1:j+1][::-1] + tour[j+1:]

            #Calculate change in cost for reversing edges 
            delta = 0
            delta -= dist_matrix[tour[i]][tour[i+1]] + dist_matrix[tour[j]][tour[(j+1) % n]]
            delta += dist_matrix[tour[i]][tour[j]] + dist_matrix[tour[i+1]][tour[(j+1) % n]]

            # Return on first improvement 
            if delta < 0:
                return new_tour, current_cost + delta
    return None, current_cost # No improvement found 


# Local Search
def local_search(initial_tour, dist_matrix, neighbour_func, max_iters=5000):
    best = initial_tour
    best_cost = tour_cost(initial_tour, dist_matrix)

    terminate = False
    iterations = 0

    # Terminate search if no improvement found or max iterations reached
    while not terminate and iterations < max_iters:
        terminate = True
        iterations += 1

        # Find improving neighbour 
        new_tour, new_cost = neighbour_func(best, dist_matrix, best_cost)
        #Update current point 
        if new_tour is not None and new_cost < best_cost:
            best, best_cost = new_tour, new_cost
            terminate = False 

    return best, best_cost

# Run multiple local searches 
def run_local_search(tsp, neighbour_func, runs=30, seed=None):
    if seed is not None:
        random.seed(seed)
    results = []
    for _ in range(runs):
        # Generate a random initial tour 
        init_tour = list(range(int(tsp.dimension)))
        random.shuffle(init_tour)

        # Run local search on the initial tour 
        _, cost = local_search(init_tour, tsp.distance_matrix, neighbour_func)
        results.append(cost)
        print(f"Best cost: {cost}")

    #Return best and mean cost across all runs
    return min(results), statistics.mean(results)

def run_all_local_search(output_file="results/local_search.txt"):
    # List of instances (tours) to test
    instances = [
    "eil51",
    "eil76",
    "eil101",
    "st70",
    "kroa100",
    "kroc100",
    "krod100",
    "lin105",
    "pcb442",
    "pr2392",
    "usa13509"
    ]
     
    # Map algorithm names to neighbour functions 
    algorithms = {
        "jump": jump_neighbour,
        "exchange": exchange_neighbour,
        "2-opt": two_op_neighbour
    }

    with open(output_file, "w") as f:
        for instance in instances:
            #Load TSP instance 
            try:
                tsp = TSP.create_from_file(f"data/{instance}.tsp")
            except Exception as e:
                print(f"Error loading {instance}: {e}")
                continue

            f.write(f"Instance: {instance}\n")

            # Run each algorithm and write min and mean costs 
            for name, func in algorithms.items():
                min_cost, mean_cost = run_local_search(tsp, func, runs=30)
                f.write(f"  {name}: min={min_cost:.2f}, mean={mean_cost:.2f}\n")
            f.write("\n")