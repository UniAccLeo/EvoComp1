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

        return childTour

# Mark Section

    @staticmethod
    def CycleCrossover(tour1: List[int], tour2: List[int]) -> List[int]:
        size = len(tour1)
        childTour = [-1] * size
        alleleVisited = [False] * size
        cycle = 0

        while alleleVisited.count(True) < size:
            # start with the first unvisited allele
            start = None
            for i in range(len(alleleVisited)):
                if not alleleVisited[i]:
                    start = i
                    break

            current = start
            # cycle loop
            while not alleleVisited[current]:
                alleleVisited[current] = True
                if cycle % 2 == 0:
                    # if even cycle, take allele from Parent1
                    childTour[current] = tour1[current]
                else:
                    # if odd cycle, take allele from Parent2
                    childTour[current] = tour2[current]
                # move to position in Parent1 where Parent2[current] is found
                current = tour1.index(tour2[current])
            cycle += 1

        return childTour

    @staticmethod
    def EdgeRecombination(tour1: List[int], tour2: List[int]) -> List[int]:
        # create a dictionary that has key:city and ans:combined neighbours of both parents
        size = len(tour1)
        edgeTable = {city: set() for city in tour1}
        for i in (tour1, tour2):
            for j in range(len(i)):
                city = i[j]
                left = i[(j - 1) % size]
                right = i[(j + 1) % size]
                edgeTable[city].add(left)
                edgeTable[city].add(right)
        childTour: List[int] = []
        unused = set(tour1)

        # start from a city chosen at random
        current = random.choice(tour1)
        # print(current)

        while len(childTour) < size:
            childTour.append(current)
            unused.discard(current)

            # delete current city from the set
            for i in edgeTable.values():
                i.discard(current)

            # check if current city has any common edges
            commonEdge = []
            for i in edgeTable[current]:
                if i in unused:
                    commonEdge.append(i)

            # if common edges exist, choose one with smallest remaining edges
            if commonEdge:
                sizes = []
                for i in commonEdge:
                    sizes.append(len(edgeTable[i]))
                minSize = min(sizes)
                candidates = []
                for i in commonEdge:
                    if len(edgeTable[i]) == minSize:
                        candidates.append(i)
                nextCity = random.choice(candidates)
            else: # otherwise choose any city with smallest remaining edges
                if unused:
                    sizes = []
                    for i in commonEdge:
                        sizes.append(len(edgeTable[i]))
                    minSize = min(sizes)
                    candidates = []
                    for i in unused:
                        if len(edgeTable[i]) == minSize:
                            candidates.append(i)
                    # pick random city when tied shortest lists
                    nextCity = random.choice(candidates)
                else:
                    break
            current = nextCity

        return childTour
    
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

def test_order_crossover():
    parent1 = [0, 1, 2, 3, 4, 5]
    parent2 = [5, 4, 3, 2, 1, 0]
    child = Operators2.OrderCrossover(parent1, parent2)
    print("Parent1:", parent1)
    print("Parent2:", parent2)

def test_pmx():
    parent1 = [1, 2, 3, 4, 5, 6, 7, 8]
    parent2 = [5, 6, 7, 8, 1, 2, 3, 4]
    child = Operators2.PMX(parent1, parent2)
    print("Parent1:", parent1)
    print("Parent2:", parent2)
    print("Child:", child)

def test_cycle_crossover():
    parent1 = [1, 2, 3, 4, 5, 6, 7, 8]
    parent2 = [5, 6, 7, 8, 1, 2, 3, 4]
    child = Operators2.CycleCrossover(parent1, parent2)
    print("Parent1:", parent1)
    print("Parent2:", parent2)
    print("Child:", child)

def test_edge_recombination():
    parent1 = [0,1,2,3,4,5,6,7]
    parent2 = [3,7,5,1,6,0,2,4]
    child = Operators2.EdgeRecombination(parent1, parent2)
    print("Parent1:", parent1)
    print("Parent2:", parent2)
    print("Child:", child)

if __name__ == "__main__":
    # test_operators()
    # test_order_crossover()
    # test_pmx()
    test_cycle_crossover()
    test_edge_recombination()
