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
    
    # -------------------------------------------------------------------------------------------------------
 
