from PyQt5.QtWidgets import QApplication, QMainWindow, QDockWidget, QAction, QFileDialog, QWidget, QLabel, \
    QPushButton, QColorDialog, QVBoxLayout, QGridLayout, QRadioButton, QButtonGroup, QSlider, QMessageBox, QFrame
from PyQt5.QtGui import QIcon, QImage, QPainter, QPen, QColor
import sys
import os
from PyQt5.QtCore import Qt, QPoint, QRect, QRectF
from enum import Enum


class CellState(Enum):
    EMPTY = 0
    BLACK = 1
    WHITE = 2


class Player1Widget(QWidget):
    def __init__(self):
        super().__init__()

        label = QLabel("player 1")

        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)

        self.setStyleSheet("background: red")


class Player2Widget(QWidget):
    def __init__(self):
        super().__init__()

        label = QLabel("player 2")

        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)

        self.setStyleSheet("background: blue")


class GameBoardWidget(QFrame):
    def __init__(self):
        super().__init__()

        self.BOARD_SIZE = 0
        self.CELL_SIZE = 0

    def draw_board(self):
        painter = QPainter(self)

        pen = QPen(Qt.black, 6, Qt.SolidLine, Qt.FlatCap, Qt.MiterJoin)
        painter.setPen(pen)
        painter.drawLine(0, 0, self.BOARD_SIZE, 0)
        painter.drawLine(self.BOARD_SIZE, 0, self.BOARD_SIZE, self.BOARD_SIZE)
        painter.drawLine(self.BOARD_SIZE, self.BOARD_SIZE, 0, self.BOARD_SIZE)
        painter.drawLine(0, 0, 0, self.BOARD_SIZE)

        for i in range(8):
            for j in range(8):
                x = j * self.CELL_SIZE
                y = i * self.CELL_SIZE
                if i % 2 == 0 and j % 2 > 0:
                    painter.fillRect(x, y, self.CELL_SIZE, self.CELL_SIZE, Qt.black)
                elif i % 2 > 0 and j % 2 == 0:
                    painter.fillRect(x, y, self.CELL_SIZE, self.CELL_SIZE, Qt.black)

    def paintEvent(self, event):
        print("paint event")
        self.draw_board()

    def resizeEvent(self, event):
        print("resize event")
        size = 0
        if self.width() <= self.height():
            size = self.width()
            self.resize(self.width(), self.width())
        elif self.width() > self.height():
            size = self.height()
            self.resize(self.height(), self.height())
        self.BOARD_SIZE = size
        self.CELL_SIZE = size / 8


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.game_board_widget = GameBoardWidget()
        self.player1_widget = Player1Widget()
        self.player2_widget = Player2Widget()

        layout = QGridLayout()
        layout.addWidget(self.game_board_widget, 0, 0, 2, 2)
        layout.addWidget(self.player1_widget, 0, 2, 1, 1)
        layout.addWidget(self.player2_widget, 1, 2, 1, 1)
        self.setLayout(layout)


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        top = 400
        left = 400
        width = 1280
        height = 720
        self.setWindowTitle("Game of Draughts")
        self.setGeometry(left, top, width, height)

        self.central_widget = MainWidget()
        self.setCentralWidget(self.central_widget)
        # self.central_widget.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec()

    """
        def __init__(self, parent=None):
            super(MainWidget, self).__init__(parent)
    """
