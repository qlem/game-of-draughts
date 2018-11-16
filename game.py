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
        self.ScoreBlack = 0
        self.ScoreWhite = 0
        self.Selected = False
        self.SelectedPawn = dict([("x", 0), ("y", 0)])
        self.InitializeBoard()

        self.RunTest()


    def RunTest(self):
        self.PrintCells()
        self.ValidClick(0, 2)
        self.ValidClick(1, 3)
        self.PrintCells()

        self.ValidClick(1, 3)
        self.ValidClick(0, 2)

        self.ValidClick(3, 5)
        self.ValidClick(2, 4)
        self.PrintCells()

        self.ValidClick(1, 3)
        self.ValidClick(3, 5)
        self.PrintCells()


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

    """
    Verifies if a click is valid
    """
    def ValidClick(self, x, y):
        # If the user click on its own color, we select the pawn
        if ((self.Cells[y][x] == CellState.BLACK_KING or self.Cells[y][x] == CellState.BLACK_MAN)\
                and self.PlayerTurn == PlayerTurn.BLACK) or\
            ((self.Cells[y][x] == CellState.WHITE_KING or self.Cells[y][x] == CellState.WHITE_MAN)\
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
                return True
            else:
                print("Impossible move")
                return False
        else:
            print("Wrong selection")
            return False

    def Move(self, x, y):
        # Moves the selected pawn to the new location
        self.Cells[y][x] = self.Cells[self.SelectedPawn["y"]][self.SelectedPawn["x"]]
        self.Cells[self.SelectedPawn["y"]][self.SelectedPawn["x"]] = CellState.EMPTY
        print("Move made at " + str(x) + ";" + str(y))

    """
    Verifies if the selected man can move at the clicked position
    """
    def PerformManMove(self, x, y):
        # If the destination is one cell away
        if abs(x - self.SelectedPawn["x"]) == 1 and \
                abs(y - self.SelectedPawn["y"]) == 1 and \
                self.Cells[y][x] == CellState.EMPTY:
            self.Move(x, y)
            if self.PlayerTurn == PlayerTurn.BLACK:
                self.PlayerTurn = PlayerTurn.WHITE
            else:
                self.PlayerTurn = PlayerTurn.BLACK
            self.Selected = False
            return True
        # If the destination is two cells away
        elif abs(x - self.SelectedPawn["x"]) == 2 and \
                abs(y - self.SelectedPawn["y"]) == 2 and \
                self.Cells[y][x] == CellState.EMPTY:
            if x + 2 == self.SelectedPawn["x"] and y + 2 == self.SelectedPawn["y"]:
                # Down Right
                if (self.Cells[y + 1][x + 1] == CellState.WHITE_KING or self.Cells[y + 1][x + 1] == CellState.WHITE_MAN)\
                    and self.PlayerTurn == PlayerTurn.BLACK:
                    print("Black player ate a White pawn")
                    self.ScoreBlack += 1
                    self.Cells[y + 1][x + 1] = CellState.EMPTY
                    self.Move(x, y)
                    return True
                elif (self.Cells[y + 1][x + 1] == CellState.BLACK_KING or self.Cells[y + 1][x + 1] == CellState.BLACK_MAN)\
                    and self.PlayerTurn == PlayerTurn.WHITE:
                    print("White player ate a Black pawn")
                    self.ScoreWhite += 1
                    self.Cells[y + 1][x + 1] = CellState.EMPTY
                    self.Move(x, y)
                    return True
                else:
                    return False
            elif x + 2 == self.SelectedPawn["x"] and y - 2 == self.SelectedPawn["y"]:
                # Top Right
                if (self.Cells[y - 1][x + 1] == CellState.WHITE_KING or self.Cells[y - 1][x + 1] == CellState.WHITE_MAN)\
                    and self.PlayerTurn == PlayerTurn.BLACK:
                    print("Black player ate a White pawn")
                    self.ScoreBlack += 1
                    self.Cells[y - 1][x + 1] = CellState.EMPTY
                    self.Move(x, y)
                    return True
                elif (self.Cells[y - 1][x + 1] == CellState.BLACK_KING or self.Cells[y - 1][x + 1] == CellState.BLACK_MAN)\
                    and self.PlayerTurn == PlayerTurn.WHITE:
                    print("White player ate a Black pawn")
                    self.ScoreWhite += 1
                    self.Cells[y - 1][x + 1] = CellState.EMPTY
                    self.Move(x, y)
                    return True
                else:
                    return False
            elif x - 2 == self.SelectedPawn["x"] and y + 2 == self.SelectedPawn["y"]:
                # Down Left
                if (self.Cells[y + 1][x - 1] == CellState.WHITE_KING or self.Cells[y + 1][x - 1] == CellState.WHITE_MAN)\
                    and self.PlayerTurn == PlayerTurn.BLACK:
                    print("Black player ate a White pawn")
                    self.ScoreBlack += 1
                    self.Cells[y + 1][x - 1] = CellState.EMPTY
                    self.Move(x, y)
                    return True
                elif (self.Cells[y + 1][x + 1] == CellState.BLACK_KING or self.Cells[y + 1][x - 1] == CellState.BLACK_MAN)\
                    and self.PlayerTurn == PlayerTurn.WHITE:
                    print("White player ate a Black pawn")
                    self.ScoreWhite += 1
                    self.Cells[y + 1][x - 1] = CellState.EMPTY
                    self.Move(x, y)
                    return True
                else:
                    return False
            elif x - 2 == self.SelectedPawn["x"] and y - 2 == self.SelectedPawn["y"]:
                # Top Left
                if (self.Cells[y - 1][x - 1] == CellState.WHITE_KING or self.Cells[y - 1][x - 1] == CellState.WHITE_MAN)\
                    and self.PlayerTurn == PlayerTurn.BLACK:
                    print("Black player ate a White pawn")
                    self.ScoreBlack += 1
                    self.Cells[y - 1][x - 1] = CellState.EMPTY
                    self.Move(x, y)
                    return True
                elif (self.Cells[y - 1][x - 1] == CellState.BLACK_KING or self.Cells[y - 1][x - 1] == CellState.BLACK_MAN)\
                    and self.PlayerTurn == PlayerTurn.WHITE:
                    print("White player ate a Black pawn")
                    self.ScoreWhite += 1
                    self.Cells[y - 1][x - 1] = CellState.EMPTY
                    self.Move(x, y)
                    return True
                else:
                    return False
        return False

    """
    Verifies if the selected king can move at the clicked position
    """
    def PerformKingMove(self, x, y):
        # Moves the selected pawn to the new location
        self.Cells[y][x] = self.Cells[self.SelectedPawn["y"]][self.SelectedPawn["x"]]
        self.Cells[self.SelectedPawn["y"]][self.SelectedPawn["x"]] = CellState.EMPTY
        print("Move made at " + x + ";" + y)
        return True

    """
    Defines if a move is possible
    """
    def PerformMove(self, x, y):
        # If the pawn is a man
        if self.Cells[self.SelectedPawn["y"]][self.SelectedPawn["x"]] == CellState.WHITE_MAN or \
                self.Cells[self.SelectedPawn["y"]][self.SelectedPawn["x"]] == CellState.BLACK_MAN:
            return self.PerformManMove(x, y)
        # If the pawn is a king
        elif self.Cells[self.SelectedPawn["y"]][self.SelectedPawn["x"]] == CellState.WHITE_KING or \
                self.Cells[self.SelectedPawn["y"]][self.SelectedPawn["x"]] == CellState.BLACK_KING:
            return self.PerformKingMove(x, y)
        return False


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
            print("\n", end='')


if __name__ == '__main__':
    app = Game(8, 8)
