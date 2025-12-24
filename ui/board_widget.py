"""
Board widget for rendering the Omok game board.
"""

from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, pyqtSignal, QPointF, QRectF
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor, QRadialGradient, QFont
from core.board import Board, Stone
from typing import Optional, Set, Tuple


class BoardWidget(QWidget):
    """Widget for rendering and interacting with the game board."""
    
    # Signals
    cell_clicked = pyqtSignal(int, int)  # row, col
    
    def __init__(self, board: Board, parent=None):
        super().__init__(parent)
        self.board = board
        self.cell_size = 40
        self.margin = 40
        self.setMinimumSize(700, 700)
        
        # Visual state
        self.forbidden_positions: Set[Tuple[int, int]] = set()
        self.recommended_move: Optional[Tuple[int, int]] = None
        self.hover_pos: Optional[Tuple[int, int]] = None
        
        # Enable mouse tracking for hover effects
        self.setMouseTracking(True)
        
        # Star points (hoshi)
        self.star_points = [(3, 3), (3, 11), (7, 7), (11, 3), (11, 11)]
    
    def set_forbidden_positions(self, positions: Set[Tuple[int, int]]):
        """Set the forbidden move positions."""
        self.forbidden_positions = positions
        self.update()
    
    def set_recommended_move(self, position: Optional[Tuple[int, int]]):
        """Set the AI recommended move."""
        self.recommended_move = position
        self.update()
    
    def paintEvent(self, event):
        """Paint the board."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Calculate board dimensions
        self._calculate_dimensions()
        
        # Draw background
        self._draw_background(painter)
        
        # Draw grid
        self._draw_grid(painter)
        
        # Draw star points
        self._draw_star_points(painter)
        
        # Draw hover effect
        if self.hover_pos:
            self._draw_hover(painter, *self.hover_pos)
        
        # Draw stones
        self._draw_stones(painter)
        
        # Draw forbidden positions
        self._draw_forbidden_positions(painter)
        
        # Draw recommended move
        if self.recommended_move:
            self._draw_recommended_move(painter, *self.recommended_move)
        
        # Draw winning line
        if self.board.winning_line:
            self._draw_winning_line(painter)
    
    def _calculate_dimensions(self):
        """Calculate cell size based on widget size."""
        available_width = self.width() - 2 * self.margin
        available_height = self.height() - 2 * self.margin
        self.cell_size = min(available_width, available_height) / (Board.SIZE - 1)
    
    def _draw_background(self, painter: QPainter):
        """Draw the wood-textured background."""
        # Board background (wood color)
        board_color = QColor(234, 182, 118)  # #eab676
        painter.fillRect(self.rect(), QColor(17, 20, 24))  # Dark background
        
        # Board area
        board_rect = QRectF(
            self.margin - 20,
            self.margin - 20,
            self.cell_size * (Board.SIZE - 1) + 40,
            self.cell_size * (Board.SIZE - 1) + 40
        )
        
        # Frame
        frame_color = QColor(204, 163, 114)  # #cca372
        painter.fillRect(board_rect, frame_color)
        
        # Inner board
        inner_rect = QRectF(
            self.margin,
            self.margin,
            self.cell_size * (Board.SIZE - 1),
            self.cell_size * (Board.SIZE - 1)
        )
        painter.fillRect(inner_rect, board_color)
    
    def _draw_grid(self, painter: QPainter):
        """Draw the grid lines."""
        pen = QPen(QColor(0, 0, 0, 100), 1)
        painter.setPen(pen)
        
        # Vertical lines
        for col in range(Board.SIZE):
            x = self.margin + col * self.cell_size
            y1 = self.margin
            y2 = self.margin + (Board.SIZE - 1) * self.cell_size
            painter.drawLine(QPointF(x, y1), QPointF(x, y2))
        
        # Horizontal lines
        for row in range(Board.SIZE):
            y = self.margin + row * self.cell_size
            x1 = self.margin
            x2 = self.margin + (Board.SIZE - 1) * self.cell_size
            painter.drawLine(QPointF(x1, y), QPointF(x2, y))
    
    def _draw_star_points(self, painter: QPainter):
        """Draw star points (hoshi)."""
        brush = QBrush(QColor(0, 0, 0))
        painter.setBrush(brush)
        painter.setPen(Qt.PenStyle.NoPen)
        
        for row, col in self.star_points:
            x, y = self._get_position(row, col)
            painter.drawEllipse(QPointF(x, y), 3, 3)
    
    def _draw_stones(self, painter: QPainter):
        """Draw all stones on the board."""
        for row in range(Board.SIZE):
            for col in range(Board.SIZE):
                stone = self.board.get_stone(row, col)
                if stone != Stone.EMPTY:
                    self._draw_stone(painter, row, col, stone)
    
    def _draw_stone(self, painter: QPainter, row: int, col: int, stone: Stone):
        """Draw a single stone."""
        x, y = self._get_position(row, col)
        radius = self.cell_size * 0.42
        
        if stone == Stone.BLACK:
            # Black stone with gradient
            gradient = QRadialGradient(x - radius * 0.3, y - radius * 0.3, radius * 1.5)
            gradient.setColorAt(0, QColor(100, 100, 100))
            gradient.setColorAt(0.5, QColor(30, 41, 59))  # slate-900
            gradient.setColorAt(1, QColor(0, 0, 0))
            
            painter.setBrush(QBrush(gradient))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(QPointF(x, y), radius, radius)
        
        else:  # White stone
            # White stone with border
            painter.setBrush(QBrush(QColor(241, 245, 249)))  # slate-100
            painter.setPen(QPen(QColor(203, 213, 225), 1))  # slate-300
            painter.drawEllipse(QPointF(x, y), radius, radius)
        
        # Draw move number
        move_num = self._get_move_number(row, col)
        if move_num is not None:
            self._draw_move_number(painter, x, y, move_num, stone)
    
    def _draw_move_number(self, painter: QPainter, x: float, y: float, 
                         move_num: int, stone: Stone):
        """Draw move number on the stone."""
        # Only show last move number
        if move_num == len(self.board.move_history):
            font = QFont("Arial", int(self.cell_size * 0.2), QFont.Weight.Bold)
            painter.setFont(font)
            
            # Red badge
            badge_size = self.cell_size * 0.35
            badge_x = x + self.cell_size * 0.25
            badge_y = y + self.cell_size * 0.25
            
            painter.setBrush(QBrush(QColor(239, 68, 68)))  # red-500
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(
                QRectF(badge_x - badge_size/2, badge_y - badge_size/2, 
                       badge_size, badge_size * 0.6),
                3, 3
            )
            
            # Number text
            painter.setPen(QPen(QColor(255, 255, 255)))
            painter.drawText(
                QRectF(badge_x - badge_size/2, badge_y - badge_size/2,
                       badge_size, badge_size * 0.6),
                Qt.AlignmentFlag.AlignCenter,
                str(move_num)
            )
    
    def _get_move_number(self, row: int, col: int) -> Optional[int]:
        """Get the move number for a position."""
        for i, move in enumerate(self.board.move_history):
            if move.row == row and move.col == col:
                return i + 1
        return None
    
    def _draw_forbidden_positions(self, painter: QPainter):
        """Draw red X marks on forbidden positions."""
        font = QFont("Arial", int(self.cell_size * 0.8), QFont.Weight.Bold)
        painter.setFont(font)
        painter.setPen(QPen(QColor(220, 38, 38), 3))  # red-600
        
        for row, col in self.forbidden_positions:
            if self.board.is_empty(row, col):
                x, y = self._get_position(row, col)
                size = self.cell_size * 0.3
                
                # Draw X
                painter.drawLine(
                    QPointF(x - size, y - size),
                    QPointF(x + size, y + size)
                )
                painter.drawLine(
                    QPointF(x + size, y - size),
                    QPointF(x - size, y + size)
                )
    
    def _draw_recommended_move(self, painter: QPainter, row: int, col: int):
        """Draw AI recommended move indicator."""
        if not self.board.is_empty(row, col):
            return
        
        x, y = self._get_position(row, col)
        radius = self.cell_size * 0.25
        
        # Pulsing green circle
        painter.setBrush(QBrush(QColor(34, 197, 94, 150)))  # green-500 with alpha
        painter.setPen(QPen(QColor(74, 222, 128), 2))  # green-400
        painter.drawEllipse(QPointF(x, y), radius, radius)
    
    def _draw_hover(self, painter: QPainter, row: int, col: int):
        """Draw hover effect."""
        if not self.board.is_empty(row, col):
            return
        
        x, y = self._get_position(row, col)
        radius = self.cell_size * 0.15
        
        # Semi-transparent circle
        color = QColor(43, 140, 238, 80)  # primary blue with alpha
        painter.setBrush(QBrush(color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(QPointF(x, y), radius, radius)
    
    def _draw_winning_line(self, painter: QPainter):
        """Draw a line through the winning stones."""
        if len(self.board.winning_line) < 2:
            return
        
        pen = QPen(QColor(34, 197, 94), 4)  # green-500
        painter.setPen(pen)
        
        start_row, start_col = self.board.winning_line[0]
        end_row, end_col = self.board.winning_line[-1]
        
        x1, y1 = self._get_position(start_row, start_col)
        x2, y2 = self._get_position(end_row, end_col)
        
        painter.drawLine(QPointF(x1, y1), QPointF(x2, y2))
    
    def _get_position(self, row: int, col: int) -> Tuple[float, float]:
        """Convert board coordinates to pixel coordinates."""
        x = self.margin + col * self.cell_size
        y = self.margin + row * self.cell_size
        return x, y
    
    def _get_board_position(self, x: float, y: float) -> Optional[Tuple[int, int]]:
        """Convert pixel coordinates to board coordinates."""
        col = round((x - self.margin) / self.cell_size)
        row = round((y - self.margin) / self.cell_size)
        
        if 0 <= row < Board.SIZE and 0 <= col < Board.SIZE:
            return row, col
        return None
    
    def mousePressEvent(self, event):
        """Handle mouse click."""
        if event.button() == Qt.MouseButton.LeftButton:
            pos = self._get_board_position(event.position().x(), event.position().y())
            if pos:
                row, col = pos
                self.cell_clicked.emit(row, col)
    
    def mouseMoveEvent(self, event):
        """Handle mouse move for hover effect."""
        pos = self._get_board_position(event.position().x(), event.position().y())
        if pos != self.hover_pos:
            self.hover_pos = pos
            self.update()
    
    def leaveEvent(self, event):
        """Clear hover when mouse leaves."""
        self.hover_pos = None
        self.update()
