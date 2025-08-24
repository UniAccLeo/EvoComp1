#exercise 4
from typing import List
import random

class Operators2:
    #mutation operators : for one tour
    @staticmethod 
    def Insert(tour: List[int]) -> List[int]: 
        tour = tour.copy()
        size = len(tour)
        #gets the start position and end position
        start = random.randint(0, size-1)
        end = start 
        while(end == start):
            end = random.randint(0, size-1)

        if(start < end):
            for i in range(start, end):
                temp = tour[i]
                tour[i] = tour[i+1]
                tour[i+1] = temp
        else:
            for i in range(start, end, -1):
                temp = tour[i]
                tour[i] = tour[i-1]
                tour[i-1] = temp
        print(f"Insert: moved element from index {start} to {end} -> {tour}")
        return tour
                
    #algorihtm design for insert (kinda like bubbles sort)
    #insert pos 5 in pos 2  
    #0,1,2,3,4,5 
    #0,1,2,3,5,4
    #0,1,2,5,3,4
    #0,1,5,2,3,4            
    #insert pos 2 in pos 5 
    #0,1,2,3,4,5 
    #0,1,3,2,4,5
    #0,1,3,4,2,5
    #0,1,3,4,5,2

    @staticmethod 
    def Swap(tour: List[int]) -> List[int]: 
        tour = tour.copy()

        size = len(tour)
        pos1 = random.randint(0, size-1)
        pos2 = pos1
        while(pos2 == pos1):
            pos2 = random.randint(0, size-1)
        
        temp = tour[pos1]
        tour[pos1] = tour[pos2]
        tour[pos2] = temp
        print(f"Swap: swapped indices {pos1} and {pos2} -> {tour}")
        return tour 


    @staticmethod 
    def Inversion(tour: List[int]) -> List[int]: 
        tour = tour.copy()

        size = len(tour)
        pos1 = random.randint(0, size-1)
        pos2 = pos1
        while(pos2 == pos1):
            pos2 = random.randint(0, size-1)

        if(pos1 > pos2):
            temp = pos1
            pos1 = pos2
            pos2 = temp

        tour[pos1:pos2+1] = tour[pos1:pos2+1][::-1]
        print(f"Inversion: reversed indices {pos1} to {pos2} -> {tour}")
        return tour
    
            
    @staticmethod
    def OrderCrossover(tour1: List[int], tour2: List[int]) -> List[int]: #run this two times for two children as you can cross over in both ways
        #create the random segment 
        childTour = tour1.copy()
        size = len(tour1)
        pos1 = random.randint(0, size-1)
        pos2 = pos1
        while(pos2 == pos1):
            pos2 = random.randint(0, size-1)

        if(pos1 > pos2):
            temp = pos1
            pos1 = pos2
            pos2 = temp
        #set to contain the segment
        segment = set()
        for i in range(pos1, pos2+1):
            segment.add(tour1[i])
        
        ptr = 0
        t2ptr = 0
        while(ptr < size):
            if(ptr >= pos1 and ptr <= pos2):
                ptr = pos2+1
                continue
            if(tour2[t2ptr] in segment):
                t2ptr = t2ptr + 1
                continue
            
            childTour[ptr] = tour2[t2ptr]
            ptr = ptr +1
            t2ptr = t2ptr + 1

        print(f"Parent1: {tour1}")
        print(f"Parent2: {tour2}")
        print(f"Segment indices: {pos1}-{pos2}, Segment: {tour1[pos1:pos2+1]}")
        print(f"Child: {childTour}\n")
        return childTour
            
    
    @staticmethod
    def PMX(tour1: List[int], tour2: List[int]) -> List[int]:
        #create the random segment 
        childTour = tour1.copy()
        crossOver = {}

        size = len(tour1)
        pos1 = random.randint(0, size-1)
        pos2 = pos1
        while(pos2 == pos1):
            pos2 = random.randint(0, size-1)

        if(pos1 > pos2):
            temp = pos1
            pos1 = pos2
            pos2 = temp
        
        print(pos1)
        print(pos2)
        #loop over and add to hashmap
        for i in range(pos1, pos2+1):
            crossOver[tour1[i]] = tour2[i]
        
        for i in range(0, size):
            node = tour2[i]
            if(i >= pos1 and i <=pos2):
                continue

            visited = set()
            while(node in crossOver):
                if node in visited:
                    break
                visited.add(node)
                node = crossOver[node]

            childTour[i] = node

        print(f"Parent1: {tour1}")
        print(f"Parent2: {tour2}")
        print(f"Segment indices: {pos1}-{pos2}, Segment from Parent1: {tour1[pos1:pos2+1]}")
        print(f"ChildTour: {childTour}\n")
        return childTour
        

       #3: 7
       #4: 8
       #5: 1 

    @staticmethod
    def CycleCrossover(tour1: List[int], tour2: List[int]) -> List[int]:
        """
        Cycle Crossover (CX).
        Returns a single child by alternating cycles between parents.
        """
        size = len(tour1)
        child = [-1] * size
        visited = [False] * size
        cycle = 0

        while not all(visited):
            # find first index not visited yet
            start = next(i for i, v in enumerate(visited) if not v)
            idx = start
            # follow cycle
            while not visited[idx]:
                visited[idx] = True
                if cycle % 2 == 0:
                    child[idx] = tour1[idx]
                else:
                    child[idx] = tour2[idx]
                # move to position in P1 where p2[idx] occurs
                idx = tour1.index(tour2[idx])
            cycle += 1

        return child

    @staticmethod
    def EdgeRecombination(tour1: List[int], tour2: List[int]) -> List[int]:
        #create a hashmap: key: city, ans: combined neighbors of both parent
        t1 = tour1.copy()
        t2 = tour2.copy()
        size = len(t1)
        # build adjacency sets: for each city, add both neighbors from both parents
        adj = {city: set() for city in t1}
        for p in (t1, t2):
            for i in range(len(p)):
                city = p[i]
                left = p[(i - 1) % size]
                right = p[(i + 1) % size]
                adj[city].add(left)
                adj[city].add(right)

        child: List[int] = []
        unused = set(t1)

        # start from a random city taken from parent1 (consistent with many ERX variants)
        current = random.choice(t1)
        print(current)

        while len(child) < size:
            child.append(current)
            unused.discard(current)

            # remove 'current' from all adjacency sets (so counts reflect remaining choices)
            for s in adj.values():
                s.discard(current)

            # find neighbors of current that are still unused
            neighbors = [v for v in adj[current] if v in unused]
            if neighbors:
                # choose neighbor with smallest adjacency set (min remaining edges)
                min_size = min(len(adj[n]) for n in neighbors)
                candidates = [n for n in neighbors if len(adj[n]) == min_size]
                next_city = random.choice(candidates)
            else:
                # no usable neighbor => pick random unused city
                if unused:
                    next_city = random.choice(list(unused))
                else:
                    break  # finished
            current = next_city

        # safety: if anything left, append them
        if len(child) < size:
            for v in list(unused):
                child.append(v)

        return child
    
