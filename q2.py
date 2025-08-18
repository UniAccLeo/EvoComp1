from tsp import TSP
import statistics
import random


# --- Utility: compute full tour cost (only needed for initial cost) ---
def tour_cost(tour, dist_matrix):
    cost = 0
    for i in range(len(tour)):
        cost += dist_matrix[tour[i]][tour[(i + 1) % len(tour)]]
    return cost


# --- Delta-cost functions (O(1) updates) ---
def jump_delta_cost(tour, dist_matrix, i, j):
    n = len(tour)
    if i == j:
        return 0

    node = tour[i]
    prev_i = tour[i - 1] if i > 0 else tour[-1]
    next_i = tour[(i + 1) % n]

    # remove node i
    cost_before = dist_matrix[prev_i][node] + dist_matrix[node][next_i]
    cost_after = dist_matrix[prev_i][next_i]

    # insertion cost
    if j < i:
        prev_j = tour[j - 1] if j > 0 else tour[-1]
        next_j = tour[j]
    else:
        prev_j = tour[j]
        next_j = tour[(j + 1) % n]

    cost_before += dist_matrix[prev_j][next_j]
    cost_after += dist_matrix[prev_j][node] + dist_matrix[node][next_j]

    return cost_after - cost_before


def exchange_delta_cost(tour, dist_matrix, i, j):
    n = len(tour)
    if i == j:
        return 0

    a, b = tour[i], tour[j]
    a_prev, a_next = tour[i - 1 if i > 0 else n - 1], tour[(i + 1) % n]
    b_prev, b_next = tour[j - 1 if j > 0 else n - 1], tour[(j + 1) % n]

    cost_before = dist_matrix[a_prev][a] + dist_matrix[a][a_next] \
                + dist_matrix[b_prev][b] + dist_matrix[b][b_next]

    if j == i + 1:  # adjacent swap
        cost_after = dist_matrix[a_prev][b] + dist_matrix[b][a] + dist_matrix[a][b_next]
    else:
        cost_after = dist_matrix[a_prev][b] + dist_matrix[b][a_next] \
                   + dist_matrix[b_prev][a] + dist_matrix[a][b_next]

    return cost_after - cost_before


def two_opt_delta_cost(tour, dist_matrix, i, j):
    n = len(tour)
    a, b = tour[i], tour[i + 1]
    c, d = tour[j], tour[(j + 1) % n]
    cost_before = dist_matrix[a][b] + dist_matrix[c][d]
    cost_after = dist_matrix[a][c] + dist_matrix[b][d]
    return cost_after - cost_before


# --- Local search with efficient updates ---
def local_search(initial_tour, dist_matrix, move_type="2-opt"):
    best = initial_tour[:]
    best_cost = tour_cost(best, dist_matrix)

    improved = True
    while improved:
        improved = False
        n = len(best)

        if move_type == "jump":
            for i in range(n):
                for j in range(n):
                    if i == j:
                        continue
                    delta = jump_delta_cost(best, dist_matrix, i, j)
                    if delta < 0:
                        node = best.pop(i)
                        best.insert(j, node)
                        best_cost += delta
                        improved = True
                        break
                if improved:
                    break

        elif move_type == "exchange":
            for i in range(n):
                for j in range(i + 1, n):
                    delta = exchange_delta_cost(best, dist_matrix, i, j)
                    if delta < 0:
                        best[i], best[j] = best[j], best[i]
                        best_cost += delta
                        improved = True
                        break
                if improved:
                    break

        elif move_type == "2-opt":
            for i in range(n - 1):
                for j in range(i + 2, n - 1):
                    if j - i == 1:
                        continue
                    delta = two_opt_delta_cost(best, dist_matrix, i, j)
                    if delta < 0:
                        best[i + 1:j + 1] = reversed(best[i + 1:j + 1])
                        best_cost += delta
                        improved = True
                        break
                if improved:
                    break

    return best, best_cost


# --- Multiple runs for statistics ---
def run_local_search(tsp, move_type, runs=30, seed=None):
    if seed is not None:
        random.seed(seed)
    results = []
    for _ in range(runs):
        print("instance1")
        init_tour = list(range(int(tsp.dimension)))
        random.shuffle(init_tour)
        _, cost = local_search(init_tour, tsp.distance_matrix, move_type)
        results.append(cost)
    return min(results), statistics.mean(results)


# --- Experiment runner ---
def run_experiments(output_file="results/local_search.txt"):
    instances = ["eil51", "pcb442", "pr2392", "usa13509"]
    algorithms = ["jump", "exchange", "2-opt"]

    with open(output_file, "w") as f:
        for instance in instances:
            try:
                tsp = TSP.create_from_file(f"data/{instance}.tsp")
            except Exception as e:
                print(f"Error loading {instance}: {e}")
                continue

            f.write(f"Instance: {instance}\n")
            print(f"Running {instance}...")

            for name in algorithms:
                min_cost, mean_cost = run_local_search(tsp, name, runs=30)
                f.write(f"  {name}: min={min_cost:.2f}, mean={mean_cost:.2f}\n")
            f.write("\n")
