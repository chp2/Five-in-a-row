"""
Sidebar widget for analysis panel.
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTableWidget, QTableWidgetItem,
                             QTextEdit, QLineEdit, QScrollArea, QFrame)
from PyQt6.QtCore import Qt, pyqtSignal, QMargins
from PyQt6.QtGui import QFont, QColor, QPainter
from PyQt6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis
from core.board import Board, Move


class SidebarWidget(QWidget):
    """Sidebar for displaying analysis and move history."""
    
    # Signals
    ask_ai_question = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(420)
        self.setStyleSheet("""
            QWidget {
                background-color: #111418;
                color: #ffffff;
                font-family: 'Segoe UI', Arial;
            }
            QLabel {
                color: #9dabb9;
            }
            QPushButton {
                background-color: #1c2127;
                border: 1px solid #283039;
                border-radius: 4px;
                padding: 8px 16px;
                color: #9dabb9;
            }
            QPushButton:hover {
                background-color: #283039;
                color: #ffffff;
            }
            QTableWidget {
                background-color: #111418;
                border: none;
                gridline-color: #283039;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #283039;
            }
            QTableWidget::item:selected {
                background-color: rgba(43, 140, 238, 0.1);
            }
            QHeaderView::section {
                background-color: #1c2127;
                color: #9dabb9;
                padding: 8px;
                border: none;
                font-weight: bold;
                text-transform: uppercase;
                font-size: 11px;
            }
            QLineEdit {
                background-color: #111418;
                border: 1px solid #283039;
                border-radius: 8px;
                padding: 10px 40px 10px 16px;
                color: #ffffff;
            }
            QLineEdit:focus {
                border: 1px solid #2b8cee;
            }
        """)
        
        self._init_ui()
    
    def _init_ui(self):
        """Initialize the UI components."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Win probability section
        self.win_prob_widget = self._create_win_probability_section()
        layout.addWidget(self.win_prob_widget)
        
        # Move history section
        self.history_widget = self._create_move_history_section()
        layout.addWidget(self.history_widget, 1)
        
        # AI chat section
        self.chat_widget = self._create_ai_chat_section()
        layout.addWidget(self.chat_widget)
    
    def _create_win_probability_section(self) -> QWidget:
        """Create the win probability chart section."""
        widget = QWidget()
        widget.setStyleSheet("background-color: #161b22; border-bottom: 1px solid #283039;")
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header_layout = QHBoxLayout()
        
        # Left side - probability
        left_layout = QVBoxLayout()
        title = QLabel("Win Probability")
        title.setStyleSheet("color: #9dabb9; font-size: 14px; font-weight: 500;")
        left_layout.addWidget(title)
        
        prob_layout = QHBoxLayout()
        self.win_prob_label = QLabel("50%")
        self.win_prob_label.setStyleSheet("color: #ffffff; font-size: 36px; font-weight: bold;")
        prob_layout.addWidget(self.win_prob_label)
        
        self.player_label = QLabel("Black")
        self.player_label.setStyleSheet("color: #9dabb9; font-size: 18px;")
        prob_layout.addWidget(self.player_label)
        prob_layout.addStretch()
        
        self.trend_label = QLabel("+0%")
        self.trend_label.setStyleSheet("color: #10b981; font-size: 14px; font-weight: 500;")
        prob_layout.addWidget(self.trend_label)
        
        left_layout.addLayout(prob_layout)
        header_layout.addLayout(left_layout)
        
        # Right side - move counter and status
        right_layout = QVBoxLayout()
        right_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        self.move_counter = QLabel("Move 0")
        self.move_counter.setStyleSheet("color: #9dabb9; font-size: 12px;")
        right_layout.addWidget(self.move_counter)
        
        self.status_badge = QLabel("Ready")
        self.status_badge.setStyleSheet("""
            background-color: rgba(59, 130, 246, 0.2);
            color: #3b82f6;
            border: 1px solid rgba(59, 130, 246, 0.3);
            border-radius: 4px;
            padding: 4px 8px;
            font-size: 12px;
            font-weight: bold;
        """)
        right_layout.addWidget(self.status_badge)
        
        header_layout.addLayout(right_layout)
        layout.addLayout(header_layout)
        
        # Chart (simplified - will use QChart)
        self.chart_view = QChartView()
        self.chart_view.setFixedHeight(128)
        self.chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.chart_view.setStyleSheet("background-color: transparent; border: none;")
        
        self.chart = QChart()
        self.chart.setBackgroundVisible(False)
        self.chart.legend().setVisible(False)
        self.chart.setMargins(QMargins(0, 0, 0, 0))
        
        self.series = QLineSeries()
        self.series.append(0, 50)  # Initial point
        
        self.chart.addSeries(self.series)
        
        # Axes
        axis_x = QValueAxis()
        axis_x.setVisible(False)
        axis_y = QValueAxis()
        axis_y.setRange(0, 100)
        axis_y.setVisible(False)
        
        self.chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        self.chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        self.series.attachAxis(axis_x)
        self.series.attachAxis(axis_y)
        
        self.chart_view.setChart(self.chart)
        layout.addWidget(self.chart_view)
        
        return widget
    
    def _create_move_history_section(self) -> QWidget:
        """Create the move history table section."""
        widget = QWidget()
        widget.setStyleSheet("background-color: #111418;")
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Header
        header = QWidget()
        header.setStyleSheet("background-color: #161b22; border-bottom: 1px solid #283039;")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 12, 20, 12)
        
        title = QLabel("Move History")
        title.setStyleSheet("color: #ffffff; font-size: 14px; font-weight: 600;")
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        layout.addWidget(header)
        
        # Table
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(4)
        self.history_table.setHorizontalHeaderLabels(["#", "Black", "White", "Time"])
        self.history_table.horizontalHeader().setStretchLastSection(True)
        self.history_table.setColumnWidth(0, 50)
        self.history_table.setColumnWidth(1, 80)
        self.history_table.setColumnWidth(2, 80)
        self.history_table.verticalHeader().setVisible(False)
        self.history_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        
        layout.addWidget(self.history_table)
        
        return widget
    
    def _create_ai_chat_section(self) -> QWidget:
        """Create the AI chat interface section."""
        widget = QWidget()
        widget.setStyleSheet("background-color: #161b22; border-top: 1px solid #283039;")
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(16, 16, 16, 24)
        
        # AI message
        message_layout = QHBoxLayout()
        
        # Avatar (simplified)
        avatar = QLabel("🤖")
        avatar.setFixedSize(40, 40)
        avatar.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #6366f1, stop:0.5 #a855f7, stop:1 #ec4899);
            border-radius: 20px;
            font-size: 24px;
        """)
        avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        message_layout.addWidget(avatar)
        
        # Message bubble
        bubble_layout = QVBoxLayout()
        
        header_layout = QHBoxLayout()
        name = QLabel("OmokBot AI")
        name.setStyleSheet("color: #ffffff; font-size: 14px; font-weight: bold;")
        header_layout.addWidget(name)
        header_layout.addStretch()
        
        timestamp = QLabel("Just now")
        timestamp.setStyleSheet("color: #9dabb9; font-size: 10px;")
        header_layout.addWidget(timestamp)
        
        bubble_layout.addLayout(header_layout)
        
        self.ai_message = QLabel("Welcome to Omok-Lab! I'll analyze your moves and provide strategic advice.")
        self.ai_message.setWordWrap(True)
        self.ai_message.setStyleSheet("""
            background-color: #1c2127;
            border: 1px solid #283039;
            border-radius: 16px;
            border-top-left-radius: 0;
            padding: 12px;
            color: #d1d5db;
            font-size: 14px;
            line-height: 1.5;
        """)
        bubble_layout.addWidget(self.ai_message)
        
        message_layout.addLayout(bubble_layout, 1)
        layout.addLayout(message_layout)
        
        # Input field
        input_layout = QHBoxLayout()
        self.ai_input = QLineEdit()
        self.ai_input.setPlaceholderText("Ask AI about this position...")
        self.ai_input.returnPressed.connect(self._on_send_question)
        input_layout.addWidget(self.ai_input)
        
        layout.addLayout(input_layout)
        
        return widget
    
    def _on_send_question(self):
        """Handle sending a question to AI."""
        question = self.ai_input.text().strip()
        if question:
            self.ask_ai_question.emit(question)
            self.ai_input.clear()
    
    def update_win_probability(self, probability: float, player: str, trend: float):
        """Update the win probability display."""
        self.win_prob_label.setText(f"{int(probability * 100)}%")
        self.player_label.setText(player)
        
        if trend > 0:
            self.trend_label.setText(f"+{int(trend)}%")
            self.trend_label.setStyleSheet("color: #10b981; font-size: 14px; font-weight: 500;")
        elif trend < 0:
            self.trend_label.setText(f"{int(trend)}%")
            self.trend_label.setStyleSheet("color: #ef4444; font-size: 14px; font-weight: 500;")
        else:
            self.trend_label.setText("0%")
            self.trend_label.setStyleSheet("color: #9dabb9; font-size: 14px; font-weight: 500;")
    
    def update_move_counter(self, move_num: int):
        """Update the move counter."""
        self.move_counter.setText(f"Move {move_num}")
    
    def set_status(self, status: str, color: str = "#3b82f6"):
        """Set the status badge."""
        self.status_badge.setText(status)
        self.status_badge.setStyleSheet(f"""
            background-color: rgba({self._hex_to_rgb(color)}, 0.2);
            color: {color};
            border: 1px solid rgba({self._hex_to_rgb(color)}, 0.3);
            border-radius: 4px;
            padding: 4px 8px;
            font-size: 12px;
            font-weight: bold;
        """)
    
    def _hex_to_rgb(self, hex_color: str) -> str:
        """Convert hex color to RGB string."""
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        return f"{r}, {g}, {b}"
    
    def add_move_to_history(self, move_num: int, black_move: str, white_move: str, time_str: str):
        """Add a move to the history table."""
        row = self.history_table.rowCount()
        self.history_table.insertRow(row)
        
        self.history_table.setItem(row, 0, QTableWidgetItem(str(move_num)))
        self.history_table.setItem(row, 1, QTableWidgetItem(black_move))
        self.history_table.setItem(row, 2, QTableWidgetItem(white_move))
        self.history_table.setItem(row, 3, QTableWidgetItem(time_str))
        
        # Scroll to bottom
        self.history_table.scrollToBottom()
    
    def set_ai_message(self, message: str):
        """Set the AI message."""
        self.ai_message.setText(message)
    
    def update_chart(self, move_num: int, probability: float):
        """Update the win probability chart."""
        self.series.append(move_num, probability * 100)
        
        # Update x-axis range
        if move_num > 10:
            self.chart.axes(Qt.Orientation.Horizontal)[0].setRange(0, move_num)
