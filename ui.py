from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QWidget, QLabel, QGridLayout, QFrame, QVBoxLayout, \
    QHBoxLayout
from PyQt5.QtGui import QIcon, QImage, QPainter, QPen
from PyQt5.QtCore import Qt, QRect, QRectF
import sys
import logic


# This class stores the variables of the current game.
class VarsGame:
    def __init__(self, turn=logic.PlayerTurn.RED, score_red_player=0, score_white_player=0, jump_red=0, jump_white=0,
                 game_over=False):
        self.turn = turn
        self.score_red_player = score_red_player
        self.score_white_player = score_white_player
        self.jump_red = jump_red
        self.jump_white = jump_white
        self.game_over = game_over


# This class defines a simple widget that displays the piece's picture that represents the player.
class PieceIndicator(QFrame):
    def __init__(self, parent=None, player=logic.PlayerTurn.RED):
        super().__init__(parent)

        # init the player
        self.player = player

        # init the size of the widget
        self.setFixedSize(140, 80)

        # init the sprite sheet that contains the resources
        self.sprite_sheet = QImage(696, 154, QImage.Format_ARGB32_Premultiplied)
        self.sprite_sheet.load("./res/sprite_sheet.png")

    # This function return the targeted area where the piece will be drawn.
    @staticmethod
    def get_targeted_rect(x, y):
        factor = 154 / 174
        scaled_w = 80 * 0.7
        scaled_h = scaled_w * factor
        x = x + 70 - scaled_w / 2
        y = y + 40 - scaled_h / 2
        return QRectF(x, y, scaled_w, scaled_h)

    # This function is called for draw the widget.
    def paintEvent(self, event):
        painter = QPainter(self)
        target = self.get_targeted_rect(0, 0)
        if self.player == logic.PlayerTurn.RED:
            painter.drawImage(target, self.sprite_sheet, QRectF(0, 0, 174, 154))
        else:
            painter.drawImage(target, self.sprite_sheet, QRectF(348, 0, 174, 154))
        pen = QPen(Qt.black, 4, Qt.SolidLine, Qt.FlatCap, Qt.MiterJoin)
        painter.setPen(pen)
        borders = QRect(0, 0, 140, 80)
        painter.drawRect(borders)


# This is the widget that displays the information about one player.
class InfoPlayerWidget(QWidget):
    def __init__(self, parent=None, player=logic.PlayerTurn.RED):
        super().__init__(parent)

        # init the player
        self.player = player

        # init the elements that compose the UI
        piece_indicator = PieceIndicator(self, self.player)
        score_label = QLabel("score")
        self.score_value = QLabel("0")
        jumps_label = QLabel("jumps")
        self.jumps_value = QLabel("0")
        self.turn_label = QLabel("Your turn")
        self.turn_label.setAlignment(Qt.AlignHCenter)

        # apply some styles
        score_label.setStyleSheet("font-size: 18px; font: bold; padding-left: 5px")
        self.score_value.setStyleSheet("font-size: 18px; font: bold; padding-right: 5px")
        jumps_label.setStyleSheet("font-size: 18px; font: bold; padding-left: 5px")
        self.jumps_value.setStyleSheet("font-size: 18px; font: bold; padding-right: 5px")
        self.turn_label.setStyleSheet("background: blue; color:white; font: bold; font-size: 22px; "
                                      "padding-top: 5px; padding-bottom: 5px")

        # init the layout
        layout = QGridLayout()
        layout.addWidget(piece_indicator, 0, 0, 1, 2)
        layout.addWidget(score_label, 1, 0, 1, 1)
        layout.addWidget(self.score_value, 1, 1, 1, 1, Qt.AlignRight)
        layout.addWidget(jumps_label, 2, 0, 1, 1)
        layout.addWidget(self.jumps_value, 2, 1, 1, 1, Qt.AlignRight)
        layout.addWidget(self.turn_label, 3, 0, 1, 2)
        layout.setAlignment(Qt.AlignTop)
        self.setLayout(layout)

        self.setFixedHeight(220)

    # This function is called for refresh the UI according to the passed game variables.
    def update_ui(self, v_game):

        # refresh the score and jumps values
        if self.player == logic.PlayerTurn.RED:
            self.score_value.setText(str(v_game.score_red_player))
            self.jumps_value.setText(str(v_game.jump_red))
        else:
            self.score_value.setText(str(v_game.score_white_player))
            self.jumps_value.setText(str(v_game.jump_white))

        # refresh the turn label
        self.turn_label.hide()
        if v_game.game_over and self.player == logic.PlayerTurn.RED and \
                v_game.score_red_player > v_game.score_white_player or \
                v_game.game_over and self.player == logic.PlayerTurn.WHITE and \
                v_game.score_white_player > v_game.score_red_player:
            self.turn_label.setText("Winner")
            self.turn_label.show()
        elif v_game.game_over and v_game.score_red_player == v_game.score_white_player:
            self.turn_label.setText("Draw")
            self.turn_label.show()
        elif not v_game.game_over:
            self.turn_label.setText("Your turn")
            if self.player == logic.PlayerTurn.RED and v_game.turn == logic.PlayerTurn.RED or \
                    self.player == logic.PlayerTurn.WHITE and v_game.turn == logic.PlayerTurn.WHITE:
                self.turn_label.show()


