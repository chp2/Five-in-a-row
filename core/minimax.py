"""
Minimax AI algorithm with Alpha-Beta pruning.
"""

from typing import Tuple, Optional
from .board import Board, Stone
from .evaluator import PositionEvaluator
from .rule_engine import RenjuRuleEngine
import time


class MinimaxAI:
    """AI player using Minimax algorithm with Alpha-Beta pruning."""
    
    def __init__(self, board: Board, max_depth: int = 3, time_limit: float = 5.0):
        self.board = board
        self.max_depth = max_depth
        self.time_limit = time_limit
        self.evaluator = PositionEvaluator(board)
        self.rule_engine = RenjuRuleEngine(board)
        self.nodes_evaluated = 0
        self.start_time = 0
    
    def get_best_move(self, stone: Stone) -> Optional[Tuple[int, int, int]]:
        """
        Get the best move for the given stone.
        Returns (row, col, score) or None if no valid moves.
        """
        self.nodes_evaluated = 0
        self.start_time = time.time()
        
        best_move = None
        best_score = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        
        # Get candidate moves (prioritize center and nearby stones)
        candidates = self._get_candidate_moves(stone)
        
        if not candidates:
            return None
        
        for row, col in candidates:
            # Check time limit
            if time.time() - self.start_time > self.time_limit:
                break
            
            # Skip forbidden moves for black
            if stone == Stone.BLACK and self.rule_engine.is_forbidden_move(row, col, stone):
                continue
            
            # Make the move
            self.board.grid[row, col] = stone
            
            # Evaluate with minimax
            score = self._minimax(self.max_depth - 1, alpha, beta, False, stone)
            
            # Undo the move
            self.board.grid[row, col] = Stone.EMPTY
            
            if score > best_score:
                best_score = score
                best_move = (row, col, score)
            
            alpha = max(alpha, score)
        
        return best_move
    
    def _minimax(self, depth: int, alpha: float, beta: float, 
                 is_maximizing: bool, perspective: Stone) -> float:
        """
        Minimax algorithm with Alpha-Beta pruning.
        """
        self.nodes_evaluated += 1
        
        # Check time limit
        if time.time() - self.start_time > self.time_limit:
            return self.evaluator.evaluate(perspective)
        
        # Terminal conditions
        if depth == 0 or self.board.game_over:
            return self.evaluator.evaluate(perspective)
        
        current_stone = perspective if is_maximizing else (
            Stone.WHITE if perspective == Stone.BLACK else Stone.BLACK
        )
        
        candidates = self._get_candidate_moves(current_stone, limit=15)
        
        if not candidates:
            return self.evaluator.evaluate(perspective)
        
        if is_maximizing:
            max_eval = float('-inf')
            for row, col in candidates:
                # Skip forbidden moves
                if current_stone == Stone.BLACK and self.rule_engine.is_forbidden_move(row, col, current_stone):
                    continue
                
                self.board.grid[row, col] = current_stone
                eval_score = self._minimax(depth - 1, alpha, beta, False, perspective)
                self.board.grid[row, col] = Stone.EMPTY
                
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                
                if beta <= alpha:
                    break  # Beta cutoff
            
            return max_eval
        else:
            min_eval = float('inf')
            for row, col in candidates:
                # Skip forbidden moves
                if current_stone == Stone.BLACK and self.rule_engine.is_forbidden_move(row, col, current_stone):
                    continue
                
                self.board.grid[row, col] = current_stone
                eval_score = self._minimax(depth - 1, alpha, beta, True, perspective)
                self.board.grid[row, col] = Stone.EMPTY
                
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                
                if beta <= alpha:
                    break  # Alpha cutoff
            
            return min_eval
    
    def _get_candidate_moves(self, stone: Stone, limit: int = 25) -> list:
        """
        Get candidate moves prioritized by heuristics.
        This reduces the search space significantly.
        """
        candidates = []
        
        # If board is empty, start at center
        if len(self.board.move_history) == 0:
            center = Board.SIZE // 2
            return [(center, center)]
        
        # Get all empty positions near existing stones
        for row in range(Board.SIZE):
            for col in range(Board.SIZE):
                if self.board.is_empty(row, col):
                    # Check if there's a stone within 2 squares
                    if self._has_nearby_stone(row, col, distance=2):
                        # Quick evaluation
                        self.board.grid[row, col] = stone
                        score = self.evaluator.evaluate(stone)
                        self.board.grid[row, col] = Stone.EMPTY
                        
                        candidates.append((row, col, score))
        
        # Sort by score and return top candidates
        candidates.sort(key=lambda x: x[2], reverse=True)
        return [(r, c) for r, c, _ in candidates[:limit]]
    
    def _has_nearby_stone(self, row: int, col: int, distance: int = 2) -> bool:
        """Check if there's any stone within the given distance."""
        for dr in range(-distance, distance + 1):
            for dc in range(-distance, distance + 1):
                r, c = row + dr, col + dc
                if self.board.is_valid_position(r, c):
                    if self.board.grid[r, c] != Stone.EMPTY:
                        return True
        return False
