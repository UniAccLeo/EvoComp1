import argparse
import random
import math
from typing import List, Tuple
import os
import pandas as pd
import ioh
from ioh import logger

RNG = random.Random()

def is_feasible(f):
    # In MaxCoverage / MaxInfluence here, IOH returns negative values for infeasible
    return f >= 0

def evaluate(problem, x) -> float:
    # One call to the problem counts towards budget inside IOH.
    return problem(x)

def random_bitstring(n: int, p: float=0.5) -> List[int]:
    return [1 if RNG.random() < p else 0 for _ in range(n)]

def hamming(a: List[int], b: List[int]) -> int:
    return sum(1 for i in range(len(a)) if a[i] != b[i])

def bitflip_mutation(x: List[int]) -> List[int]:
    n = len(x)
    y = x[:]
    for i in range(n):
        if RNG.random() < 1.0 / n:
            y[i] = 1 - y[i]
    return y

def marginal_drop_repair(problem, x: List[int]) -> Tuple[List[int], float]:
    """If infeasible (problem(x) < 0), drop 1-bits with the smallest marginal contribution first.
       This is greedy and consumes extra evaluations; we cap work by a simple loop.
       Returns: (feasible_x, fitness)
    """
    f = evaluate(problem, x)
    if is_feasible(f):
        return x, f

    # Collect indices of active items
    ones = [i for i, bit in enumerate(x) if bit == 1]
    if not ones:
        return x, f

    # Compute marginal contributions (remove each 1 and measure drop)
    contributions = []
    base = f
    for idx in ones:
        x2 = x[:]
        x2[idx] = 0
        f2 = evaluate(problem, x2)
        contributions.append((idx, base - f2))  # drop means we lose value; smaller loss = worse item

    # Remove items with the smallest contributions first until feasible
    contributions.sort(key=lambda t: t[1])  # ascending (smallest contribution first)
    x_repaired = x[:]
    current_f = f
    for idx, _ in contributions:
        if is_feasible(current_f):
            break
        x_repaired[idx] = 0
        current_f = evaluate(problem, x_repaired)

    return x_repaired, current_f

def random_drop_repair(problem, x: List[int]) -> Tuple[List[int], float]:
    """Cheaper repair: randomly remove 1-bits until feasible. Fewer evaluations than marginal_drop."""
    f = evaluate(problem, x)
    if is_feasible(f):
        return x, f
    ones = [i for i, bit in enumerate(x) if bit == 1]
    RNG.shuffle(ones)
    xr = x[:]
    current_f = f
    for idx in ones:
        if is_feasible(current_f):
            break
        xr[idx] = 0
        current_f = evaluate(problem, xr)
    return xr, current_f

def deterministic_crowding(parent_a, parent_b, child_a, child_b, fit_a, fit_b, fit_ca, fit_cb):
    """Return survivors between two parents and two children using distance to most similar parent."""
    # Pair child to the closest parent (Hamming distance)
    d_ap = hamming(child_a, parent_a)
    d_bp = hamming(child_a, parent_b)
    if d_ap <= d_bp:
        # child_a competes with parent_a
        a_survivor = child_a if fit_ca >= fit_a else parent_a
        a_survivor_fit = max(fit_ca, fit_a)
        # child_b vs parent_b
        b_survivor = child_b if fit_cb >= fit_b else parent_b
        b_survivor_fit = max(fit_cb, fit_b)
    else:
        # child_a competes with parent_b
        b_survivor = child_a if fit_ca >= fit_b else parent_b
        b_survivor_fit = max(fit_ca, fit_b)
        # child_b vs parent_a
        a_survivor = child_b if fit_cb >= fit_a else parent_a
        a_survivor_fit = max(fit_cb, fit_a)
    return (a_survivor, a_survivor_fit), (b_survivor, b_survivor_fit)

def fitness_sharing_adjusted(fitnesses: List[float], genomes: List[List[int]], sigma=0.25):
    """Mild sharing: divide each fitness by niche count (based on normalized Hamming)."""
    n = len(genomes[0])
    shared = []
    for i in range(len(genomes)):
        niche = 0.0
        for j in range(len(genomes)):
            if i == j: 
                niche += 1.0
            else:
                d = hamming(genomes[i], genomes[j]) / n
                if d < sigma:
                    niche += 1.0 - (d / sigma)
        shared.append(fitnesses[i] / max(1e-9, niche))
    return shared

