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
        self.Selected = False
        self.SelectedPawn = dict([("x", 0), ("y", 0)])
        self.InitializeBoard()

    """
    Initializes the board game depending on x and y board sizes
    For now it only fills 3 lines of pawns for each player
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
    Verifies if a click is valid
    """
    def ValidClick(self, x, y):
        # If the user click on its own color, we select the pawn
        if (self.Cells[y][x] == CellState.BLACK_KING or self.Cells[y][x] == CellState.BLACK_MAN\
                and self.PlayerTurn == PlayerTurn.BLACK) or\
            (self.Cells[y][x] == CellState.WHITE_KING or self.Cells[y][x] == CellState.WHITE_MAN\
                and self.PlayerTurn == PlayerTurn.WHITE):
            self.SelectedPawn["x"] = int(x)
            self.SelectedPawn["y"] = int(y)
            self.Selected = True
            # Informs if White or Black selected
            if self.PlayerTurn == PlayerTurn.WHITE:
                print("White player selected x:" + str(self.SelectedPawn["x"]) + " y:" + str(self.SelectedPawn["y"]))
            elif self.PlayerTurn == PlayerTurn.BLACK:
                print("Black player selected x:" + str(self.SelectedPawn["x"]) + " y:" + str(self.SelectedPawn["y"]))
            return True

        # If a pawn is selected already
        if self.Selected:
            # Verifies if the second click is doable and performs it
            if self.PerformMove(x, y):
                if self.PlayerTurn == PlayerTurn.BLACK:
                    self.PlayerTurn = PlayerTurn.WHITE
                else:
                    self.PlayerTurn = PlayerTurn.BLACK
                self.Selected = False
                return True
            else:
                print("Impossible move")
                return False
        else:
            print("Wrong selection")
            return False

    """
    Defines if a move is possible
    """
    def PerformMove(self, x, y):
        # Moves the selected pawn to the new location
        self.Cells[y][x] = self.Cells[self.SelectedPawn["y"]][self.SelectedPawn["x"]]
        self.Cells[self.SelectedPawn["y"]][self.SelectedPawn["x"]] = CellState.EMPTY
        print("Move made at " + x + ";" + y)
        return True


    """
    DEBUG Method : prints the board cells differently for visibility
    """
    def PrintCells(self):
        for y in self.Cells:
            for x in y:
                BLACK_MAN = 1
                BLACK_KING = 2
                WHITE_MAN = 3
                WHITE_KING = 4
                if x == CellState.EMPTY: print(0, end='')
                elif x == CellState.BLACK_MAN: print(1, end='')
                elif x == CellState.BLACK_KING: print(2, end='')
                elif x == CellState.WHITE_MAN: print(3, end='')
                elif x == CellState.WHITE_KING: print(4, end='')
            print("\n")


if __name__ == '__main__':
    app = Game(8, 8)
