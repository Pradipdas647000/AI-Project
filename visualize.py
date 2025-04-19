import pygame
import time
from collections import deque

# Settings
TILE_SIZE = 100
GRID_SIZE = 4
WIDTH = HEIGHT = TILE_SIZE * GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_SIZE = 36
GOAL_STATE = tuple([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0])

# Directions: (delta, move name)
DIRECTIONS = {
    'up': -4,
    'down': 4,
    'left': -1,
    'right': 1
}

def is_valid_move(zero_index, direction):
    if direction == 'up': return zero_index >= 4
    if direction == 'down': return zero_index < 12
    if direction == 'left': return zero_index % 4 != 0
    if direction == 'right': return zero_index % 4 != 3
    return False

def bfs_solver(start):
    queue = deque()
    visited = set()
    parent = {}

    queue.append(tuple(start))
    visited.add(tuple(start))
    parent[tuple(start)] = None

    while queue:
        current = queue.popleft()
        if current == GOAL_STATE:
            break
        zero_index = current.index(0)
        for direction in DIRECTIONS:
            if is_valid_move(zero_index, direction):
                new_index = zero_index + DIRECTIONS[direction]
                new_board = list(current)
                new_board[zero_index], new_board[new_index] = new_board[new_index], new_board[zero_index]
                new_board_tuple = tuple(new_board)
                if new_board_tuple not in visited:
                    visited.add(new_board_tuple)
                    parent[new_board_tuple] = current
                    queue.append(new_board_tuple)

    # Reconstruct path
    path = []
    current = GOAL_STATE
    while current is not None:
        path.append(current)
        current = parent.get(current)
    path.reverse()
    return path

def draw_board(screen, board, font):
    screen.fill(WHITE)
    for i in range(4):
        for j in range(4):
            val = board[i * 4 + j]
            if val != 0:
                pygame.draw.rect(screen, BLACK, (j*TILE_SIZE, i*TILE_SIZE, TILE_SIZE, TILE_SIZE), 2)
                text = font.render(str(val), True, BLACK)
                text_rect = text.get_rect(center=(j*TILE_SIZE + TILE_SIZE//2, i*TILE_SIZE + TILE_SIZE//2))
                screen.blit(text, text_rect)
    pygame.display.flip()

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("15-Puzzle Solver Visualization")
    font = pygame.font.Font(None, FONT_SIZE)

    # Initial board (customize as needed)
    start_board = [5, 1, 2, 3, 9, 6, 7, 4, 0, 10, 11, 8, 13, 14, 15, 12]

    print("Solving puzzle...")
    path = bfs_solver(start_board)
    print(f"Solution found in {len(path)-1} steps!")

    for board in path:
        draw_board(screen, board, font)
        time.sleep(0.5)

    # Wait before exit
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()

if __name__ == "__main__":
    main()
