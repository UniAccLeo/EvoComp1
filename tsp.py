import math
from typing import List, Tuple, Dict, Optional
import io

class TSP :
    def __init__(
        self,
        name : str = None,
        comment : str = None,
        type : str = None,
        dimension : str = None,
        nodes : List[Tuple[int, int]] = None
    ) : 
        self.name = name
        self.comment = comment
        self.type = type
        self.dimension = dimension
        self.nodes = nodes

        matrix : List[List[float]] = [[0.0 for _ in range(int(dimension))] for _ in range(int(dimension))]
        for i, node in enumerate(nodes) :
            for i2, node2 in enumerate(nodes[:i]):
                distance = math.sqrt((node[0] - node2[0])**2 + (node[1] - node2[1])**2)
                matrix[i][i2] = distance
                matrix[i2][i] = distance
        self.distance_matrix = matrix

    @classmethod
    def create_from_file(cls, filename : str) :
        with open(filename, 'r', encoding='utf-8') as f:
            data = f.read()
        lines = [line.rstrip() for line in data.splitlines()]
        header: Dict[str, str] = {}
        nodes: List[Tuple[int,int]] = []
        is_coord_section = False
        for raw in lines:
            line = raw.strip()
            if not line :
                continue
            if not is_coord_section :
                if line.startswith("NODE_COORD_SECTION"):
                    is_coord_section = True
                    continue
                key, val = [part.strip() for part in line.split(':', 1)]
                header[key.upper()] = val
            else :
                if line.startswith("EOF"):
                    break
                line_coordinates = line.split()
                nodes.append((float(line_coordinates[1]), float(line_coordinates[2])))

        name = header.get("NAME")
        comment = header.get("COMMENT")
        type = header.get("TYPE")
        dimension = header.get("DIMENSION")
        
        tsp = TSP(
            name,
            comment,
            type,
            dimension,
            nodes
        )

        return tsp
    
    def load_solution(self):
        if(self.name == None) : return
        with open(f"data/{self.name}.opt.tour", 'r', encoding='utf-8') as f:
            data = f.read()
        lines = [line.rstrip() for line in data.splitlines()]
        is_tour_section = False
        solution = []
        for raw in lines:
            line = raw.strip()
            if not line :
                continue
            if not is_tour_section :
                if line.startswith("TOUR_SECTION"):
                    is_tour_section = True
                continue
            else :
                if line.startswith("EOF"):
                    break
                solution.append(int(line))
        return solution