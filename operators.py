#exercise 4
from typing import List
import random

class Operators:
    #mutation operators : for one tour
    @staticmethod 
    def Insert(tour: List[int]) -> List[int]: 
        tour = tour.copy()
        size = len(tour)
        #gets a random start position and end position
        start = random.randint(0, size-1)
        end = start 
        while(end == start):
            end = random.randint(0, size-1)
        if(start < end): #if you need to move the node to the right
            for i in range(start, end):
                temp = tour[i]
                tour[i] = tour[i+1]
                tour[i+1] = temp
        else: #if you need to move the node to the left
            for i in range(start, end, -1):
                temp = tour[i]
                tour[i] = tour[i-1]
                tour[i-1] = temp
        return tour

    @staticmethod 
    def Swap(tour: List[int]) -> List[int]: 
        #gets a random start position and end position
        tour = tour.copy()
        size = len(tour)
        pos1 = random.randint(0, size-1)
        pos2 = pos1
        while(pos2 == pos1):
            pos2 = random.randint(0, size-1)
        #swaps the nodes
        temp = tour[pos1]
        tour[pos1] = tour[pos2]
        tour[pos2] = temp

        return tour 

    @staticmethod 
    def Inversion(tour: List[int]) -> List[int]: 
        tour = tour.copy()
        size = len(tour)
        pos1 = random.randint(0, size-1)
        pos2 = pos1
        while(pos2 == pos1):
            pos2 = random.randint(0, size-1)
        #makes sure that the the smaller position is pos1
        if(pos1 > pos2):
            temp = pos1
            pos1 = pos2
            pos2 = temp
        #reverse the segment between pos1 and pos2
        tour[pos1:pos2+1] = tour[pos1:pos2+1][::-1]
        
        return tour
    
    @staticmethod
    def OrderCrossover(tour1: List[int], tour2: List[int]) -> List[int]: 
        #set tour1 as the child tour
        childTour = tour1.copy() 
        #find the bounds of the random segment 
        size = len(tour1)
        pos1 = random.randint(0, size-1)
        pos2 = pos1
        while(pos2 == pos1):
            pos2 = random.randint(0, size-1)
        if(pos1 > pos2):
            temp = pos1
            pos1 = pos2
            pos2 = temp
        #set to contain the nodes within the random segment of tour1
        segment = set()
        for i in range(pos1, pos2+1):
            segment.add(tour1[i])
        ptr = 0
        t2ptr = 0
        while(ptr < size):
            if(ptr >= pos1 and ptr <= pos2): 
                ptr = pos2+1 #skip preserved segments
                continue
            if(tour2[t2ptr] in segment): 
                t2ptr +=1#skip duplicates
                continue
            #write over the genes in the child tour which wasnt in the random segment in order of tour2 nodes
            childTour[ptr] = tour2[t2ptr] 
            ptr += 1
            t2ptr +=1

        return childTour
            
    
    @staticmethod
    def PMX(tour1: List[int], tour2: List[int]) -> List[int]:
        childTour = tour1.copy()
        crossOver = {}
        size = len(tour1)
        #select random segment
        pos1 = random.randint(0, size-1)
        pos2 = pos1
        while(pos2 == pos1):
            pos2 = random.randint(0, size-1)
        if(pos1 > pos2):
            temp = pos1
            pos1 = pos2
            pos2 = temp
        #hashmap stores the mapping from parent1 segment to parent 2 segment
        for i in range(pos1, pos2+1):
            crossOver[tour1[i]] = tour2[i]
        
        #fill the non segment positions using parent2, applying mapping if needed
        for i in range(0, size):
            node = tour2[i]
            if(i >= pos1 and i <=pos2):
                continue #skip segment as it is already copied from parent1

            visited = set() #visited set to prevent infininte loop/mapping conflict
            while(node in crossOver):
                if node in visited:
                    break
                visited.add(node)
                node = crossOver[node] #set the node tothe mapping of the crossover

            childTour[i] = node
        return childTour

    #------------------------------ Mark Section --------------------------------------------------

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
    
    # -------------------------------------------------------------------------------------------------------
 
