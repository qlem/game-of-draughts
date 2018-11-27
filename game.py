from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QWidget, QLabel, QGridLayout, QFrame, QVBoxLayout
from PyQt5.QtGui import QIcon, QImage, QPainter, QPen
from PyQt5.QtCore import Qt, QRect, QRectF
import sys
import logic


class VarsGame:
    def __init__(self, turn=logic.PlayerTurn.RED, score_red_player=0, score_white_player=0, game_over=False):
        self.turn = turn
        self.score_red_player = score_red_player
        self.score_white_player = score_white_player
        self.game_over = game_over


class PieceIndicator(QFrame):
    def __init__(self, parent=None, player=logic.PlayerTurn.RED):
        super().__init__(parent)

        self.player = player

        self.setFixedSize(100, 100)

        self.sprite_sheet = QImage(696, 154, QImage.Format_ARGB32_Premultiplied)
        self.sprite_sheet.load("./res/sprite_sheet.png")

    @staticmethod
    def get_targeted_rect(x, y):
        factor = 154 / 174
        scaled_w = 100 * 0.7
        scaled_h = scaled_w * factor
        x = x + 50 - scaled_w / 2
        y = y + 50 - scaled_h / 2
        return QRectF(x, y, scaled_w, scaled_h)

    def paintEvent(self, event):
        painter = QPainter(self)
        target = self.get_targeted_rect(0, 0)
        if self.player == logic.PlayerTurn.RED:
            painter.drawImage(target, self.sprite_sheet, QRectF(0, 0, 174, 154))
        else:
            painter.drawImage(target, self.sprite_sheet, QRectF(348, 0, 174, 154))
        pen = QPen(Qt.black, 6, Qt.SolidLine, Qt.FlatCap, Qt.MiterJoin)
        painter.setPen(pen)
        borders = QRect(0, 0, 100, 100)
        painter.drawRect(borders)


class InfoPlayerWidget(QWidget):
    def __init__(self, parent=None, player=logic.PlayerTurn.RED):
        super().__init__(parent)

        self.player = player

        piece_indicator = PieceIndicator(self, self.player)
        score_label = QLabel("score")
        self.score_value = QLabel("0")
        jumps_label = QLabel("jumps")
        self.jumps_value = QLabel("0")
        self.turn_label = QLabel("Your turn")

        score_label.setStyleSheet("font-size: 25px")
        self.score_value.setStyleSheet("font: bold; font-size: 30px")
        jumps_label.setStyleSheet("font-size: 25px")
        self.jumps_value.setStyleSheet("font: bold; font-size: 30px")
        self.turn_label.setStyleSheet("background: blue; color:white; font: bold; font-size: 30px; "
                                      "padding: 5px 10px 5px 10px;")

        layout = QGridLayout()
        layout.addWidget(piece_indicator, 0, 0, 1, 2)
        layout.addWidget(score_label, 1, 0, 1, 1)
        layout.addWidget(self.score_value, 1, 1, 1, 1)
        layout.addWidget(jumps_label, 2, 0, 1, 1)
        layout.addWidget(self.jumps_value, 2, 1, 1, 1)
        layout.addWidget(self.turn_label, 3, 0, 1, 2)
        layout.setAlignment(Qt.AlignLeft)
        self.setLayout(layout)

    def update_ui(self, v_game):
        if self.player == logic.PlayerTurn.RED:
            self.score_value.setText(str(v_game.score_red_player))
        else:
            self.score_value.setText(str(v_game.score_white_player))

        self.turn_label.hide()
        if v_game.game_over and self.player == logic.PlayerTurn.RED and \
                v_game.score_red_player > v_game.score_white_player or \
                v_game.game_over and self.player == logic.PlayerTurn.WHITE and \
                v_game.score_white_player > v_game.score_red_player:
            self.turn_label.setText("Winner")
            self.turn_label.show()
            return
        elif v_game.game_over and v_game.score_red_player == v_game.score_white_player:
            self.turn_label.setText("Draw")
            self.turn_label.show()
            return

        if self.player == logic.PlayerTurn.RED and v_game.turn == logic.PlayerTurn.RED or \
                self.player == logic.PlayerTurn.WHITE and v_game.turn == logic.PlayerTurn.WHITE:
            self.turn_label.show()


