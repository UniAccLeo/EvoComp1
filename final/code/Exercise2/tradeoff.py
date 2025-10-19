import pandas as pd
import matplotlib.pyplot as plt
import os

# List of problem IDs
problem_ids = [2100, 2101, 2102, 2103, 2200, 2201, 2202, 2203, 2300, 2301, 2302]

root_data_folder = "C:/Users/USER/Desktop/Evocomp/EvoComp1/data/Exercise2csv"

for problem_id in problem_ids:
    data_folder = os.path.join(root_data_folder, f"Problem_{problem_id}")
    csv_file = os.path.join(data_folder, f"GSEMO_{problem_id}_all_runs_tradeoff.csv")
    
    # Load CSV
    df = pd.read_csv(csv_file)
    
    # Filter first run
    df_run1 = df[df['run'] == 1]
    
    # Plot trade-off
    plt.figure(figsize=(6,5))
    plt.scatter(df_run1['neg_cost'], df_run1['submodular_value'], alpha=0.6)
    plt.xlabel("Negative Cost")
    plt.ylabel("Submodular Value")
    plt.title(f"Trade-off for Problem {problem_id} - Run 1")
    plt.grid(True)
    plt.show()
