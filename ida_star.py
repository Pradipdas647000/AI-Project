from puzzle import Puzzle
from pattern_db import pattern_database_heuristic

def ida_star(start):
    threshold = pattern_database_heuristic(start)

    def search(path, g, threshold):
        node = path[-1]
        f = g + pattern_database_heuristic(node)
        if f > threshold:
            return f
        if node.is_goal():
            return "FOUND"
        min_cost = float('inf')
        for _, pos in node.get_possible_moves():
            new_state = node.move(pos)
            if new_state in path:
                continue
            path.append(new_state)
            temp = search(path, g + 1, threshold)
            if temp == "FOUND":
                return "FOUND"
            if temp < min_cost:
                min_cost = temp
            path.pop()
        return min_cost

    path = [start]
    while True:
        temp = search(path, 0, threshold)
        if temp == "FOUND":
            return path
        if temp == float('inf'):
            return None
        threshold = temp
