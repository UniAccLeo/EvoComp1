from tsp import TSP
from q2 import run_all_local_search
def main():
    problem = "eil51" 

    try:
        tsp = TSP.create_from_file(f"data/{problem}.tsp")
    except Exception as e:
        print(f"Error reading TSP file: {e}")
        return

    print(f"Loaded problem: {tsp.name}")
    print(f"Dimension: {tsp.dimension}")
    print(f"First 5 coordinates: {tsp.nodes[:5]}")
    #print(f"First 5 matrix inputs: {[row[:5] for row in tsp.distance_matrix[:5]]}")
    print(f"First 5 nodes in solution: {tsp.load_solution()[:5]}")

    run_all_local_search()

if __name__ == "__main__":
    main()
