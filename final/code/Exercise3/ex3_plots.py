import os
import glob
import pandas as pd
import matplotlib.pyplot as plt

ROOT = "./data"
EX2_ROOT = "./data"

MAXCOVERAGE = [2100,2101,2102,2103]
MAXINFLUENCE = [2200,2201,2202,2203]

def plot_fixed_budget(problem_id):
    plt.figure(figsize=(7,5))

    # --- Exercise 3 (SOEA progress) ---
    so_patterns = [
        f"{ROOT}/Exercise3/SOEA_random/Problem_{problem_id}/pop_*/single_objective_progress.csv",
        f"{ROOT}/Exercise3/SOEA_marginal/Problem_{problem_id}/pop_*/single_objective_progress.csv",
    ]
    labels = ["SOEA (random-repair)", "SOEA (marginal-repair)"]
    for pat, lab in zip(so_patterns, labels):
        files = glob.glob(pat)
        if not files: 
            continue
        # combine runs
        df = pd.concat((pd.read_csv(f) for f in files), ignore_index=True)
        # mean +- std of best_so_far vs evaluations (sampled)
        gb = df.groupby("evaluations")["best_so_far"]
        mean = gb.mean()
        std = gb.std()
        plt.plot(mean.index, mean.values, label=lab)
        plt.fill_between(mean.index, mean.values-std.values, mean.values+std.values, alpha=0.15)

    plt.title(f"Fixed-Budget Progress – Problem {problem_id}")
    plt.xlabel("Evaluations")
    plt.ylabel("Best-so-far (single-objective)")
    plt.grid(True, alpha=0.3)
    plt.legend()
    out = f"{ROOT}/Exercise3/plots/fixed_budget_{problem_id}.png"
    os.makedirs(os.path.dirname(out), exist_ok=True)
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()

def plot_tradeoffs(problem_id):
    plt.figure(figsize=(6,5))

    # Exercise 2 GSEMO tradeoffs if saved (neg_cost vs value)
    gsemo_csv = f"{EX2_ROOT}/Exercise2/Problem_{problem_id}/GSEMO_{problem_id}_all_runs_tradeoff.csv"
    if os.path.exists(gsemo_csv):
        df = pd.read_csv(gsemo_csv)
        df1 = df[df["run"] == 1]
        plt.scatter(df1["neg_cost"], df1["submodular_value"], s=12, alpha=0.35, label="GSEMO (run 1)")

    # Exercise 3 MOEA tradeoffs (use run 1)
    moea_csv_glob = glob.glob(f"{ROOT}/Exercise3/MOEA/Problem_{problem_id}/pop_*/moea_tradeoffs.csv")
    if moea_csv_glob:
        dfm = pd.concat((pd.read_csv(f) for f in moea_csv_glob), ignore_index=True)
        dfm1 = dfm[dfm["run"] == 1]
        plt.scatter(dfm1["neg_cost"], dfm1["value"], s=16, alpha=0.6, label="MOEA (run 1)")

    plt.xlabel("Negative Cost")
    plt.ylabel("Submodular Value")
    plt.title(f"Trade-offs – Problem {problem_id} (Run 1)")
    plt.grid(True, alpha=0.3)
    plt.legend()
    out = f"{ROOT}/Exercise3/plots/tradeoffs_{problem_id}.png"
    os.makedirs(os.path.dirname(out), exist_ok=True)
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()

def main():
    for pid in MAXCOVERAGE + MAXINFLUENCE:
        plot_fixed_budget(pid)
        plot_tradeoffs(pid)
    print(f"Saved plots under {ROOT}/Exercise3/plots")

if __name__ == "__main__":
    main()
