#exercise 4
from typing import List
import random

class Operators:
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

        #loop over and add to hashmap
        for i in range(pos1, pos2+1):
            crossOver[tour1[i]] = tour2[i]
            crossOver[tour2[i]] = tour1[i]

        for i in range(0, size):
            node = tour2[i]
            if(i >= pos1 and i <=pos2):
                continue
            while(node in crossOver):
                node = crossOver[node]

            childTour[i] = node

        print(f"Parent1: {tour1}")
        print(f"Parent2: {tour2}")
        print(f"Segment indices: {pos1}-{pos2}, Segment: {tour1[pos1:pos2+1]}")
        print(f"Child: {childTour}\n")
        return childTour
        

    # @staticmethod
    # def EdgeRecombination(tour1: List[int], tour2: List[int]) -> List[int]:
    #     #create a hashmap: key: city, ans: combined neighbors of both parent

 
def test_order_crossover():
    parent1 = [0, 1, 2, 3, 4, 5]
    parent2 = [5, 4, 3, 2, 1, 0]

    # Test 1: segment in middle
    Operators.OrderCrossover(parent1, parent2)


def test_pmx():
    parent1 = [1, 2, 3, 4, 5, 6, 7, 8]
    parent2 = [5, 6, 7, 8, 1, 2, 3, 4]

    # Case 1: crossover segment [2, 5] (positions 2–5 inclusive)
    Operators.PMX(parent1, parent2)

#testing
def test_operators():
    original_tour = [0, 1, 2, 3, 4, 5]
    print("Original tour:", original_tour)

    print("\nTesting Insert:")
    for _ in range(5):
        new_tour = Operators.Insert(original_tour)
        print(new_tour)

    print("\nTesting Swap:")
    for _ in range(5):
        new_tour = Operators.Swap(original_tour)
        print(new_tour)

    print("\nInversion Swap:")
    for _ in range(5):
        new_tour = Operators.Inversion(original_tour)
        print(new_tour)
if __name__ == "__main__":
    # test_operators()
      # Example parents


    

