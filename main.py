from tsp import TSP

def main():
    path = "data/eil101.tsp" 

    try:
        tsp = TSP.create_from_file(path)
    except Exception as e:
        print(f"Error reading TSP file: {e}")
        return

    print(f"Loaded problem: {tsp.name}")
    print(f"Dimension: {tsp.dimension}")
    print(f"Edge weight type: {tsp.edgeWeightType}")
    print(f"First 5 coordinates: {tsp.nodes[:5]}")

if __name__ == "__main__":
    main()
