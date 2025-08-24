from tsp import TSP
from inverover import inver_over
import os

def main():
    problems = ["eil51", "eil76", "eil101", "st70", "kroa100",
    "kroc100", "krod100", "lin105", "pcb442", "pr2392", "usa13509"]

    os.makedirs('results', exist_ok=True)
    path = os.path.join('results', 'inverover_test_2.txt')

    with open(path, 'w') as f:
        for problem in problems :
            results = []
            try:
                tsp = TSP.create_from_file(f"data/{problem}.tsp")
                print(f"\nSolving problem: {problem}") 

                for i in range (30):
                    print(f"  Run {i+1}/30...", end='\r')

                    best_route, _ = inver_over(tsp)
                    best_route_cost = tsp.calculate_route_cost(best_route)
                    results.append(best_route_cost)
            except Exception as e:
                print(f"Error reading TSP file: {e}")   
                return
            
            mean = sum(results) / len(results)
            stdev = (sum((x - mean) ** 2 for x in results) / len(results)) ** 0.5
            
            f.write(f"results for {tsp.name}:\n")
            f.write(f"mean: {mean}\n")
            f.write(f"stdev: {stdev}\n\n")
            f.flush()

    print("\nAll tests completed.")

if __name__ == "__main__":
    main()
