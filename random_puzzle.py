import random
from puzzle import Puzzle

def generate_random_solvable_puzzle(difficulty=30):
    """
    Generate a solvable puzzle by making valid moves from the goal state.
    """
    # Start with the goal state
    board = list(range(1, 16)) + [0]  # Goal state (1-15 followed by blank)
    puzzle = Puzzle(board)

    visited = set()
    visited.add(tuple(puzzle.board))

    # Make random moves to scramble the puzzle
    for _ in range(difficulty):
        successors = puzzle.get_successors()
        random.shuffle(successors)
        for next_state in successors:
            if tuple(next_state.board) not in visited:
                puzzle = next_state
                visited.add(tuple(next_state.board))
                break
    # Return the scrambled board
    return puzzle.board

# Keep the old function name for backward compatibility
def generate_easy_solvable_board(moves=30):
    return generate_random_solvable_puzzle(difficulty=moves)
