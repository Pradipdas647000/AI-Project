import pygame
import time
import math
from collections import deque

# Settings
TILE_SIZE = 100
GRID_SIZE = 4
WIDTH = HEIGHT = TILE_SIZE * GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 200, 0)
RECT_COLOR = (50, 50, 200)
EMPTY_TILE_COLOR = (240, 240, 240)
FONT_SIZE = 36
GOAL_STATE = tuple([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0])
ANIMATION_SPEED = 10  # Animation speed (higher is faster)

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

def draw_tile(screen, val, rect, font, is_correct_pos=False):
    """Draw a single tile with proper styling"""
    if val != 0:
        # Determine the color based on position correctness
        if is_correct_pos:
            color = GREEN
        else:
            color = RECT_COLOR
            
        # Create a nicer looking tile with gradient and shadow effect
        pygame.draw.rect(screen, (30, 30, 30), rect.inflate(4, 4))  # Shadow
        pygame.draw.rect(screen, color, rect)
        
        # Add a gradient effect
        gradient_rect = rect.inflate(-20, -20)
        pygame.draw.rect(screen, (min(color[0] + 40, 255), min(color[1] + 40, 255), min(color[2] + 40, 255)), 
                         gradient_rect)
        
        # Number text
        text = font.render(str(val), True, BLACK)
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)
    else:
        # Empty tile - improved null box with pattern
        pygame.draw.rect(screen, EMPTY_TILE_COLOR, rect)
        
        # Add a subtle pattern to the empty tile
        for i in range(0, rect.width, 10):
            pygame.draw.line(screen, (220, 220, 220), 
                            (rect.left + i, rect.top), 
                            (rect.left + i, rect.bottom), 1)
        for i in range(0, rect.height, 10):
            pygame.draw.line(screen, (220, 220, 220), 
                            (rect.left, rect.top + i), 
                            (rect.right, rect.top + i), 1)
        
        # Add text "Empty" in the center
        empty_text = font.render("", True, (150, 150, 150))
        empty_rect = empty_text.get_rect(center=rect.center)
        screen.blit(empty_text, empty_rect)

def draw_board(screen, board, font, animated_tiles=None):
    """Draw the game board with support for animated tiles"""
    screen.fill(WHITE)
    
    # Draw grid background
    for i in range(4):
        for j in range(4):
            grid_rect = pygame.Rect(j*TILE_SIZE, i*TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, (230, 230, 230), grid_rect)
            pygame.draw.rect(screen, (200, 200, 200), grid_rect, 1)
    
    # Draw regular tiles
    for i in range(4):
        for j in range(4):
            index = i * 4 + j
            val = board[index]
            
            # Skip drawing tiles that are being animated
            if animated_tiles and val in [t[0] for t in animated_tiles]:
                continue
                
            rect = pygame.Rect(j*TILE_SIZE, i*TILE_SIZE, TILE_SIZE, TILE_SIZE)
            
            # Check if tile is in correct position
            goal_pos = val - 1 if val > 0 else 15
            is_correct_pos = index == goal_pos
            
            draw_tile(screen, val, rect, font, is_correct_pos)
    
    # Draw animated tiles
    if animated_tiles:
        for val, pos_x, pos_y in animated_tiles:
            rect = pygame.Rect(pos_x, pos_y, TILE_SIZE, TILE_SIZE)
            
            # Check if animated tile is in correct position
            goal_pos = val - 1 if val > 0 else 15
            is_correct_pos = board.index(val) == goal_pos
            
            draw_tile(screen, val, rect, font, is_correct_pos)

def animate_move(screen, from_board, to_board, font):
    """Animate the transition between two board states"""
    # Find the tile that moved (the one that was swapped with the empty tile)
    moved_val = None
    from_zero_index = from_board.index(0)
    to_zero_index = to_board.index(0)
    
    # The moved tile is the value now at the position where zero was
    moved_val = to_board[from_zero_index]
    
    # Calculate starting and ending positions
    from_i, from_j = to_zero_index // 4, to_zero_index % 4
    to_i, to_j = from_zero_index // 4, from_zero_index % 4
    
    from_x, from_y = from_j * TILE_SIZE, from_i * TILE_SIZE
    to_x, to_y = to_j * TILE_SIZE, to_i * TILE_SIZE
    
    # Animation loop
    steps = 20  # Number of animation frames
    clock = pygame.time.Clock()
    
    for step in range(steps + 1):
        progress = step / steps
        
        # Easing function for smoother animation
        ease = math.sin(progress * math.pi / 2)
        
        # Current position
        current_x = from_x + (to_x - from_x) * ease
        current_y = from_y + (to_y - from_y) * ease
        
        # Draw board with animated tile
        draw_board(screen, to_board, font, [(moved_val, current_x, current_y)])
        
        # Add step indicator
        pygame.display.flip()
        clock.tick(60)
        
        # Check for quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
    
    return True

