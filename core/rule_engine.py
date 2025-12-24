"""
Renju Rule Engine for detecting forbidden moves.
Implements 3-3, 4-4, and overline detection for black stones.
"""

from typing import List, Tuple, Set
from .board import Board, Stone


class RenjuRuleEngine:
    """Enforces Renju rules for the game."""
    
    def __init__(self, board: Board):
        self.board = board
    
    def is_forbidden_move(self, row: int, col: int, stone: Stone) -> bool:
        """
        Check if a move is forbidden under Renju rules.
        Only applies to black stones.
        """
        if stone != Stone.BLACK:
            return False
        
        # Temporarily place the stone
        original = self.board.grid[row, col]
        self.board.grid[row, col] = stone
        
        # Check all forbidden patterns
        is_33 = self._is_double_three(row, col)
        is_44 = self._is_double_four(row, col)
        is_overline = self._is_overline(row, col)
        
        # Restore original state
        self.board.grid[row, col] = original
        
        return is_33 or is_44 or is_overline
    
    def get_all_forbidden_positions(self, stone: Stone) -> Set[Tuple[int, int]]:
        """Get all forbidden positions for the given stone color."""
        if stone != Stone.BLACK:
            return set()
        
        forbidden = set()
        for row in range(Board.SIZE):
            for col in range(Board.SIZE):
                if self.board.is_empty(row, col):
                    if self.is_forbidden_move(row, col, stone):
                        forbidden.add((row, col))
        
        return forbidden
    
    def _is_overline(self, row: int, col: int) -> bool:
        """Check if the move creates 6 or more consecutive stones (overline)."""
        for direction in Board.DIRECTIONS:
            count = self.board.count_consecutive(row, col, Stone.BLACK, direction)
            if count >= 6:
                return True
        return False
    
    def _is_double_three(self, row: int, col: int) -> bool:
        """Check if the move creates two or more open threes (3-3)."""
        open_threes = 0
        
        for direction in Board.DIRECTIONS:
            if self._is_open_three(row, col, direction):
                open_threes += 1
                if open_threes >= 2:
                    return True
        
        return False
    
    def _is_double_four(self, row: int, col: int) -> bool:
        """Check if the move creates two or more open fours (4-4)."""
        open_fours = 0
        
        for direction in Board.DIRECTIONS:
            if self._is_open_four(row, col, direction):
                open_fours += 1
                if open_fours >= 2:
                    return True
        
        return False
    
    def _is_open_three(self, row: int, col: int, direction: Tuple[int, int]) -> bool:
        """
        Check if there's an open three in the given direction.
        An open three means exactly 3 consecutive stones with both ends open,
        and can become a five in one more move.
        """
        dr, dc = direction
        pattern = self._get_pattern(row, col, direction, 6)
        
        # Open three patterns (X = black, _ = empty, ? = any)
        # _XXX_ (basic open three)
        open_three_patterns = [
            [0, 1, 1, 1, 0],  # _XXX_
        ]
        
        # Check if pattern matches any open three
        for i in range(len(pattern) - 4):
            segment = pattern[i:i+5]
            if segment in open_three_patterns:
                # Verify it can become a five
                if self._can_become_five(row, col, direction, segment, i):
                    return True
        
        return False
    
    def _is_open_four(self, row: int, col: int, direction: Tuple[int, int]) -> bool:
        """
        Check if there's an open four in the given direction.
        An open four means exactly 4 consecutive stones with at least one end open,
        guaranteeing a win in the next move.
        """
        dr, dc = direction
        pattern = self._get_pattern(row, col, direction, 7)
        
        # Open four patterns
        # _XXXX_ (both ends open)
        # _XXXX (one end open)
        open_four_patterns = [
            [0, 1, 1, 1, 1, 0],  # _XXXX_
        ]
        
        for i in range(len(pattern) - 5):
            segment = pattern[i:i+6]
            if segment == open_four_patterns[0]:
                return True
        
        # Check for one-end-open four
        for i in range(len(pattern) - 4):
            segment = pattern[i:i+5]
            if segment == [0, 1, 1, 1, 1] or segment == [1, 1, 1, 1, 0]:
                # Make sure it's not blocked on the open end
                if segment[0] == 0:  # Open on left
                    if i > 0 and pattern[i-1] != 2:  # Not blocked by white
                        return True
                if segment[-1] == 0:  # Open on right
                    if i + 5 < len(pattern) and pattern[i+5] != 2:
                        return True
        
        return False
    
    def _get_pattern(self, row: int, col: int, direction: Tuple[int, int], 
                     length: int) -> List[int]:
        """
        Get a pattern of stones in the given direction.
        Returns a list where 0=empty, 1=black, 2=white, -1=out of bounds.
        """
        dr, dc = direction
        pattern = []
        
        # Get pattern centered on (row, col)
        start_offset = -(length // 2)
        for i in range(length):
            r = row + (start_offset + i) * dr
            c = col + (start_offset + i) * dc
            
            if not self.board.is_valid_position(r, c):
                pattern.append(-1)  # Out of bounds
            else:
                pattern.append(int(self.board.grid[r, c]))
        
        return pattern
    
    def _can_become_five(self, row: int, col: int, direction: Tuple[int, int],
                        segment: List[int], offset: int) -> bool:
        """Check if an open three can become a five."""
        # For a true open three, adding one stone on either end should create a four
        # This is a simplified check - in reality, we'd need to verify
        # that the resulting four is also open
        
        # Count how many empty spaces are adjacent
        empty_count = segment.count(0)
        black_count = segment.count(1)
        
        # A valid open three has exactly 3 blacks and 2 empties on the ends
        return black_count == 3 and empty_count == 2
    
    def get_forbidden_reason(self, row: int, col: int, stone: Stone) -> str:
        """Get a human-readable reason why a move is forbidden."""
        if stone != Stone.BLACK:
            return ""
        
        original = self.board.grid[row, col]
        self.board.grid[row, col] = stone
        
        reasons = []
        
        if self._is_double_three(row, col):
            reasons.append("Double Three (3-3)")
        
        if self._is_double_four(row, col):
            reasons.append("Double Four (4-4)")
        
        if self._is_overline(row, col):
            reasons.append("Overline (6+ stones)")
        
        self.board.grid[row, col] = original
        
        return ", ".join(reasons) if reasons else ""