# This is the widget that displays the game board.
class GameBoardWidget(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        # init the logic of the game
        self.game = logic.Game(8, 8)

        # init some constants
        self.BOARD_SIZE = 0
        self.CELL_SIZE = 0

        # set the minimum size of the board
        self.setMinimumSize(600, 600)

        # init the sprite sheet that contains the resources
        self.sprite_sheet = QImage(696, 154, QImage.Format_ARGB32_Premultiplied)
        self.sprite_sheet.load("./res/sprite_sheet.png")

    # This function return the targeted area where a piece will be drawn.
    def get_targeted_rect(self, x, y):
        factor = 154 / 174
        scaled_w = self.CELL_SIZE * 0.7
        scaled_h = scaled_w * factor
        x = x + self.CELL_SIZE / 2 - scaled_w / 2
        y = y + self.CELL_SIZE / 2 - scaled_h / 2
        return QRectF(x, y, scaled_w, scaled_h)

    # This function draws the current state of the game board.
    def paintEvent(self, event):

        # init the painter
        painter = QPainter(self)

        # draw the game board by iterating the matrix
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

        # draw the borders of the game board
        pen = QPen(Qt.black, 6, Qt.SolidLine, Qt.FlatCap, Qt.MiterJoin)
        painter.setPen(pen)
        borders = QRect(0, 0, self.BOARD_SIZE, self.BOARD_SIZE)
        painter.drawRect(borders)

        # draw the highlighting for the selected piece
        if self.game.Selected:
            row = self.game.SelectedPawn.get("y")
            col = self.game.SelectedPawn.get("x")
            x = col * self.CELL_SIZE
            y = row * self.CELL_SIZE
            pen.setColor(Qt.yellow)
            painter.setPen(pen)
            borders.setRect(x, y, self.CELL_SIZE, self.CELL_SIZE)
            painter.drawRect(borders)

            # draw the pieces that represents the possible moves
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

    # This function is called when a resize event occur.
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

    # This Function is called when a click event occur. If the click is valid, updates the game logic,
    # redraws the game board and refresh the UI.
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            col = int(event.x() / self.CELL_SIZE)
            row = int(event.y() / self.CELL_SIZE)
            if self.game.ValidClick(col, row):
                self.update()
                self.parentWidget().update_ui(self.game.PlayerTurn, self.game.ScoreRed, self.game.ScoreWhite,
                                              self.game.JumpRed, self.game.JumpWhite, self.game.GameOver)


# This class initializes the main widget divided into 2 sub widgets : the game board widget and
# the panel widget that provides information about each player.
class MainWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # init the game vars
        self.v_game = VarsGame()

        # init the sub widgets
        self.game_board_widget = GameBoardWidget(self)
        game_panel_title = QLabel("Game Panel")
        game_panel_title.setStyleSheet("font-size: 20px; font: bold; margin-bottom: 10px")
        self.red_player_widget = InfoPlayerWidget(self, logic.PlayerTurn.RED)
        self.white_player_widget = InfoPlayerWidget(self, logic.PlayerTurn.WHITE)
        self.white_player_widget.turn_label.hide()

        # init the game panel widget that provides some information about the current game
        panel_widget = QWidget()
        panel_widget.setStyleSheet("background-color: #c4c4c4")
        panel_layout = QVBoxLayout()
        panel_layout.addWidget(game_panel_title)
        panel_layout.addWidget(self.red_player_widget)
        panel_layout.addWidget(self.white_player_widget)
        panel_layout.setAlignment(Qt.AlignTop)
        panel_widget.setLayout(panel_layout)
        panel_widget.setFixedWidth(190)

        # init the layout of the main widget
        layout = QHBoxLayout()
        layout.addWidget(panel_widget, Qt.AlignLeft)
        layout.addWidget(self.game_board_widget)
        self.setLayout(layout)

    # This function is called for update the players widgets.
    def update_ui(self, turn, score_red_pl, score_white_pl, jump_red, jump_white, game_over):
        self.v_game.turn = turn
        self.v_game.score_red_player = score_red_pl
        self.v_game.score_white_player = score_white_pl
        self.v_game.jump_red = jump_red
        self.v_game.jump_white = jump_white
        self.v_game.game_over = game_over
        self.red_player_widget.update_ui(self.v_game)
        self.white_player_widget.update_ui(self.v_game)


# This class initializes the window of the game.
class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        # set the title of the window
        self.setWindowTitle("Game of Draughts")

        # set the main widget of the window
        self.central_widget = MainWidget(self)
        self.setCentralWidget(self.central_widget)

        # init the menu
        menu = self.menuBar()
        game_menu = menu.addMenu("Game")

        # action for restart the game
        restart_action = QAction(QIcon("./res/restore.png"), "Restart", self)
        restart_action.setShortcut("Ctrl+R")
        game_menu.addAction(restart_action)
        restart_action.triggered.connect(self.restart_game)

        # action for quit the game
        quit_action = QAction(QIcon("./res/exit.png"), "Quit", self)
        quit_action.setShortcut("Ctrl+Q")
        game_menu.addAction(quit_action)
        quit_action.triggered.connect(lambda: self.close())

    # This function restart the game.
    def restart_game(self):
        self.central_widget.game_board_widget.game = logic.Game(8, 8)
        self.central_widget.update_ui(logic.PlayerTurn.RED, 0, 0, 0, 0, False)
        self.central_widget.update()
        return


# Entry point of the game.
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec()
