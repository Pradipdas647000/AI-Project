import time
from puzzle import Puzzle
from ida_star import ida_star

def print_move_trace(path):
    print("\n🧩 Move Trace:")
    for i in range(1, len(path)):
        move = path[i-1].get_move(path[i])
        print(f"Step {i}: Move blank {move}")
        print(path[i])  # Pretty board printing (requires __str__ or __repr__)
        print("------")

def main():
    # Example scrambled puzzle
    initial_board = [5, 1, 2, 3,
                     9, 6, 7, 4,
                     13, 10, 11, 8,
                     0, 14, 15, 12]  # 0 is the blank

    puzzle = Puzzle(initial_board)

    start_time = time.time()
    path = ida_star(puzzle)
    end_time = time.time()

    print_move_trace(path)

    print("\n📊 Search Stats:")
    print(f"Nodes explored: {Puzzle.nodes_explored}")
    print(f"Solution steps: {len(path) - 1}")
    print(f"Total time taken: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    main()
