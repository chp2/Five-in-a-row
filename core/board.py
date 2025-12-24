"""
Board state management for Omok game.
Handles stone placement, move history, and board state.
"""

import numpy as np
from typing import List, Tuple, Optional
from enum import IntEnum


class Stone(IntEnum):
    """Stone types on the board."""
    EMPTY = 0
    BLACK = 1
    WHITE = 2


class Move:
    """Represents a single move in the game."""
    
    def __init__(self, row: int, col: int, stone: Stone, move_number: int, time_taken: float = 0.0):
        self.row = row
        self.col = col
        self.stone = stone
        self.move_number = move_number
        self.time_taken = time_taken
        self.timestamp = 0  # Will be set when move is made
    
    def to_coordinate(self) -> str:
        """Convert to coordinate notation (e.g., 'H8')."""
        # Columns: A-O (excluding I)
        cols = 'ABCDEFGHJKLMNO'
        return f"{cols[self.col]}{self.row + 1}"
    
    @staticmethod
    def from_coordinate(coord: str) -> Tuple[int, int]:
        """Convert coordinate notation to (row, col)."""
        cols = 'ABCDEFGHJKLMNO'
        col = cols.index(coord[0].upper())
        row = int(coord[1:]) - 1
        return row, col


class Board:
    """Manages the game board state."""
    
    SIZE = 15
    DIRECTIONS = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal \
        (1, -1),  # Diagonal /
    ]
    
    def __init__(self):
        """Initialize an empty 15x15 board."""
        self.grid = np.zeros((self.SIZE, self.SIZE), dtype=int)
        self.move_history: List[Move] = []
        self.current_player = Stone.BLACK
        self.winner: Optional[Stone] = None
        self.game_over = False
        self.winning_line: List[Tuple[int, int]] = []
    
    def reset(self):
        """Reset the board to initial state."""
        self.grid = np.zeros((self.SIZE, self.SIZE), dtype=int)
        self.move_history.clear()
        self.current_player = Stone.BLACK
        self.winner = None
        self.game_over = False
        self.winning_line.clear()
    
    def is_valid_position(self, row: int, col: int) -> bool:
        """Check if position is within board bounds."""
        return 0 <= row < self.SIZE and 0 <= col < self.SIZE
    
    def is_empty(self, row: int, col: int) -> bool:
        """Check if position is empty."""
        return self.is_valid_position(row, col) and self.grid[row, col] == Stone.EMPTY
    
    def place_stone(self, row: int, col: int, stone: Stone, time_taken: float = 0.0) -> bool:
        """
        Place a stone on the board.
        Returns True if successful, False otherwise.
        """
        if not self.is_empty(row, col) or self.game_over:
            return False
        
        self.grid[row, col] = stone
        move = Move(row, col, stone, len(self.move_history) + 1, time_taken)
        self.move_history.append(move)
        
        # Check for win
        if self._check_win(row, col, stone):
            self.winner = stone
            self.game_over = True
        
        # Switch player
        self.current_player = Stone.WHITE if stone == Stone.BLACK else Stone.BLACK
        
        return True
    
    def undo_move(self) -> bool:
        """Undo the last move. Returns True if successful."""
        if not self.move_history:
            return False
        
        last_move = self.move_history.pop()
        self.grid[last_move.row, last_move.col] = Stone.EMPTY
        self.current_player = last_move.stone
        self.winner = None
        self.game_over = False
        self.winning_line.clear()
        
        return True
    
    def get_stone(self, row: int, col: int) -> Stone:
        """Get the stone at the given position."""
        if not self.is_valid_position(row, col):
            return Stone.EMPTY
        return Stone(self.grid[row, col])
    
    def get_empty_positions(self) -> List[Tuple[int, int]]:
        """Get all empty positions on the board."""
        positions = []
        for row in range(self.SIZE):
            for col in range(self.SIZE):
                if self.grid[row, col] == Stone.EMPTY:
                    positions.append((row, col))
        return positions
    
    def count_consecutive(self, row: int, col: int, stone: Stone, 
                         direction: Tuple[int, int]) -> int:
        """
        Count consecutive stones in a given direction.
        Returns total count including the stone at (row, col).
        """
        dr, dc = direction
        count = 1  # Count the stone at (row, col)
        
        # Count in positive direction
        r, c = row + dr, col + dc
        while self.is_valid_position(r, c) and self.grid[r, c] == stone:
            count += 1
            r += dr
            c += dc
        
        # Count in negative direction
        r, c = row - dr, col - dc
        while self.is_valid_position(r, c) and self.grid[r, c] == stone:
            count += 1
            r -= dr
            c -= dc
        
        return count
    
    def get_line_stones(self, row: int, col: int, stone: Stone, 
                       direction: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Get all positions of consecutive stones in a direction."""
        dr, dc = direction
        positions = [(row, col)]
        
        # Positive direction
        r, c = row + dr, col + dc
        while self.is_valid_position(r, c) and self.grid[r, c] == stone:
            positions.append((r, c))
            r += dr
            c += dc
        
        # Negative direction
        r, c = row - dr, col - dc
        while self.is_valid_position(r, c) and self.grid[r, c] == stone:
            positions.append((r, c))
            r -= dr
            c -= dc
        
        return positions
    
    def _check_win(self, row: int, col: int, stone: Stone) -> bool:
        """Check if the last move resulted in a win."""
        for direction in self.DIRECTIONS:
            count = self.count_consecutive(row, col, stone, direction)
            
            # For black, exactly 5 wins. For white, 5 or more wins.
            if stone == Stone.BLACK:
                if count == 5:
                    self.winning_line = self.get_line_stones(row, col, stone, direction)
                    return True
            else:  # White
                if count >= 5:
                    self.winning_line = self.get_line_stones(row, col, stone, direction)
                    return True
        
        return False
    
    def copy(self) -> 'Board':
        """Create a deep copy of the board."""
        new_board = Board()
        new_board.grid = self.grid.copy()
        new_board.move_history = self.move_history.copy()
        new_board.current_player = self.current_player
        new_board.winner = self.winner
        new_board.game_over = self.game_over
        new_board.winning_line = self.winning_line.copy()
        return new_board
    
    def __str__(self) -> str:
        """String representation of the board."""
        lines = []
        cols = 'ABCDEFGHJKLMNO'
        
        # Column headers
        lines.append('   ' + ' '.join(cols))
        
        # Board rows (from top to bottom)
        for row in range(self.SIZE - 1, -1, -1):
            line = f"{row + 1:2d} "
            for col in range(self.SIZE):
                stone = self.grid[row, col]
                if stone == Stone.BLACK:
                    line += '● '
                elif stone == Stone.WHITE:
                    line += '○ '
                else:
                    line += '· '
            lines.append(line)
        
        return '\n'.join(lines)
