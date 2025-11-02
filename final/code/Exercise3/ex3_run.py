import subprocess
import sys
import os

# Adjust ROOT to your workspace. Requires ex3_single.py and ex3_moea.py in PYTHONPATH or same folder.
ROOT = "./data"

MAXCOVERAGE = [2100,2101,2102,2103]
MAXINFLUENCE = [2200,2201,2202,2203]
ALL = MAXCOVERAGE + MAXINFLUENCE

POPS = [10,20,50]
RUNS = 30
BUDGET = 10000

def main():
    here = os.path.dirname(os.path.abspath(__file__))
    ex3_single = os.path.join(here, "ex3_single.py")
    ex3_moea = os.path.join(here, "ex3_moea.py")

    for pid in ALL:
        for pop in POPS:
            # Single-objective (marginal-repair)
            subprocess.run([sys.executable, ex3_single, "--problem_id", str(pid),
                            "--runs", str(RUNS), "--budget", str(BUDGET),
                            "--pop", str(pop), "--root", ROOT, "--repair", "marginal"], check=True)
            # MOEA
            subprocess.run([sys.executable, ex3_moea, "--problem_id", str(pid),
                            "--runs", str(RUNS), "--budget", str(BUDGET),
                            "--pop", str(pop), "--root", ROOT], check=True)

if __name__ == "__main__":
    main()
