import pygame
import time

# Settings
TILE_SIZE = 100
GRID_SIZE = 4
WIDTH = HEIGHT = TILE_SIZE * GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_SIZE = 36

# Example: one board per step (from your trace)
boards = [
    [5, 1, 2, 3, 9, 6, 7, 4, 0, 10, 11, 8, 13, 14, 15, 12],
    [5, 1, 2, 3, 0, 6, 7, 4, 9, 10, 11, 8, 13, 14, 15, 12],
    [0, 1, 2, 3, 5, 6, 7, 4, 9, 10, 11, 8, 13, 14, 15, 12],
    [1, 0, 2, 3, 5, 6, 7, 4, 9, 10, 11, 8, 13, 14, 15, 12],
    [1, 2, 0, 3, 5, 6, 7, 4, 9, 10, 11, 8, 13, 14, 15, 12],
    [1, 2, 3, 0, 5, 6, 7, 4, 9, 10, 11, 8, 13, 14, 15, 12],
    [1, 2, 3, 4, 5, 6, 7, 0, 9, 10, 11, 8, 13, 14, 15, 12],
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0, 13, 14, 15, 12],
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0],
]

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

    for board in boards:
        draw_board(screen, board, font)
        time.sleep(0.7)  # pause to show move

    # Wait before exit
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()

if __name__ == "__main__":
    main()
