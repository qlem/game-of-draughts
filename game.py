import sys
import os
from enum import Enum

class PlayerTurn(Enum):
    BLACK = 0
    WHITE = 1

class CellState(Enum):
    EMPTY = 0
    BLACK_MAN = 1
    BLACK_KING = 2
    WHITE_MAN = 3
    WHITE_KING = 4

class Game:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.Cells = [[CellState.EMPTY for i in range(y)] for j in range(x)]
        self.PlayerTurn = PlayerTurn.BLACK
        self.Clicks = 0

        self.InitializeBoard()

    """
    Initializes the board game depending on x and y board sizes.
    For now it only fills 3 lines of pawns for each player.
    """
    def InitializeBoard(self):
        w, h = 8, 8
        """
        Setting top pawns, Black player
        """
        for y in range(0, 3):
            if y % 2 == 0: start = 0
            else: start = 1
            for x in range(start, w, 2):
                self.Cells[y][x] = CellState.BLACK_MAN

        """
        Setting bottom pawns, White player
        """
        for y in range(h - 1, h - 4, -1):
            if y % 2 == 0: start = 0
            else: start = 1
            for x in range(start, w, 2):
                self.Cells[y][x] = CellState.WHITE_MAN
        self.PrintCells()

    """
    DEBUG Method : prints the board cells
    """
    def PrintCells(self):
        for x in self.Cells:
            print(x)


if __name__ == '__main__':
    app = Game(8, 8)
