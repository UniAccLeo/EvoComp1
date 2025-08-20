# q3.py
import random
import math
from typing import List

class Individual:
    def __init__(self, tour: List[int], tsp_problem):
        self.tour = tour[:]  # permutation
        self.tsp = tsp_problem
        self.length = self.evaluate()
        self.fitness = 1 / (1 + self.length)

    def _dist(self, i: int, j: int) -> int:
        """Distance between city i and j, trying multiple fallbacks."""
        # 1) If TSP has distance(), use it
        if hasattr(self.tsp, "distance") and callable(getattr(self.tsp, "distance")):
            return self.tsp.distance(i, j)

        # 2) If TSP has a distance_matrix, use it (support 0- or 1-based)
        if hasattr(self.tsp, "distance_matrix"):
            dm = self.tsp.distance_matrix
            n = len(dm)
            # Heuristic: if matrix is (n x n) for 0-based, indices valid directly;
            # if it's (n+1 x n+1) for 1-based, shift by +1
            if i < n and j < n:
                try:
                    return dm[i][j]
                except Exception:
                    pass
            if i + 1 < n and j + 1 < n:
                return dm[i + 1][j + 1]

        # 3) Compute EUC_2D directly from nodes (assumes tsp.nodes is list of (x,y))
        x1, y1 = self._xy(i)
        x2, y2 = self._xy(j)
        return int(round(math.hypot(x1 - x2, y1 - y2)))

    def _xy(self, idx: int):
        """Get (x,y) for city idx from tsp.nodes; supports string coords."""
        x, y = self.tsp.nodes[idx]
        return float(x), float(y)

    def evaluate(self) -> int:
        total = 0
        for k in range(len(self.tour)):
            a = self.tour[k]
            b = self.tour[(k + 1) % len(self.tour)]
            total += self._dist(a, b)
        return total

    @classmethod
    def random_individual(cls, tsp_problem):
        """
        Build a random permutation.
        Your TSP.nodes is a *list* in your code, so use 0-based labels [0..n-1].
        """
        n = len(tsp_problem.nodes)
        tour = list(range(n))  # 0-based indices
        random.shuffle(tour)
        return cls(tour, tsp_problem)

    def __repr__(self):
        return f"Individual(length={self.length}, fitness={self.fitness:.6f})"


class Population:
    def __init__(self, tsp_problem, size: int):
        self.tsp = tsp_problem
        self.individuals = [Individual.random_individual(tsp_problem) for _ in range(size)]

    def best(self) -> Individual:
        return min(self.individuals, key=lambda ind: ind.length)

    def average_length(self) -> float:
        return sum(ind.length for ind in self.individuals) / len(self.individuals)

    def __repr__(self):
        return f"Population(size={len(self.individuals)}, best_length={self.best().length})"
