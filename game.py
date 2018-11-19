from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QWidget, QLabel, \
    QVBoxLayout, QGridLayout, QMessageBox, QFrame
from PyQt5.QtGui import QIcon, QImage, QPainter, QPen
from PyQt5.QtCore import Qt, QPoint, QRect, QRectF, QSize
import sys
import os
import logic


class PieceIndicator(QFrame):
    def __init__(self, parent=None, player=logic.PlayerTurn.BLACK):
        super().__init__(parent)

        self.player = player

        self.setFixedSize(100, 100)

        self.sprite_sheet = QImage(696, 154, QImage.Format_ARGB32_Premultiplied)
        self.sprite_sheet.load("./res/sprite_sheet.png")

    def paintEvent(self, event):
        painter = QPainter(self)
        target = QRect(15, 15, 70, 70)
        if self.player == logic.PlayerTurn.BLACK:
            painter.drawImage(target, self.sprite_sheet, QRect(0, 0, 174, 154))
        else:
            painter.drawImage(target, self.sprite_sheet, QRect(348, 0, 174, 154))
        pen = QPen(Qt.black, 6, Qt.SolidLine, Qt.FlatCap, Qt.MiterJoin)
        painter.setPen(pen)
        borders = QRect(0, 0, 100, 100)
        painter.drawRect(borders)


class Player1Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        piece_indicator = PieceIndicator(self, logic.PlayerTurn.BLACK)
        self.turn_label = QLabel("Your turn")
        score_label = QLabel("score:")
        self.score_value = QLabel("0")
        jumps_label = QLabel("jumps:")
        self.jumps_value = QLabel("0")

        layout = QGridLayout()
        layout.addWidget(piece_indicator, 0, 0, 1, 1)
        layout.addWidget(self.turn_label, 0, 1, 1, 1)
        layout.addWidget(score_label, 1, 0, 1, 1)
        layout.addWidget(self.score_value, 1, 1, 1, 1)
        layout.addWidget(jumps_label, 2, 0, 1, 1)
        layout.addWidget(self.jumps_value, 2, 1, 1, 1)
        self.setLayout(layout)

        self.setFixedSize(self.minimumSizeHint())

    def update_ui(self):
        # TODO
        return


class Player2Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        piece_indicator = PieceIndicator(self, logic.PlayerTurn.WHITE)
        self.turn_label = QLabel()
        score_label = QLabel("score:")
        self.score_value = QLabel("0")
        jumps_label = QLabel("jumps:")
        self.jumps_value = QLabel("0")

        layout = QGridLayout()
        layout.addWidget(piece_indicator, 0, 0, 1, 1)
        layout.addWidget(self.turn_label, 0, 1, 1, 1)
        layout.addWidget(score_label, 1, 0, 1, 1)
        layout.addWidget(self.score_value, 1, 1, 1, 1)
        layout.addWidget(jumps_label, 2, 0, 1, 1)
        layout.addWidget(self.jumps_value, 2, 1, 1, 1)
        self.setLayout(layout)

        self.setFixedSize(self.minimumSizeHint())

    def update_ui(self):
        # TODO
        return


class GameBoardWidget(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.game = logic.Game(8, 8)

        self.BOARD_SIZE = 0
        self.CELL_SIZE = 0

        self.setMinimumSize(600, 600)

        self.sprite_sheet = QImage(696, 154, QImage.Format_ARGB32_Premultiplied)
        self.sprite_sheet.load("./res/sprite_sheet.png")

    """
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
    """

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
                if self.game.Cells[i][j] == logic.CellState.BLACK_MAN:
                    painter.drawImage(target, self.sprite_sheet, QRectF(0, 0, 174, 154))
                elif self.game.Cells[i][j] == logic.CellState.WHITE_MAN:
                    painter.drawImage(target, self.sprite_sheet, QRectF(348, 0, 174, 154))
                elif self.game.Cells[i][j] == logic.CellState.BLACK_KING:
                    painter.drawImage(target, self.sprite_sheet, QRectF(174, 0, 174, 154))
                elif self.game.Cells[i][j] == logic.CellState.WHITE_KING:
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

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            col = int(event.x() / self.CELL_SIZE)
            row = int(event.y() / self.CELL_SIZE)
            self.game.ValidClick(col, row)
            self.update()
        # TODO update ui


class MainWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.game_board_widget = GameBoardWidget(self)
        self.player1_widget = Player1Widget(self)
        self.player2_widget = Player2Widget(self)

        layout = QGridLayout()
        layout.addWidget(self.game_board_widget, 0, 0, 2, 2)
        layout.addWidget(self.player1_widget, 0, 2, 1, 1)
        layout.addWidget(self.player2_widget, 1, 2, 1, 1)
        self.setLayout(layout)


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Game of Draughts")

        self.central_widget = MainWidget(self)
        self.setCentralWidget(self.central_widget)
        # self.central_widget.show()

        menu = self.menuBar()
        game_menu = menu.addMenu("Game")

        restart_action = QAction(QIcon("./res/restore.png"), "Restart", self)
        restart_action.setShortcut("Ctrl+R")
        game_menu.addAction(restart_action)
        restart_action.triggered.connect(self.restart_game)

        quit_action = QAction(QIcon("./res/exit.png"), "Quit", self)
        quit_action.setShortcut("Ctrl+Q")
        game_menu.addAction(quit_action)
        quit_action.triggered.connect(lambda: self.close())

    def restart_game(self):
        # TODO
        self.central_widget.update_ui()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec()