class GameBoardWidget(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.game = logic.Game(8, 8)

        self.BOARD_SIZE = 0
        self.CELL_SIZE = 0

        self.setMinimumSize(600, 600)

        self.sprite_sheet = QImage(696, 154, QImage.Format_ARGB32_Premultiplied)
        self.sprite_sheet.load("./res/sprite_sheet.png")

    def get_targeted_rect(self, x, y):
        factor = 154 / 174
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
                if self.game.Cells[i][j] == logic.CellState.RED_MAN:
                    painter.drawImage(target, self.sprite_sheet, QRectF(0, 0, 174, 154))
                elif self.game.Cells[i][j] == logic.CellState.RED_KING:
                    painter.drawImage(target, self.sprite_sheet, QRectF(174, 0, 174, 154))
                elif self.game.Cells[i][j] == logic.CellState.WHITE_MAN:
                    painter.drawImage(target, self.sprite_sheet, QRectF(348, 0, 174, 154))
                elif self.game.Cells[i][j] == logic.CellState.WHITE_KING:
                    painter.drawImage(target, self.sprite_sheet, QRectF(522, 0, 174, 154))

        pen = QPen(Qt.black, 6, Qt.SolidLine, Qt.FlatCap, Qt.MiterJoin)
        painter.setPen(pen)
        borders = QRect(0, 0, self.BOARD_SIZE, self.BOARD_SIZE)
        painter.drawRect(borders)

        if self.game.Selected:
            row = self.game.SelectedPawn.get("y")
            col = self.game.SelectedPawn.get("x")
            x = col * self.CELL_SIZE
            y = row * self.CELL_SIZE
            pen.setColor(Qt.yellow)
            painter.setPen(pen)
            borders.setRect(x, y, self.CELL_SIZE, self.CELL_SIZE)
            painter.drawRect(borders)

            for coordinates in self.game.PossibleMoves:
                target = self.get_targeted_rect(coordinates[0] * self.CELL_SIZE, coordinates[1] * self.CELL_SIZE)
                if self.game.Cells[row][col] == logic.CellState.RED_MAN:
                    painter.drawImage(target, self.sprite_sheet, QRectF(0, 154, 174, 154))
                elif self.game.Cells[row][col] == logic.CellState.RED_KING:
                    painter.drawImage(target, self.sprite_sheet, QRectF(174, 154, 174, 154))
                elif self.game.Cells[row][col] == logic.CellState.WHITE_MAN:
                    painter.drawImage(target, self.sprite_sheet, QRectF(348, 154, 174, 154))
                elif self.game.Cells[row][col] == logic.CellState.WHITE_KING:
                    painter.drawImage(target, self.sprite_sheet, QRectF(522, 154, 174, 154))

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
        self.parentWidget().update_ui(self.game.PlayerTurn, self.game.ScoreRed, self.game.ScoreWhite,
                                      self.game.GameOver)


class MainWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.v_game = VarsGame()

        self.game_board_widget = GameBoardWidget(self)
        self.red_player_widget = InfoPlayerWidget(self, logic.PlayerTurn.RED)
        self.white_player_widget = InfoPlayerWidget(self, logic.PlayerTurn.WHITE)
        self.white_player_widget.turn_label.hide()

        panel_layout = QVBoxLayout()
        panel_layout.addWidget(self.red_player_widget)
        panel_layout.addWidget(self.white_player_widget)

        layout = QGridLayout()
        layout.addWidget(self.game_board_widget, 0, 0, 1, 1)
        layout.addLayout(panel_layout, 0, 1, 1, 1, Qt.AlignTop)
        self.setLayout(layout)

    def update_ui(self, turn, score_red_pl, score_white_pl, game_over):
        self.v_game.turn = turn
        self.v_game.score_red_player = score_red_pl
        self.v_game.score_white_player = score_white_pl
        self.v_game.game_over = game_over
        self.red_player_widget.update_ui(self.v_game)
        self.white_player_widget.update_ui(self.v_game)


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Game of Draughts")

        self.central_widget = MainWidget(self)
        self.setCentralWidget(self.central_widget)

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
        return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec()