def test_order_crossover():
    parent1 = [0, 1, 2, 3, 4, 5]
    parent2 = [5, 4, 3, 2, 1, 0]
    # Test 1: segment in middle
    Operators2.OrderCrossover(parent1, parent2)

def test_edge_recombination():
    cases = [
        # (parent1, parent2)
        ([0,1,2,3,4,5,6,7], [3,7,5,1,6,0,2,4]), # mixed order
        ([1,2,3,4,5,6,7,8], [5,6,7,8,1,2,3,4]), # rotation
        ([0,1,2,3,4,5], [5,4,3,2,1,0]), # reverse
        ([0,1,2,3], [0,1,2,3]), # identical parents
    ]

    for i in range(1, len(cases) + 1):
        p1, p2 = cases[i - 1]
        child = Operators2.EdgeRecombination(p1, p2)
        print(f"Case {i}:")
        print(" Parent1:", p1)
        print(" Parent2:", p2)
        print(" Child:", child)

def test_cycle_crossover():
    parent1 = [1, 2, 3, 4, 5, 6, 7, 8]
    parent2 = [5, 6, 7, 8, 1, 2, 3, 4]

    child = Operators2.CycleCrossover(parent1, parent2)

    print("Parent1:", parent1)
    print("Parent2:", parent2)
    print("Child:", child)

def test_pmx():
    parent1 = [1, 2, 3, 4, 5, 6, 7, 8]
    parent2 = [5, 6, 7, 8, 1, 2, 3, 4]
    # Case 1: crossover segment [2, 5] (positions 2–5 inclusive)
    Operators2.PMX(parent1, parent2)

#testing
def test_operators():
    original_tour = [0, 1, 2, 3, 4, 5]
    print("Original tour:", original_tour)

    print("\nTesting Insert:")
    for _ in range(5):
        new_tour = Operators2.Insert(original_tour)
        print(new_tour)

    print("\nTesting Swap:")
    for _ in range(5):
        new_tour = Operators2.Swap(original_tour)
        print(new_tour)

    print("\nInversion Swap:")
    for _ in range(5):
        new_tour = Operators2.Inversion(original_tour)
        print(new_tour)

if __name__ == "__main__":
    # test_operators()
    # Example parents
    # test_pmx()
    # test_edge_recombination()
    test_cycle_crossover()