def visualize_solution(path):
    """
    Visualize a solution path using Pygame with animations and controls.
    Path should be a list of board states.
    """
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT + 50))  # Extra space for controls
    pygame.display.set_caption("15-Puzzle Solver Visualization")
    font = pygame.font.Font(None, FONT_SIZE)
    small_font = pygame.font.Font(None, 24)

    print("\n🎮 Starting visualization...")
    print(f"Solution has {len(path)-1} steps.")
    
    # Convert Puzzle objects to board lists if needed
    boards = []
    for puzzle in path:
        if hasattr(puzzle, 'board'):
            boards.append(puzzle.board)
        else:
            boards.append(puzzle)
    
    # Initialize state
    current_step = 0
    auto_play = False
    last_auto_time = time.time()
    
    # Main visualization loop
    running = True
    while running:
        current_time = time.time()
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and current_step < len(boards) - 1:
                    # Animate the transition to the next state
                    animate_move(screen, boards[current_step], boards[current_step + 1], font)
                    current_step += 1
                elif event.key == pygame.K_LEFT and current_step > 0:
                    # Animate the transition to the previous state
                    animate_move(screen, boards[current_step], boards[current_step - 1], font)
                    current_step -= 1
                elif event.key == pygame.K_SPACE:
                    # Toggle auto-play
                    auto_play = not auto_play
                    last_auto_time = current_time
                elif event.key == pygame.K_ESCAPE:
                    running = False
        
        # Auto-play functionality
        if auto_play and current_step < len(boards) - 1 and current_time - last_auto_time > 0.5:
            animate_move(screen, boards[current_step], boards[current_step + 1], font)
            current_step += 1
            last_auto_time = current_time
            
            # Stop auto-play at the end
            if current_step == len(boards) - 1:
                auto_play = False
        
        # Draw current board state
        screen.fill(WHITE)
        draw_board(screen, boards[current_step], font)
        
        # Draw controls bar
        controls_rect = pygame.Rect(0, HEIGHT, WIDTH, 50)
        pygame.draw.rect(screen, (240, 240, 240), controls_rect)
        pygame.draw.line(screen, (200, 200, 200), (0, HEIGHT), (WIDTH, HEIGHT), 2)
        
        # Display step number and controls
        step_text = font.render(f"Step: {current_step}/{len(boards)-1}", True, BLUE)
        screen.blit(step_text, (10, HEIGHT + 10))
        
        # Display controls info
        controls_text = small_font.render("← → : Navigate | Space : Auto-play | Esc : Exit", True, (100, 100, 100))
        controls_rect = controls_text.get_rect(right=WIDTH-10, centery=HEIGHT+25)
        screen.blit(controls_text, controls_rect)
        
        # Show auto-play indicator
        if auto_play:
            indicator = small_font.render("Auto-playing", True, GREEN)
            screen.blit(indicator, (WIDTH // 2 - 40, HEIGHT + 10))
        
        pygame.display.flip()
        
    pygame.quit()


def main():
    """
    Standalone test function for the visualizer.
    """
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT + 50))
    pygame.display.set_caption("15-Puzzle Solver Visualization")
    font = pygame.font.Font(None, FONT_SIZE)

    # Initial board (customize as needed)
    start_board = [5, 1, 2, 3, 9, 6, 7, 4, 0, 10, 11, 8, 13, 14, 15, 12]

    print("Solving puzzle...")
    path = bfs_solver(start_board)
    print(f"Solution found in {len(path)-1} steps!")

    # Visualize the solution
    visualize_solution(path)

if __name__ == "__main__":
    main()
