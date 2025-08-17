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

if __name__ == "__main__":
    test_operators()

        
    #@staticmethod

    #def OrderCrossover(tour1: List[int], tour2: List[int]) -> List[int]


    

