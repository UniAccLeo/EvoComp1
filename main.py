from tsp import TSP

def main():
    path = "data/eil101.tsp" 

    try:
        tsp = TSP.create_from_file(path)
        print(tsp.name)
        return
    except Exception as e:
        print(f"Error reading TSP file: {e}")
        return

    # print(f"Loaded problem: {tsp_instance.name}")
    # print(f"Dimension: {tsp_instance.dimension}")
    # print(f"Edge weight type: {tsp_instance.edge_weight_type}")
    # print(f"First 5 coordinates: {tsp_instance.coords[:5]}")
    # print(f"Distance from node 0 to node 1: {tsp_instance.distance(0, 1)}")

if __name__ == "__main__":
    main()
