"""
Main window for Omok-Lab application.
"""

from PyQt6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
                             QPushButton, QDialog, QLabel, QButtonGroup, QRadioButton,
                             QMessageBox, QToolBar, QStatusBar, QTableWidgetItem)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QMargins
from PyQt6.QtGui import QIcon, QAction, QFont
from core.board import Board, Stone
from core.rule_engine import RenjuRuleEngine
from core.evaluator import PositionEvaluator
from core.minimax import MinimaxAI
from ui.board_widget import BoardWidget
from ui.sidebar_widget import SidebarWidget
import time


class AIWorker(QThread):
    """Worker thread for AI computation."""
    
    move_calculated = pyqtSignal(int, int, int)  # row, col, score
    
    def __init__(self, board: Board, stone: Stone):
        super().__init__()
        self.board = board.copy()
        self.stone = stone
        self.ai = MinimaxAI(self.board, max_depth=3, time_limit=5.0)
    
    def run(self):
        """Calculate the best move."""
        result = self.ai.get_best_move(self.stone)
        if result:
            row, col, score = result
            self.move_calculated.emit(row, col, score)


class PlayerSelectionDialog(QDialog):
    """Dialog for selecting player color at game start."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Choose Your Color")
        self.setModal(True)
        self.setFixedSize(400, 250)
        self.selected_color = Stone.BLACK
        
        self.setStyleSheet("""
            QDialog {
                background-color: #111418;
            }
            QLabel {
                color: #ffffff;
                font-size: 16px;
            }
            QRadioButton {
                color: #ffffff;
                font-size: 14px;
                padding: 10px;
            }
            QRadioButton::indicator {
                width: 20px;
                height: 20px;
            }
            QPushButton {
                background-color: #2b8cee;
                color: #ffffff;
                border: none;
                border-radius: 8px;
                padding: 12px 32px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1e7ed6;
            }
        """)
        
        self._init_ui()
    
    def _init_ui(self):
        """Initialize the UI."""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # Title
        title = QLabel("Welcome to Omok-Lab!")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #2b8cee;")
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Choose your stone color to begin")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("font-size: 14px; color: #9dabb9;")
        layout.addWidget(subtitle)
        
        # Radio buttons
        radio_layout = QVBoxLayout()
        radio_layout.setSpacing(10)
        
        self.button_group = QButtonGroup(self)
        
        self.black_radio = QRadioButton("⚫ Black (First Player)")
        self.black_radio.setChecked(True)
        self.button_group.addButton(self.black_radio)
        radio_layout.addWidget(self.black_radio)
        
        self.white_radio = QRadioButton("⚪ White (Second Player)")
        self.button_group.addButton(self.white_radio)
        radio_layout.addWidget(self.white_radio)
        
        layout.addLayout(radio_layout)
        
        layout.addStretch()
        
        # Start button
        start_btn = QPushButton("Start Game")
        start_btn.clicked.connect(self.accept)
        layout.addWidget(start_btn, alignment=Qt.AlignmentFlag.AlignCenter)
    
    def get_selected_color(self) -> Stone:
        """Get the selected stone color."""
        if self.black_radio.isChecked():
            return Stone.BLACK
        else:
            return Stone.WHITE


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Omok-Lab v2.4.0 (Pro)")
        self.setMinimumSize(1400, 800)
        
        # Game state
        self.board = Board()
        self.rule_engine = RenjuRuleEngine(self.board)
        self.evaluator = PositionEvaluator(self.board)
        self.player_color = Stone.BLACK
        self.ai_color = Stone.WHITE
        self.ai_worker: AIWorker = None
        self.last_probability = 0.5
        
        # Apply dark theme
        self.setStyleSheet("""
            QMainWindow {
                background-color: #111418;
            }
            QToolBar {
                background-color: #111418;
                border-bottom: 1px solid #283039;
                spacing: 8px;
                padding: 8px;
            }
            QToolButton {
                background-color: #1c2127;
                border: 1px solid #283039;
                border-radius: 8px;
                padding: 8px 16px;
                color: #9dabb9;
            }
            QToolButton:hover {
                background-color: #283039;
                color: #ffffff;
            }
            QStatusBar {
                background-color: #111418;
                border-top: 1px solid #283039;
                color: #9dabb9;
            }
        """)
        
        self._init_ui()
        self._show_player_selection()
    
    def _init_ui(self):
        """Initialize the UI components."""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Board widget
        self.board_widget = BoardWidget(self.board)
        self.board_widget.cell_clicked.connect(self._on_cell_clicked)
        main_layout.addWidget(self.board_widget, 1)
        
        # Sidebar
        self.sidebar = SidebarWidget()
        self.sidebar.ask_ai_question.connect(self._on_ai_question)
        main_layout.addWidget(self.sidebar)
        
        # Toolbar
        self._create_toolbar()
        
        # Status bar
        self.statusBar().showMessage("Ready to play")
    
    def _create_toolbar(self):
        """Create the toolbar."""
        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)
        
        # New game
        new_game_action = QAction("🎮 New Game", self)
        new_game_action.triggered.connect(self._new_game)
        toolbar.addAction(new_game_action)
        
        toolbar.addSeparator()
        
        # Undo
        undo_action = QAction("↶ Undo", self)
        undo_action.triggered.connect(self._undo_move)
        toolbar.addAction(undo_action)
        
        # Redo (placeholder)
        redo_action = QAction("↷ Redo", self)
        redo_action.setEnabled(False)
        toolbar.addAction(redo_action)
        
        toolbar.addSeparator()
        
        # Settings (placeholder)
        settings_action = QAction("⚙ Settings", self)
        toolbar.addAction(settings_action)
    
    def _show_player_selection(self):
        """Show the player selection dialog."""
        dialog = PlayerSelectionDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.player_color = dialog.get_selected_color()
            self.ai_color = Stone.WHITE if self.player_color == Stone.BLACK else Stone.BLACK
            
            # If player chose white, AI makes first move
            if self.player_color == Stone.WHITE:
                self._make_ai_move()
    
    def _new_game(self):
        """Start a new game."""
        reply = QMessageBox.question(
            self,
            "New Game",
            "Start a new game?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.board.reset()
            self.board_widget.set_forbidden_positions(set())
            self.board_widget.set_recommended_move(None)
            self.board_widget.update()
            self.sidebar.history_table.setRowCount(0)
            self.sidebar.series.clear()
            self.sidebar.series.append(0, 50)
            self.last_probability = 0.5
            self._show_player_selection()
    
    def _on_cell_clicked(self, row: int, col: int):
        """Handle cell click."""
        if self.board.game_over:
            return
        
        # Check if it's player's turn
        if self.board.current_player != self.player_color:
            self.statusBar().showMessage("It's not your turn!")
            return
        
        # Check if position is empty
        if not self.board.is_empty(row, col):
            self.statusBar().showMessage("Position already occupied!")
            return
        
        # Check for forbidden move
        if self.player_color == Stone.BLACK and self.rule_engine.is_forbidden_move(row, col, self.player_color):
            reason = self.rule_engine.get_forbidden_reason(row, col, self.player_color)
            self.statusBar().showMessage(f"Forbidden move: {reason}")
            return
        
        # Make the move
        self._make_move(row, col, self.player_color)
        
        # Check for game over
        if self.board.game_over:
            self._handle_game_over()
            return
        
        # AI's turn
        self._make_ai_move()
    
    def _make_move(self, row: int, col: int, stone: Stone):
        """Make a move on the board."""
        start_time = time.time()
        success = self.board.place_stone(row, col, stone)
        time_taken = time.time() - start_time
        
        if success:
            # Update UI
            self.board_widget.update()
            
            # Update move history
            move = self.board.move_history[-1]
            coord = move.to_coordinate()
            
            # Add to history table
            if stone == Stone.BLACK:
                if len(self.board.move_history) % 2 == 1:
                    self.sidebar.add_move_to_history(
                        len(self.board.move_history),
                        coord,
                        "--",
                        f"{time_taken:.2f}s"
                    )
            else:
                # Update the last row with white's move
                row_count = self.sidebar.history_table.rowCount()
                if row_count > 0:
                    self.sidebar.history_table.setItem(
                        row_count - 1,
                        2,
                        QTableWidgetItem(coord)
                    )
                else:
                    self.sidebar.add_move_to_history(
                        len(self.board.move_history),
                        "--",
                        coord,
                        f"{time_taken:.2f}s"
                    )
            
            # Update win probability
            self._update_win_probability()
            
            # Update forbidden positions for next player
            next_player = self.board.current_player
            if next_player == Stone.BLACK:
                forbidden = self.rule_engine.get_all_forbidden_positions(Stone.BLACK)
                self.board_widget.set_forbidden_positions(forbidden)
            else:
                self.board_widget.set_forbidden_positions(set())
            
            # Update move counter
            self.sidebar.update_move_counter(len(self.board.move_history))
            
            self.statusBar().showMessage(f"Move {len(self.board.move_history)}: {coord}")
    
    def _make_ai_move(self):
        """Make an AI move."""
        if self.board.game_over:
            return
        
        self.sidebar.set_status("Thinking...", "#3b82f6")
        self.statusBar().showMessage("AI is thinking...")
        
        # Start AI worker thread
        self.ai_worker = AIWorker(self.board, self.ai_color)
        self.ai_worker.move_calculated.connect(self._on_ai_move_calculated)
        self.ai_worker.start()
    
    def _on_ai_move_calculated(self, row: int, col: int, score: int):
        """Handle AI move calculation completion."""
        self.sidebar.set_status("Ready", "#10b981")
        
        # Make the move
        self._make_move(row, col, self.ai_color)
        
        # Generate AI analysis message
        move = self.board.move_history[-1]
        coord = move.to_coordinate()
        message = f"Move {len(self.board.move_history)} ({coord}) is a strategic position. "
        message += f"Evaluation score: {score}. "
        
        if score > 5000:
            message += "This creates a strong offensive opportunity!"
        elif score > 1000:
            message += "This move strengthens my position."
        else:
            message += "This is a solid defensive move."
        
        self.sidebar.set_ai_message(message)
        
        # Check for game over
        if self.board.game_over:
            self._handle_game_over()
    
    def _update_win_probability(self):
        """Update the win probability display."""
        prob = self.evaluator.calculate_win_probability(Stone.BLACK)
        trend = (prob - self.last_probability) * 100
        
        if self.board.current_player == Stone.BLACK:
            player_name = "Black"
            display_prob = prob
        else:
            player_name = "White"
            display_prob = 1.0 - prob
        
        self.sidebar.update_win_probability(display_prob, player_name, trend)
        self.sidebar.update_chart(len(self.board.move_history), prob)
        
        self.last_probability = prob
    
    def _undo_move(self):
        """Undo the last move."""
        if self.board.undo_move():
            # If AI just moved, undo one more time to undo player's move
            if self.board.current_player == self.ai_color:
                self.board.undo_move()
            
            self.board_widget.update()
            
            # Update history table
            row_count = self.sidebar.history_table.rowCount()
            if row_count > 0:
                self.sidebar.history_table.removeRow(row_count - 1)
            
            self.statusBar().showMessage("Move undone")
    
    def _on_ai_question(self, question: str):
        """Handle AI question from user."""
        # Simple response based on current position
        response = f"You asked: '{question}'. "
        
        if "forbidden" in question.lower():
            response += "Forbidden moves are marked with red X on the board. "
            response += "Black cannot make 3-3, 4-4, or overline moves."
        elif "recommend" in question.lower() or "best" in question.lower():
            # Get best moves
            best_moves = self.evaluator.get_best_moves(self.player_color, top_n=3)
            if best_moves:
                response += "Top recommended moves: "
                for i, (r, c, s) in enumerate(best_moves[:3]):
                    from core.board import Move
                    coord = Move(r, c, self.player_color, 0).to_coordinate()
                    response += f"{coord} (score: {s})"
                    if i < len(best_moves) - 1:
                        response += ", "
        else:
            response += "I'm here to help you improve your game. Ask me about forbidden moves, best moves, or strategy!"
        
        self.sidebar.set_ai_message(response)
    
    def _handle_game_over(self):
        """Handle game over."""
        winner_name = "Black" if self.board.winner == Stone.BLACK else "White"
        
        if self.board.winner == self.player_color:
            message = f"Congratulations! You ({winner_name}) won! 🎉"
        else:
            message = f"AI ({winner_name}) won! Better luck next time!"
        
        self.sidebar.set_ai_message(message)
        self.sidebar.set_status("Game Over", "#ef4444")
        self.statusBar().showMessage(message)
        
        QMessageBox.information(self, "Game Over", message)
