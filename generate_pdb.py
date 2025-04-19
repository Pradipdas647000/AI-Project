import pickle
from collections import deque

GOAL = tuple([1, 2, 3, 4, 5, 6, 7, 8] + [0]*8)
TILE_SET = set(range(1, 9))

def get_blank_neighbors(pos):
    neighbors = []
    row, col = divmod(pos, 4)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dr, dc in directions:
        r, c = row + dr, col + dc
        if 0 <= r < 4 and 0 <= c < 4:
            neighbors.append(r * 4 + c)
    return neighbors

def generate_pdb():
    pdb = {}
    visited = set()
    queue = deque([(GOAL, GOAL.index(0), 0)])

    while queue:
        state, blank, cost = queue.popleft()
        state_key = tuple(tile if tile in TILE_SET or tile == 0 else -1 for tile in state)
        if state_key in visited:
            continue
        visited.add(state_key)
        pdb[state_key] = cost

        for neighbor in get_blank_neighbors(blank):
            new_state = list(state)
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
            queue.append((tuple(new_state), neighbor, cost + 1))

    with open("pdb_1to8.pkl", "wb") as f:
        pickle.dump(pdb, f)
    print("✅ Pattern database generated and saved as pdb_1to8.pkl")

if __name__ == "__main__":
    generate_pdb()
