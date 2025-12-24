"""
Position evaluator for AI analysis.
Evaluates board positions and calculates win probability.
"""

from typing import Tuple
from .board import Board, Stone
import math


class PositionEvaluator:
    """Evaluates board positions for AI decision making."""
    
    # Evaluation scores for different patterns
    FIVE = 100000      # Winning move
    OPEN_FOUR = 10000  # Guaranteed win next move
    FOUR = 1000        # Four in a row (one end blocked)
    OPEN_THREE = 500   # Open three
    THREE = 100        # Three in a row (one end blocked)
    OPEN_TWO = 50      # Open two
    TWO = 10           # Two in a row (one end blocked)
    
    def __init__(self, board: Board):
        self.board = board
    
    def evaluate(self, perspective: Stone = Stone.BLACK) -> int:
        """
        Evaluate the current board position.
        Returns a score from the perspective of the given stone.
        Positive = good for perspective, Negative = bad for perspective.
        """
        if self.board.game_over:
            if self.board.winner == perspective:
                return self.FIVE
            elif self.board.winner is not None:
                return -self.FIVE
        
        score = 0
        opponent = Stone.WHITE if perspective == Stone.BLACK else Stone.BLACK
        
        # Evaluate all positions
        for row in range(Board.SIZE):
            for col in range(Board.SIZE):
                if self.board.grid[row, col] == perspective:
                    score += self._evaluate_position(row, col, perspective)
                elif self.board.grid[row, col] == opponent:
                    score -= self._evaluate_position(row, col, opponent)
        
        # Add positional bonus (center is better)
        score += self._positional_bonus(perspective)
        
        return score
    
    def _evaluate_position(self, row: int, col: int, stone: Stone) -> int:
        """Evaluate a single stone position."""
        score = 0
        
        for direction in Board.DIRECTIONS:
            pattern_score = self._evaluate_direction(row, col, stone, direction)
            score += pattern_score
        
        return score
    
    def _evaluate_direction(self, row: int, col: int, stone: Stone, 
                           direction: Tuple[int, int]) -> int:
        """Evaluate a pattern in a specific direction."""
        dr, dc = direction
        
        # Count consecutive stones
        count = self.board.count_consecutive(row, col, stone, direction)
        
        if count >= 5:
            return self.FIVE
        
        # Check if the pattern is open (both ends are empty)
        is_open = self._is_pattern_open(row, col, stone, direction)
        
        # Score based on count and openness
        if count == 4:
            return self.OPEN_FOUR if is_open else self.FOUR
        elif count == 3:
            return self.OPEN_THREE if is_open else self.THREE
        elif count == 2:
            return self.OPEN_TWO if is_open else self.TWO
        
        return 0
    
    def _is_pattern_open(self, row: int, col: int, stone: Stone, 
                        direction: Tuple[int, int]) -> bool:
        """Check if a pattern has both ends open."""
        dr, dc = direction
        
        # Find the extent of the pattern
        # Positive direction
        r, c = row, col
        while self.board.is_valid_position(r, c) and self.board.grid[r, c] == stone:
            r += dr
            c += dc
        
        # Check if positive end is open
        positive_open = self.board.is_valid_position(r, c) and self.board.grid[r, c] == Stone.EMPTY
        
        # Negative direction
        r, c = row, col
        while self.board.is_valid_position(r, c) and self.board.grid[r, c] == stone:
            r -= dr
            c -= dc
        
        # Check if negative end is open
        negative_open = self.board.is_valid_position(r, c) and self.board.grid[r, c] == Stone.EMPTY
        
        return positive_open and negative_open
    
    def _positional_bonus(self, stone: Stone) -> int:
        """Give bonus for stones near the center."""
        bonus = 0
        center = Board.SIZE // 2
        
        for row in range(Board.SIZE):
            for col in range(Board.SIZE):
                if self.board.grid[row, col] == stone:
                    # Distance from center
                    dist = abs(row - center) + abs(col - center)
                    # Closer to center = higher bonus
                    bonus += max(0, 10 - dist)
        
        return bonus
    
    def calculate_win_probability(self, perspective: Stone = Stone.BLACK) -> float:
        """
        Calculate win probability for the given stone.
        Returns a value between 0.0 and 1.0.
        """
        score = self.evaluate(perspective)
        
        # Use sigmoid function to convert score to probability
        # sigmoid(x) = 1 / (1 + e^(-x))
        # Scale the score to make it more sensitive
        scaled_score = score / 1000.0
        
        # Clamp to avoid overflow
        scaled_score = max(-10, min(10, scaled_score))
        
        probability = 1.0 / (1.0 + math.exp(-scaled_score))
        
        return probability
    
    def get_best_moves(self, stone: Stone, top_n: int = 5) -> list:
        """
        Get the top N best moves for the given stone.
        Returns list of (row, col, score) tuples.
        """
        moves = []
        
        for row in range(Board.SIZE):
            for col in range(Board.SIZE):
                if self.board.is_empty(row, col):
                    # Simulate the move
                    self.board.grid[row, col] = stone
                    score = self.evaluate(stone)
                    self.board.grid[row, col] = Stone.EMPTY
                    
                    moves.append((row, col, score))
        
        # Sort by score (descending)
        moves.sort(key=lambda x: x[2], reverse=True)
        
        return moves[:top_n]
