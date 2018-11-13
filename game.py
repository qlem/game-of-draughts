from PyQt5.QtWidgets import QApplication, QMainWindow, QDockWidget, QAction, QFileDialog, QWidget, QLabel, \
    QPushButton, QColorDialog, QVBoxLayout, QGridLayout, QRadioButton, QButtonGroup, QSlider, QMessageBox
from PyQt5.QtGui import QIcon, QImage, QPainter, QPen, QColor
import sys
import os
from PyQt5.QtCore import Qt, QPoint
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


class GameBoardWidget(QWidget):
    def __init__(self):
        super().__init__()

        label = QLabel("game board")

        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)

        self.setStyleSheet("background: green")


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
