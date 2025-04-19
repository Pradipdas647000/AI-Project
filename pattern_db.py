import pickle
import os

pdb_path = os.path.join(os.path.dirname(__file__), "pdb_1to8.pkl")

try:
    with open(pdb_path, "rb") as f:
        PDB = pickle.load(f)
    print(f"Pattern database loaded successfully from {pdb_path}")
except Exception as e:
    print(f"Error loading pattern database: {e}")
    # Provide an empty database as fallback
    PDB = {}

important_tiles = {0, 1, 2, 3, 4, 5, 6, 7, 8}

def pattern_database_heuristic(puzzle):
    # Flatten the board if it's nested
    flat_board = [tile for row in puzzle.board for tile in row] if isinstance(puzzle.board[0], list) else puzzle.board

    # Create the state key from important tiles only
    state_key = tuple(tile if tile in important_tiles else -1 for tile in flat_board)
    
    return PDB.get(state_key, 0)

# This function should be part of the Puzzle class, removed from here
