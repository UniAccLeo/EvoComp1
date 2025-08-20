from tsp import TSP
import random

def inver_over (tsp : TSP, population_size : int = 100, p : float = 0.02, iterations : int = 20000) :
    routes = []
    n_nodes = tsp.dimension
    for _ in range(population_size) :
        routes.append(create_route(n_nodes))

    best_route = []
    best_route_cost = float('inf')
    best_route_unchanged_times = 0

    for iteration in range(iterations) : 
        if best_route_unchanged_times == 10 : return best_route, iteration
        updated_best_route = False
        for idx ,route in enumerate(routes):
            new_route = route[:]
            node1 = random.choice(new_route)
            while True:
                position_map = {node: i for i, node in enumerate(new_route)}
                if random.random() <= p:
                    choices = [node for node in new_route if node != node1]
                    node2 = random.choice(choices)
                else:
                    other_route = random.choice(routes)
                    node2 = other_route[(other_route.index(node1)+1)%n_nodes]
                
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
            new_route_cost = tsp.calculate_route_cost(new_route)
            if new_route_cost < tsp.calculate_route_cost(route) :
                routes[idx] = new_route[:]
                updated_best_route = True
                best_route_unchanged_times = 1
                if new_route_cost< best_route_cost : 
                    best_route = new_route[:]
                    best_route_cost = new_route_cost
                    # best_route_unchanged_times = 1
                    # updated_best_route = True
        if not updated_best_route :
            best_route_unchanged_times += 1    
    return best_route, iterations

def create_route(n_nodes : int) :
    nodes = list(range(n_nodes))
    random.shuffle(nodes)
    return nodes

