from tsp import TSP
import statistics
import random 

#Calculate total tour_cost
def tour_cost(tour, dist_matrix):
    cost = 0
    for i in range(len(tour)):
        cost += dist_matrix[tour[i]][tour[(i+1) % len(tour)]]
    return cost

#Find neighbours and costs

#Generate jump neighbours
def jump_neighbour(tour, dist_matrix, current_cost):
    n = len(tour)
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            new_tour = tour[:]
            node = new_tour.pop(i)
            new_tour.insert(j, node)

            # compute delta cost
            delta = 0
        
            i_prev, i_next = tour[i-1], tour[(i+1) % n]
            delta -= dist_matrix[i_prev][tour[i]] + dist_matrix[tour[i]][i_next]
            delta += dist_matrix[i_prev][i_next]

            j_prev, j_next = new_tour[j-1], new_tour[(j+1) % n]
            delta -= dist_matrix[j_prev][j_next]
            delta += dist_matrix[j_prev][node] + dist_matrix[node][j_next]

            yield new_tour, current_cost + delta   

#Generate exchange neighbours
def exchange_neighbour(tour, dist_matrix, current_cost):
    n = len(tour)
    for i in range(n):
        for j in range(i+1, n):
            new_tour = tour[:]
            new_tour[i], new_tour[j] = new_tour[j], new_tour[i]

            # compute delta cost
            delta = 0
            for idx in [i, j]:
                prev, nxt = new_tour[idx-1], new_tour[(idx+1) % n]
                node = new_tour[idx]
                delta += (dist_matrix[prev][node] + dist_matrix[node][nxt]) - \
                         (dist_matrix[prev][tour[idx]] + dist_matrix[tour[idx]][nxt])

            yield new_tour, current_cost + delta

#Generate two opt neighbours
def two_op_neighbour(tour, dist_matrix, current_cost):
    n = len(tour)
    for i in range(n - 1):
        for j in range(i+2, n):
            if j - i == 1:
                continue
            new_tour = tour[:i+1] + tour[i+1:j+1][::-1] + tour[j+1:]

            #Calculate delta cost
            delta = 0
            delta -= dist_matrix[tour[i]][tour[i+1]] + dist_matrix[tour[j]][tour[(j+1) % n]]
            delta += dist_matrix[tour[i]][tour[j]] + dist_matrix[tour[i+1]][tour[(j+1) % n]]

            yield new_tour, current_cost + delta

# Local Search
def local_search(initial_tour, dist_matrix, neighbour_func):
    best = initial_tour
    best_cost = tour_cost(initial_tour, dist_matrix)

    terminate = False
    #Keep on iterating until no improvements can be made
    while not terminate:
        terminate = True
        for n, cost in neighbour_func(best, dist_matrix, best_cost):
            if cost < best_cost:
                best = n
                best_cost = cost
                terminate = False
                break
    return best, best_cost

def run_local_search(tsp, neighbour_func, runs=30, seed=None):
    if seed is not None:
        random.seed(seed)
    results = []
    for _ in range(runs):
        init_tour = list(range(int(tsp.dimension)))
        random.shuffle(init_tour)
        _, cost = local_search(init_tour, tsp.distance_matrix, neighbour_func)
        results.append(cost)
    return min(results), statistics.mean(results)

def run_experiments(output_file="results/local_search.txt"):
    instances = [
        "eil51", "eil76", "eil101", "st70",
        "kroa100", "kroc100", "krod100",
        "lin105", "pcb442", "pr2392", "usa13509"
    ]
     
    algorithms = {
        "jump": jump_neighbour,
        "exchange": exchange_neighbour,
        "2-opt": two_op_neighbour
    }

    with open(output_file, "w") as f:
        for instance in instances:
            try:
                tsp = TSP.create_from_file(f"data/{instance}.tsp")
            except Exception as e:
                print(f"Error loading {instance}: {e}")
                continue

            f.write(f"Instance: {instance}\n")
            print(f"Running {instance}...")

            for name, func in algorithms.items():
                min_cost, mean_cost = run_local_search(tsp, func, runs=1)
                f.write(f"  {name}: min={min_cost:.2f}, mean={mean_cost:.2f}\n")
            f.write("\n")