def run_single_objective(problem_id: int, runs: int, budget: int, pop_size: int, root: str,
                         repair: str = "random"):

    os.makedirs(root, exist_ok=True)
    algo_name = f"Ex3-SOEA(pop={pop_size},repair={repair})"

    # Create Analyzer folder per problem/pop/repair
    folder_name = f"Exercise3/SOEA_{repair}/Problem_{problem_id}/pop_{pop_size}"
    l = logger.Analyzer(root=root, folder_name=folder_name,
                        algorithm_name=algo_name, algorithm_info="Single-objective EA with repair + crowding")

    problem = ioh.get_problem(problem_id, problem_class=ioh.ProblemClass.GRAPH)
    problem.attach_logger(l)

    records = []

    for r in range(1, runs + 1):
        RNG.seed(12345 + 97 * r + problem_id * 13)
        nvars = problem.meta_data.n_variables

        # init population: random bitstrings, then repair if infeasible
        pop = []
        fit = []
        for _ in range(pop_size):
            x0 = random_bitstring(nvars, p=0.5)
            if repair == "marginal":
                xr, fr = marginal_drop_repair(problem, x0)
            else:
                xr, fr = random_drop_repair(problem, x0)
            pop.append(xr)
            fit.append(fr)

        best = max(fit)
        evals_start = problem.state.evaluations

        while (problem.state.evaluations - evals_start) < budget:
            # Parent selection: random pairing
            i, j = RNG.randrange(pop_size), RNG.randrange(pop_size)
            while j == i:
                j = RNG.randrange(pop_size)

            pa, pb = pop[i], pop[j]
            fa, fb = fit[i], fit[j]

            # Variation: bitflip mutation only (robust, cheap)
            ca = bitflip_mutation(pa)
            cb = bitflip_mutation(pb)

            # Repair if infeasible
            if repair == "marginal":
                ca, fca = marginal_drop_repair(problem, ca)
                cb, fcb = marginal_drop_repair(problem, cb)
            else:
                ca, fca = random_drop_repair(problem, ca)
                cb, fcb = random_drop_repair(problem, cb)

            # Deterministic crowding survival within pairs
            (sa, sfa), (sb, sfb) = deterministic_crowding(pa, pb, ca, cb, fa, fb, fca, fcb)

            pop[i], fit[i] = sa, sfa
            pop[j], fit[j] = sb, sfb

            # Mild fitness sharing pass every 20 steps (cheap heuristic)
            if (problem.state.evaluations - evals_start) % 20 == 0:
                adj = fitness_sharing_adjusted(fit, pop, sigma=0.3)
                # Replace worst individual if extremely crowded
                worst_idx = min(range(pop_size), key=lambda t: adj[t])
                # Try a random immigrant
                immigrant = random_bitstring(nvars, p=0.5)
                if repair == "marginal":
                    immigrant, fim = marginal_drop_repair(problem, immigrant)
                else:
                    immigrant, fim = random_drop_repair(problem, immigrant)
                # Keep if it's not worse than worst (adjusted)

                if fim >= fit[worst_idx]:
                    pop[worst_idx], fit[worst_idx] = immigrant, fim

            best = max(best, max(fit))
            records.append({"run": r, "evaluations": problem.state.evaluations, "best_so_far": best})

        # reset between runs
        problem.reset()

    # Save CSV
    out_dir = os.path.join(root, folder_name)
    os.makedirs(out_dir, exist_ok=True)
    pd.DataFrame(records).to_csv(os.path.join(out_dir, "single_objective_progress.csv"), index=False)

    problem.detach_logger(l)
    del l

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--problem_id", type=int, required=True)
    parser.add_argument("--runs", type=int, default=30)
    parser.add_argument("--budget", type=int, default=10000)
    parser.add_argument("--pop", type=int, default=20, choices=[10,20,50])
    parser.add_argument("--root", type=str, default="./data")
    parser.add_argument("--repair", type=str, default="random", choices=["random","marginal"])
    args = parser.parse_args()
    run_single_objective(args.problem_id, args.runs, args.budget, args.pop, args.root, args.repair)

if __name__ == "__main__":
    main()
