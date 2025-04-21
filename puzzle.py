class Puzzle:
    nodes_explored = 0  # Global counter

    def __init__(self, board, g=0):
        self.board = board
        self.g = g
        self.zero_pos = board.index(0)
        Puzzle.nodes_explored += 1

    def get_move(self, other):
        dx = (other.zero_pos // 4) - (self.zero_pos // 4)
        dy = (other.zero_pos % 4) - (self.zero_pos % 4)

        if dx == -1: return "UP"
        if dx == 1: return "DOWN"
        if dy == -1: return "LEFT"
        if dy == 1: return "RIGHT"
        return "STAY"
        
    def get_possible_moves(self):
        """Get all possible moves from current state"""
        moves = []
        row, col = self.zero_pos // 4, self.zero_pos % 4
        
        # Check all four directions
        if row > 0:  # UP
            moves.append(("UP", self.zero_pos - 4))
        if row < 3:  # DOWN
            moves.append(("DOWN", self.zero_pos + 4))
        if col > 0:  # LEFT
            moves.append(("LEFT", self.zero_pos - 1))
        if col < 3:  # RIGHT
            moves.append(("RIGHT", self.zero_pos + 1))
            
        return moves
        
    def move(self, new_blank_pos):
        """Create a new puzzle state by moving the blank to new position"""
        new_board = self.board.copy()
        # Swap blank (0) with the tile at new position
        new_board[self.zero_pos], new_board[new_blank_pos] = new_board[new_blank_pos], new_board[self.zero_pos]
        return Puzzle(new_board, self.g + 1)
        
    def is_goal(self):
        """Check if current state is the goal state"""
        goal = list(range(1, 16)) + [0]  # Goal is [1,2,3,...,15,0]
        return self.board == goal
        
    def __eq__(self, other):
        if isinstance(other, Puzzle):
            return self.board == other.board
        return False
        
    def __hash__(self):
        return hash(tuple(self.board))

    def __str__(self):
        # Pretty board printing
        lines = []
        for i in range(0, 16, 4):
            row = self.board[i:i+4]
            lines.append(" ".join(f"{n:2}" if n != 0 else "  " for n in row))
        return "\n".join(lines)

    def get_successors(self):
        successors = []
        blank_pos = self.board.index(0)
        row, col = divmod(blank_pos, 4)

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 4 and 0 <= new_col < 4:
                new_blank = new_row * 4 + new_col
                new_board = self.board[:]
                new_board[blank_pos], new_board[new_blank] = new_board[new_blank], new_board[blank_pos]
                successors.append(Puzzle(new_board))
        return successors
