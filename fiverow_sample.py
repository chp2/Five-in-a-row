import sys
import numpy as np
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox
from PyQt6.QtGui import QPainter, QPen, QColor, QBrush
from PyQt6.QtCore import Qt

class OmokBoard(QWidget):
    def __init__(self):
        super().__init__()
        self.board_size = 15
        self.grid_size = 40  # 격자 간격 (픽셀)
        self.margin = 30     # 여백
        # 0: 빈칸, 1: 흑, 2: 백
        self.board_state = np.zeros((self.board_size, self.board_size), dtype=int)
        self.current_turn = 1 # 1: 흑 차례, 2: 백 차례

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # 1. 배경 그리기 (나무 색상)
        painter.fillRect(self.rect(), QColor(220, 179, 92))

        # 2. 격자 그리기
        pen = QPen(Qt.GlobalColor.black, 1)
        painter.setPen(pen)
        for i in range(self.board_size):
            # 가로선
            start_x = self.margin
            end_x = self.margin + (self.board_size - 1) * self.grid_size
            y = self.margin + i * self.grid_size
            painter.drawLine(start_x, y, end_x, y)
            
            # 세로선
            start_y = self.margin
            end_y = self.margin + (self.board_size - 1) * self.grid_size
            x = self.margin + i * self.grid_size
            painter.drawLine(x, start_y, x, end_y)

        # 3. 돌 그리기
        for y in range(self.board_size):
            for x in range(self.board_size):
                if self.board_state[y][x] != 0:
                    center_x = self.margin + x * self.grid_size
                    center_y = self.margin + y * self.grid_size
                    radius = self.grid_size // 2 - 2
                    
                    if self.board_state[y][x] == 1:
                        painter.setBrush(QBrush(Qt.GlobalColor.black)) # 흑돌
                    else:
                        painter.setBrush(QBrush(Qt.GlobalColor.white)) # 백돌
                    
                    painter.drawEllipse(center_x - radius, center_y - radius, radius * 2, radius * 2)

    def mousePressEvent(self, event):
        # 마우스 클릭 좌표를 보드 좌표로 변환
        x = round((event.position().x() - self.margin) / self.grid_size)
        y = round((event.position().y() - self.margin) / self.grid_size)

        # 범위 내이고 빈 칸일 때만 착수
        if 0 <= x < self.board_size and 0 <= y < self.board_size:
            if self.board_state[y][x] == 0:
                self.board_state[y][x] = self.current_turn
                
                # 차례 변경 (1 -> 2 -> 1)
                self.current_turn = 3 - self.current_turn
                
                # 화면 갱신 요청 (paintEvent 다시 호출)
                self.update()
                
                # (여기에 나중에 AI 분석 요청 코드를 넣으면 됨!)
                print(f"착수: ({x}, {y}) / 다음 차례: {'흑' if self.current_turn == 1 else '백'}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Omok Lab - Agent A.I")
        self.setGeometry(100, 100, 650, 650)
        self.setCentralWidget(OmokBoard())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())