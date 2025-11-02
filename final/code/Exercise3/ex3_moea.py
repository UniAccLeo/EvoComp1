import argparse
import random
from typing import List, Tuple
import os
import pandas as pd
import ioh
from ioh import logger

RNG = random.Random()

def evaluate_pair(problem, x) -> Tuple[float, int]:
    """Return (value, cost) pair; cost = number of ones."""
    v = problem(x)
    c = sum(x)
    return v, c

def dominates(a, b):
    # Maximize value, minimize cost -> equivalently maximize (value, -cost)
    # a dominates b if no worse in both and strictly better in at least one
    av, ac = a
    bv, bc = b
    return (av >= bv and ac <= bc) and (av > bv or ac < bc)

def fast_non_dominated_sort(vals: List[Tuple[float,int]]):
    S = [set() for _ in vals]
    n_dom = [0]*len(vals)
    fronts = [[]]

    for p in range(len(vals)):
        for q in range(len(vals)):
            if p == q: 
                continue
            if dominates(vals[p], vals[q]):
                S[p].add(q)
            elif dominates(vals[q], vals[p]):
                n_dom[p] += 1
        if n_dom[p] == 0:
            fronts[0].append(p)

    i = 0
    while fronts[i]:
        next_front = []
        for p in fronts[i]:
            for q in S[p]:
                n_dom[q] -= 1
                if n_dom[q] == 0:
                    next_front.append(q)
        i += 1
        fronts.append(next_front)
    if not fronts[-1]:
        fronts.pop()
    return fronts

def crowding_distance(vals: List[Tuple[float,int]], idxs: List[int]):
    if not idxs: 
        return {}
    dist = {i: 0.0 for i in idxs}
    # objectives: value (maximize) and cost (minimize)
    for obj in [0, 1]:
        sorted_idx = sorted(idxs, key=lambda i: (vals[i][obj], i))
        dist[sorted_idx[0]] = dist[sorted_idx[-1]] = float("inf")
        obj_min = vals[sorted_idx[0]][obj]
        obj_max = vals[sorted_idx[-1]][obj]
        denom = max(1e-12, obj_max - obj_min)
        for k in range(1, len(sorted_idx)-1):
            prev_v = vals[sorted_idx[k-1]][obj]
            next_v = vals[sorted_idx[k+1]][obj]
            dist[sorted_idx[k]] += (next_v - prev_v) / denom
    return dist

def bitflip_mutation(x: List[int]) -> List[int]:
    n = len(x)
    y = x[:]
    for i in range(n):
        if RNG.random() < 1.0 / n:
            y[i] = 1 - y[i]
    return y

def tournament_select(pop, vals, k=2):
    best = None
    for _ in range(k):
        cand = RNG.randrange(len(pop))
        if best is None:
            best = cand
        else:
            # Compare by rank then crowding
            if pop[cand]["rank"] < pop[best]["rank"]:
                best = cand
            elif pop[cand]["rank"] == pop[best]["rank"] and pop[cand]["crowd"] > pop[best]["crowd"]:
                best = cand
    return best

def assign_rank_and_crowding(vals):
    fronts = fast_non_dominated_sort(vals)
    meta = [{"rank": None, "crowd": 0.0} for _ in vals]
    for r, F in enumerate(fronts):
        dist = crowding_distance(vals, F)
        for i in F:
            meta[i]["rank"] = r
            meta[i]["crowd"] = dist[i]
    return meta, fronts

def run_moea(problem_id: int, runs: int, budget: int, pop_size: int, root: str):
    os.makedirs(root, exist_ok=True)
    algo_name = f"Ex3-MOEA(pop={pop_size})"

    folder_name = f"Exercise3/MOEA/Problem_{problem_id}/pop_{pop_size}"
    l = logger.Analyzer(root=root, folder_name=folder_name,
                        algorithm_name=algo_name, algorithm_info="NSGA-II style MOEA")

    problem = ioh.get_problem(problem_id, problem_class=ioh.ProblemClass.GRAPH)
    problem.attach_logger(l)

    tradeoff_records = []

    for r in range(1, runs+1):
        RNG.seed(2025 + 71 * r + problem_id * 17)
        nvars = problem.meta_data.n_variables

        pop = [ [1 if RNG.random() < 0.5 else 0 for _ in range(nvars)] for _ in range(pop_size) ]
        vals = [ evaluate_pair(problem, x) for x in pop ]
        meta, _ = assign_rank_and_crowding(vals)

        # keep archive each iteration to save tradeoffs per run
        def archive_front(pop, vals, meta):
            # non-dominated front (rank 0)
            F0 = [i for i,m in enumerate(meta) if m["rank"] == 0]
            for i in F0:
                v,c = vals[i]
                tradeoff_records.append({"run": r, "value": v, "neg_cost": -c,
                                         "evaluations": problem.state.evaluations})

        evals_start = problem.state.evaluations
        archive_front(pop, vals, meta)

        while (problem.state.evaluations - evals_start) < budget:
            # variation: tournament select two parents, mutate both
            i1 = tournament_select([{"rank":m["rank"],"crowd":m["crowd"]} for m in meta], vals)
            i2 = tournament_select([{"rank":m["rank"],"crowd":m["crowd"]} for m in meta], vals)
            while i2 == i1:
                i2 = tournament_select([{"rank":m["rank"],"crowd":m["crowd"]} for m in meta], vals)

            c1 = bitflip_mutation(pop[i1])
            c2 = bitflip_mutation(pop[i2])

            pop.extend([c1, c2])
            vals.extend([evaluate_pair(problem, c1), evaluate_pair(problem, c2)])

            # environmental selection: recompute ranks & crowding, keep best pop_size
            meta, fronts = assign_rank_and_crowding(vals)

            new_idx = []
            for F in fronts:
                if len(new_idx) + len(F) <= pop_size:
                    new_idx.extend(F)
                else:
                    # fill remainder by crowding distance
                    dist = crowding_distance(vals, F)
                    sorted_F = sorted(F, key=lambda i: dist[i], reverse=True)
                    need = pop_size - len(new_idx)
                    new_idx.extend(sorted_F[:need])
                    break

            pop = [pop[i] for i in new_idx]
            vals = [vals[i] for i in new_idx]
            meta = [meta[i] for i in new_idx]

            archive_front(pop, vals, meta)

        problem.reset()

    # save tradeoffs
    out_dir = os.path.join(root, folder_name)
    os.makedirs(out_dir, exist_ok=True)
    pd.DataFrame(tradeoff_records).to_csv(os.path.join(out_dir, "moea_tradeoffs.csv"), index=False)

    problem.detach_logger(l)
    del l

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--problem_id", type=int, required=True)
    parser.add_argument("--runs", type=int, default=30)
    parser.add_argument("--budget", type=int, default=10000)
    parser.add_argument("--pop", type=int, default=20, choices=[10,20,50])
    parser.add_argument("--root", type=str, default="./data")
    args = parser.parse_args()
    run_moea(args.problem_id, args.runs, args.budget, args.pop, args.root)

if __name__ == "__main__":
    main()
