import random
from typing import List

class Operators:
    @staticmethod
    def PMX(tour1: List[int], tour2: List[int]) -> List[int]:
        childTour = tour1.copy()
        crossOver = {}

        size = len(tour1)
        pos1, pos2 = random.sample(range(size), 2)
        pos1, pos2 = min(pos1, pos2), max(pos1, pos2)

        # Build mapping
        for i in range(pos1, pos2+1):
            crossOver[tour1[i]] = tour2[i]

        # Fill remaining positions
        for i in range(size):
            node = tour2[i]
            if pos1 <= i <= pos2:
                continue
            while node in crossOver:
                node = crossOver[node]
            childTour[i] = node

        print(f"Segment indices: {pos1}-{pos2}, Segment from Parent1: {tour1[pos1:pos2+1]}")
        print(f"ChildTour: {childTour}\n")
        return childTour


import random
from operators import Operators

def test_pmx():
    # Fix the seed for reproducibility
    random.seed(42)

    parent1 = [1, 2, 3, 4, 5, 6, 7, 8]
    parent2 = [5, 6, 7, 8, 1, 2, 3, 4]

    print("Parent1:", parent1)
    print("Parent2:", parent2)
    print("\nTesting PMX crossover multiple times:\n")

    for _ in range(3):
        child = Operators.PMX(parent1, parent2)
        print("ChildTour:", child)
        print("-" * 40)

if __name__ == "__main__":
    test_pmx()
