from PyQt5.QtWidgets import QApplication, QMainWindow, QDockWidget, QAction, QFileDialog, QWidget, QLabel, \
    QPushButton, QColorDialog, QVBoxLayout, QGridLayout, QRadioButton, QButtonGroup, QSlider, QMessageBox, QFrame
from PyQt5.QtGui import QIcon, QImage, QPainter, QPen, QColor
import sys
import os
from PyQt5.QtCore import Qt, QPoint, QRect, QRectF, QSize
from enum import Enum


class Cell(Enum):
    EMPTY = 0
    RED = 1
    WHITE = 2
    RED_KING = 3
    WHITE_KING = 4


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
        self.matrix = []

        self.init_matrix()

        self.sprite_sheet = QImage(696, 154, QImage.Format_ARGB32_Premultiplied)
        self.sprite_sheet.load("./res/sprite_sheet.png")

    def init_matrix(self):
        for i in range(8):
            self.matrix.append([])
            for j in range(8):
                self.matrix[i].append(Cell.EMPTY)
                if i % 2 == 0 and j % 2 > 0 or i % 2 > 0 and j % 2 == 0:
                    if i < 3:
                        self.matrix[i][j] = Cell.RED
                    elif i > 4:
                        self.matrix[i][j] = Cell.WHITE

    def get_targeted_rect(self, x, y):
        factor = 132 / 144
        scaled_w = self.CELL_SIZE * 0.7
        scaled_h = scaled_w * factor
        x = x + self.CELL_SIZE / 2 - scaled_w / 2
        y = y + self.CELL_SIZE / 2 - scaled_h / 2
        return QRectF(x, y, scaled_w, scaled_h)

    def draw_board(self):
        painter = QPainter(self)

        for i in range(8):
            for j in range(8):
                x = j * self.CELL_SIZE
                y = i * self.CELL_SIZE
                target = self.get_targeted_rect(x, y)
                if i % 2 == 0 and j % 2 > 0 or i % 2 > 0 and j % 2 == 0:
                    painter.fillRect(x, y, self.CELL_SIZE, self.CELL_SIZE, Qt.darkGreen)
                elif i % 2 == 0 and j % 2 == 0 or i % 2 > 0 and j % 2 > 0:
                    painter.fillRect(x, y, self.CELL_SIZE, self.CELL_SIZE, Qt.lightGray)
                if self.matrix[i][j] == Cell.RED:
                    painter.drawImage(target, self.sprite_sheet, QRectF(0, 0, 174, 154))
                elif self.matrix[i][j] == Cell.WHITE:
                    painter.drawImage(target, self.sprite_sheet, QRectF(348, 0, 174, 154))
                elif self.matrix[i][j] == Cell.RED_KING:
                    painter.drawImage(target, self.sprite_sheet, QRectF(174, 0, 174, 154))
                elif self.matrix[i][j] == Cell.WHITE_KING:
                    painter.drawImage(target, self.sprite_sheet, QRectF(522, 0, 174, 154))

        pen = QPen(Qt.black, 6, Qt.SolidLine, Qt.FlatCap, Qt.MiterJoin)
        painter.setPen(pen)
        borders = QRect(0, 0, self.BOARD_SIZE, self.BOARD_SIZE)
        painter.drawRect(borders)

    def paintEvent(self, event):
        self.draw_board()

    def resizeEvent(self, event):
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
