from tsp import TSP
import random

def inver_over (tsp : TSP, population_size : int = 50, p : float = 0.02, iterations : int = 20000) :
    routes = []
    n_nodes = tsp.dimension
    #create random permutations of paths
    for _ in range(population_size) :
        routes.append(create_route(n_nodes))
    

    best_route = []
    best_route_cost = float('inf')
    best_route_unchanged_times = 0

    #repeat for 20000 iterations
    for iteration in range(iterations) : 
        #if best route has unchanged for 10 times then early exit
        if best_route_unchanged_times == 10 : return best_route, iteration
        updated_best_route = False
        for idx ,route in enumerate(routes):
            new_route = route[:]
            #pick random node from route
            node1 = random.choice(new_route)
            while True:
                #generate position map to store initial positions of nodes
                position_map = {node: i for i, node in enumerate(new_route)}
                #use random value to determine whether to do random exploration or use existing path
                if random.random() <= p:
                    #choose random node;
                    choices = [node for node in new_route if node != node1]
                    node2 = random.choice(choices)
                else:
                    #choose adjacent node from another random route
                    other_route = random.choice(routes)
                    node2 = other_route[(other_route.index(node1)+1)%n_nodes]
                
                #check if the chosen node was already adjacent to the initial node, if so early exit
                node1_position = position_map[node1]
                node1_before = (node1_position - 1) % n_nodes
                node1_after = (node1_position + 1) % n_nodes
                node2_position = position_map[node2]
                if node2_position == node1_before or node2_position == node1_after :
                    break

                #invert
                inverted_route = new_route[:]
                if node2_position < node1_position :
                    lo = node2_position + 1
                    hi = node1_position
                else :
                    lo = node1_position + 1
                    hi = node2_position 
                while lo < hi :
                    inverted_route[lo], inverted_route[hi] = inverted_route[hi], inverted_route[lo]
                    lo += 1
                    hi -= 1
                new_route = inverted_route[:]
                node1 = node2

            #calculate the new route cost to see if it should replace the old route
            new_route_cost = tsp.calculate_route_cost(new_route)
            if new_route_cost < tsp.calculate_route_cost(route) :
                routes[idx] = new_route[:]
                # This block was used for inverover_any_route.txt, so that ANY improvement among the population would reset best_route_unchanged_times
                # updated_best_route = True
                # best_route_unchanged_times = 1
                if new_route_cost< best_route_cost : 
                    best_route = new_route[:]
                    best_route_cost = new_route_cost
                    #This block was used for inverover.txt, so only an improvement to the best 
                    #route would reset the count, following the original paper's logic
                    best_route_unchanged_times = 1
                    updated_best_route = True
        #increment best_route_unchanged_times if no improvement
        if not updated_best_route :
            best_route_unchanged_times += 1    
    return best_route, iterations

#helper function to initialise random routes;
def create_route(n_nodes : int) :
    nodes = list(range(n_nodes))
    random.shuffle(nodes)
    return nodes

