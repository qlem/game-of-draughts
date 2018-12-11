from enum import Enum

"""
Defines which turn it is
"""
class PlayerTurn(Enum):
    RED = 0
    WHITE = 1

"""
Defines a cell 
"""
class CellState(Enum):
    EMPTY = 0
    RED_MAN = 1
    RED_KING = 2
    WHITE_MAN = 3
    WHITE_KING = 4

"""
Defines the game logic
Initialize the game class and call ValidClick(x,y)
"""
class Game:
    def __init__(self, x, y):
        # x and y are the size of our board
        self.x = x
        self.y = y
        # Represents the board cells
        self.Cells = []
        # Sets the actual turn
        self.PlayerTurn = PlayerTurn.RED
        # Scores
        self.ScoreRed = 0
        self.ScoreWhite = 0
        # How many jumps each player performed
        self.JumpRed = 0
        self.JumpWhite = 0
        # Defines if a pawn is currently selected
        self.Selected = False
        # Defines if a pawn is capturing
        self.Capturing = False
        # Defines the positions of the selected pawn
        self.SelectedPawn = dict([("x", 0), ("y", 0)])
        # Contains the positions a player can play
        self.PossibleMoves = []
        # Sets the end of the game
        self.GameOver = False

        # Calls the function which initializes the board
        self.InitializeBoard()

    """
    Initializes the board game depending on x and y board sizes
    For now it only fills 3 lines of pawns for each player
    """
    def InitializeBoard(self):
        for i in range(8):
            self.Cells.append([])
            for j in range(8):
                self.Cells[i].append(CellState.EMPTY)
                if i % 2 == 0 and j % 2 > 0 or i % 2 > 0 and j % 2 == 0:
                    if i < 3:
                        self.Cells[i][j] = CellState.RED_MAN
                    elif i > 4:
                        self.Cells[i][j] = CellState.WHITE_MAN

    """
    Changes the current turn   
    """
    def ChangeTurn(self):
        if self.PlayerTurn == PlayerTurn.RED:
            self.PlayerTurn = PlayerTurn.WHITE
        else:
            self.PlayerTurn = PlayerTurn.RED

    """
    Verifies if a click is valid
    Performs actions depending on saved variables such as the selected pawn
    """
    def ValidClick(self, x, y):
        # If the user click on its own color, we select the pawn
        if (((self.Cells[y][x] == CellState.RED_KING or self.Cells[y][x] == CellState.RED_MAN) \
            and self.PlayerTurn == PlayerTurn.RED and (self.Capturing == False)) or \
                ((self.Cells[y][x] == CellState.WHITE_KING or self.Cells[y][x] == CellState.WHITE_MAN) \
                 and self.PlayerTurn == PlayerTurn.WHITE) and (self.Capturing == False)):
            self.SelectedPawn["x"] = int(x)
            self.SelectedPawn["y"] = int(y)
            self.Selected = True
            self.GetPossibleMoves()
            # Informs if White or Black selected
            if self.PlayerTurn == PlayerTurn.WHITE:
                print("White player selected x:" + str(self.SelectedPawn["x"]) + " y:" + str(self.SelectedPawn["y"]))
            elif self.PlayerTurn == PlayerTurn.RED:
                print("Black player selected x:" + str(self.SelectedPawn["x"]) + " y:" + str(self.SelectedPawn["y"]))
            return True

        # If a pawn is selected already
        if self.Selected:
            # Verifies if the second click is doable and performs it
            if self.PerformMove(x, y):
                # Cleans possible moves
                if not self.Capturing:
                    self.PossibleMoves = []
                # Verifies if the game is over
                if self.ScoreWhite == 12 or self.ScoreRed == 12:
                    self.GameOver = True
                # Verifies if the pawn becomes a king and increments the jump
                if self.PlayerTurn == PlayerTurn.WHITE:
                    self.JumpRed += 1
                    if y == self.y - 1:
                        self.Cells[y][x] = CellState.RED_KING
                elif self.PlayerTurn == PlayerTurn.RED:
                    self.JumpWhite += 1
                    if y == 0:
                        self.Cells[y][x] = CellState.WHITE_KING
                return True
            else:
                print("Impossible move")
                return False
        else:
            print("Wrong selection")
            return False

    """
    Method which moves the selected pawn to the coordinates
    """
    def Move(self, x, y):
        # Moves the selected pawn to the new location
        self.Cells[y][x] = self.Cells[self.SelectedPawn["y"]][self.SelectedPawn["x"]]
        self.Cells[self.SelectedPawn["y"]][self.SelectedPawn["x"]] = CellState.EMPTY
        print("Move made at " + str(x) + ";" + str(y))

    """
    Retrieves possible moves from the selected man
    """
    def GetManMoves(self):
        # Verifies 1 block away
        if (self.SelectedPawn["y"] + 1 < self.y and self.SelectedPawn["x"] + 1 < self.x) \
                and self.Cells[self.SelectedPawn["y"] + 1][self.SelectedPawn["x"] + 1] == CellState.EMPTY \
                and self.PlayerTurn == PlayerTurn.RED:
            self.PossibleMoves.append((self.SelectedPawn["x"] + 1, self.SelectedPawn["y"] + 1))
        if (self.SelectedPawn["y"] + 1 < self.y and self.SelectedPawn["x"] - 1 >= 0) \
                and self.Cells[self.SelectedPawn["y"] + 1][self.SelectedPawn["x"] - 1] == CellState.EMPTY \
                and self.PlayerTurn == PlayerTurn.RED:
            self.PossibleMoves.append((self.SelectedPawn["x"] - 1, self.SelectedPawn["y"] + 1))
        if (self.SelectedPawn["y"] - 1 >= 0 and self.SelectedPawn["x"] + 1 < self.x) \
                and self.Cells[self.SelectedPawn["y"] - 1][self.SelectedPawn["x"] + 1] == CellState.EMPTY \
                and self.PlayerTurn == PlayerTurn.WHITE:
            self.PossibleMoves.append((self.SelectedPawn["x"] + 1, self.SelectedPawn["y"] - 1))
        if (self.SelectedPawn["y"] - 1 >= 0 and self.SelectedPawn["x"] - 1 >= 0) \
                and self.Cells[self.SelectedPawn["y"] - 1][self.SelectedPawn["x"] - 1] == CellState.EMPTY \
                and self.PlayerTurn == PlayerTurn.WHITE:
            self.PossibleMoves.append((self.SelectedPawn["x"] - 1, self.SelectedPawn["y"] - 1))

        # Verifies if the man can capture another pawn
        if (self.SelectedPawn["y"] + 2 < self.y and self.SelectedPawn["x"] + 2 < self.x) \
                and self.Cells[self.SelectedPawn["y"] + 2][self.SelectedPawn["x"] + 2] == CellState.EMPTY \
                and (self.Cells[self.SelectedPawn["y"] + 1][self.SelectedPawn["x"] + 1] == CellState.WHITE_MAN
                     or self.Cells[self.SelectedPawn["y"] + 1][self.SelectedPawn["x"] + 1] == CellState.WHITE_KING) \
                and self.PlayerTurn == PlayerTurn.RED:
            self.PossibleMoves.append((self.SelectedPawn["x"] + 2, self.SelectedPawn["y"] + 2))

        if (self.SelectedPawn["y"] + 2 < self.y and self.SelectedPawn["x"] - 2 >= 0) \
                and self.Cells[self.SelectedPawn["y"] + 2][self.SelectedPawn["x"] - 2] == CellState.EMPTY \
                and (self.Cells[self.SelectedPawn["y"] + 1][self.SelectedPawn["x"] - 1] == CellState.WHITE_MAN
                     or self.Cells[self.SelectedPawn["y"] + 1][self.SelectedPawn["x"] - 1] == CellState.WHITE_KING) \
                and self.PlayerTurn == PlayerTurn.RED:
            self.PossibleMoves.append((self.SelectedPawn["x"] - 2, self.SelectedPawn["y"] + 2))

        if (self.SelectedPawn["y"] - 2 >= 0 and self.SelectedPawn["x"] + 2 < self.x) \
                and self.Cells[self.SelectedPawn["y"] - 2][self.SelectedPawn["x"] + 2] == CellState.EMPTY \
                and (self.Cells[self.SelectedPawn["y"] - 1][self.SelectedPawn["x"] + 1] == CellState.RED_MAN
                     or self.Cells[self.SelectedPawn["y"] - 1][self.SelectedPawn["x"] + 1] == CellState.RED_KING) \
                and self.PlayerTurn == PlayerTurn.WHITE:
            self.PossibleMoves.append((self.SelectedPawn["x"] + 2, self.SelectedPawn["y"] - 2))

        if (self.SelectedPawn["y"] - 2 >= 0 and self.SelectedPawn["x"] - 2 >= 0) \
                and self.Cells[self.SelectedPawn["y"] - 2][self.SelectedPawn["x"] - 2] == CellState.EMPTY \
                and (self.Cells[self.SelectedPawn["y"] - 1][self.SelectedPawn["x"] - 1] == CellState.RED_MAN
                     or self.Cells[self.SelectedPawn["y"] - 1][self.SelectedPawn["x"] - 1] == CellState.RED_KING) \
                and self.PlayerTurn == PlayerTurn.WHITE:
            self.PossibleMoves.append((self.SelectedPawn["x"] - 2, self.SelectedPawn["y"] - 2))

    """
    Retrieves possible moves from the selected king
    """
    def GetKingMoves(self):
        print("get king moves")
        # Verifies 1 block away
        if (self.SelectedPawn["y"] + 1 < self.y and self.SelectedPawn["x"] + 1 < self.x) \
                and self.Cells[self.SelectedPawn["y"] + 1][self.SelectedPawn["x"] + 1] == CellState.EMPTY:
            self.PossibleMoves.append((self.SelectedPawn["x"] + 1, self.SelectedPawn["y"] + 1))
        if (self.SelectedPawn["y"] + 1 < self.y and self.SelectedPawn["x"] - 1 >= 0) \
                and self.Cells[self.SelectedPawn["y"] + 1][self.SelectedPawn["x"] - 1] == CellState.EMPTY:
            self.PossibleMoves.append((self.SelectedPawn["x"] - 1, self.SelectedPawn["y"] + 1))
        if (self.SelectedPawn["y"] - 1 >= 0 and self.SelectedPawn["x"] + 1 < self.x) \
                and self.Cells[self.SelectedPawn["y"] - 1][self.SelectedPawn["x"] + 1] == CellState.EMPTY:
            self.PossibleMoves.append((self.SelectedPawn["x"] + 1, self.SelectedPawn["y"] - 1))
        if (self.SelectedPawn["y"] - 1 >= 0 and self.SelectedPawn["x"] - 1 >= 0) \
                and self.Cells[self.SelectedPawn["y"] - 1][self.SelectedPawn["x"] - 1] == CellState.EMPTY:
            self.PossibleMoves.append((self.SelectedPawn["x"] - 1, self.SelectedPawn["y"] - 1))

        # Verifies if the King can capture another pawn
        if (self.SelectedPawn["y"] + 2 < self.y and self.SelectedPawn["x"] + 2 < self.x) \
                and self.Cells[self.SelectedPawn["y"] + 2][self.SelectedPawn["x"] + 2] == CellState.EMPTY \
                and (((self.Cells[self.SelectedPawn["y"] + 1][self.SelectedPawn["x"] + 1] == CellState.WHITE_MAN
                       or self.Cells[self.SelectedPawn["y"] + 1][self.SelectedPawn["x"] + 1] == CellState.WHITE_KING)
                      and self.PlayerTurn == PlayerTurn.RED)
                     or ((self.Cells[self.SelectedPawn["y"] + 1][self.SelectedPawn["x"] + 1] == CellState.RED_MAN
                          or self.Cells[self.SelectedPawn["y"] + 1][self.SelectedPawn["x"] + 1] == CellState.RED_KING)
                         and self.PlayerTurn == PlayerTurn.WHITE)):
            self.PossibleMoves.append((self.SelectedPawn["x"] + 2, self.SelectedPawn["y"] + 2))

        if (self.SelectedPawn["y"] + 2 < self.y and self.SelectedPawn["x"] - 2 >= 0) \
                and self.Cells[self.SelectedPawn["y"] + 2][self.SelectedPawn["x"] - 2] == CellState.EMPTY \
                and (((self.Cells[self.SelectedPawn["y"] + 1][self.SelectedPawn["x"] - 1] == CellState.WHITE_MAN
                       or self.Cells[self.SelectedPawn["y"] + 1][self.SelectedPawn["x"] - 1] == CellState.WHITE_KING)
                      and self.PlayerTurn == PlayerTurn.RED)
                     or ((self.Cells[self.SelectedPawn["y"] + 1][self.SelectedPawn["x"] - 1] == CellState.RED_MAN
                          or self.Cells[self.SelectedPawn["y"] + 1][self.SelectedPawn["x"] - 1] == CellState.RED_KING)
                         and self.PlayerTurn == PlayerTurn.WHITE)):
            self.PossibleMoves.append((self.SelectedPawn["x"] - 2, self.SelectedPawn["y"] + 2))

        if (self.SelectedPawn["y"] - 2 >= 0 and self.SelectedPawn["x"] + 2 < self.x) \
                and self.Cells[self.SelectedPawn["y"] - 2][self.SelectedPawn["x"] + 2] == CellState.EMPTY \
                and (((self.Cells[self.SelectedPawn["y"] - 1][self.SelectedPawn["x"] + 1] == CellState.WHITE_MAN
                       or self.Cells[self.SelectedPawn["y"] - 1][self.SelectedPawn["x"] + 1] == CellState.WHITE_KING)
                      and self.PlayerTurn == PlayerTurn.RED)
                     or ((self.Cells[self.SelectedPawn["y"] - 1][self.SelectedPawn["x"] + 1] == CellState.RED_MAN
                          or self.Cells[self.SelectedPawn["y"] - 1][self.SelectedPawn["x"] + 1] == CellState.RED_KING)
                         and self.PlayerTurn == PlayerTurn.WHITE)):
            self.PossibleMoves.append((self.SelectedPawn["x"] + 2, self.SelectedPawn["y"] - 2))

        if (self.SelectedPawn["y"] - 2 >= 0 and self.SelectedPawn["x"] - 2 >= 0) \
                and self.Cells[self.SelectedPawn["y"] - 2][self.SelectedPawn["x"] - 2] == CellState.EMPTY \
                and (((self.Cells[self.SelectedPawn["y"] - 1][self.SelectedPawn["x"] - 1] == CellState.WHITE_MAN
                       or self.Cells[self.SelectedPawn["y"] - 1][self.SelectedPawn["x"] - 1] == CellState.WHITE_KING)
                      and self.PlayerTurn == PlayerTurn.RED)
                     or ((self.Cells[self.SelectedPawn["y"] - 1][self.SelectedPawn["x"] - 1] == CellState.RED_MAN
                          or self.Cells[self.SelectedPawn["y"] - 1][self.SelectedPawn["x"] - 1] == CellState.RED_KING)
                         and self.PlayerTurn == PlayerTurn.WHITE)):
            self.PossibleMoves.append((self.SelectedPawn["x"] - 2, self.SelectedPawn["y"] - 2))

    """
    Method called after a man captured another to know if it can still perform any move
    """
    def GetPossibleMoves(self):
        self.PossibleMoves = []
        if self.Cells[self.SelectedPawn["y"]][self.SelectedPawn["x"]] == CellState.RED_KING or \
                self.Cells[self.SelectedPawn["y"]][self.SelectedPawn["x"]] == CellState.WHITE_KING:
            self.GetKingMoves()
        elif self.Cells[self.SelectedPawn["y"]][self.SelectedPawn["x"]] == CellState.RED_MAN or \
                self.Cells[self.SelectedPawn["y"]][self.SelectedPawn["x"]] == CellState.WHITE_MAN:
            self.GetManMoves()
        # Extra feature : if a pawn can capture he has to do it
        if self.CanCapture():
            # Creates a new list
            NewMoves = []
            self.PrintPossibleMoves()
            print("selected : " + str(self.SelectedPawn["x"]) + " " + str(self.SelectedPawn["y"]))
            for x, y in self.PossibleMoves:
                if abs(x - self.SelectedPawn["x"]) == 2 or abs(y - self.SelectedPawn["y"]) == 2:
                    # Adds the capture position to the new position list
                    NewMoves.append((x, y))
            self.PossibleMoves = NewMoves
        self.PrintPossibleMoves()

    """
    Method which defines if the selected pawn can capture
    """
    def CanCapture(self):
        for x, y in self.PossibleMoves:
            if abs(x - self.SelectedPawn["x"]) == 2 and abs(y - self.SelectedPawn["y"]) == 2:
                print("Pawn can capture")
                return True
        return False

    """
    Verifies if the selected man can move at the clicked position
    """
    def PerformManMove(self, x, y):
        # If the destination is one cell away
        if abs(x - self.SelectedPawn["x"]) == 1 and \
                abs(y - self.SelectedPawn["y"]) == 1 and \
                (x, y) in self.PossibleMoves:
            self.Move(x, y)
            self.ChangeTurn()
            self.Selected = False
            return True
        # If the destination is two cells away
        elif abs(x - self.SelectedPawn["x"]) == 2 and \
                abs(y - self.SelectedPawn["y"]) == 2 and \
                self.Cells[y][x] == CellState.EMPTY:
            if x + 2 == self.SelectedPawn["x"] and y + 2 == self.SelectedPawn["y"] \
                    and self.PlayerTurn == PlayerTurn.WHITE:
                # Top Left
                if self.Cells[y + 1][x + 1] == CellState.RED_KING or self.Cells[y + 1][x + 1] == CellState.RED_MAN:
                    print("White player ate a Red pawn")
                    self.ScoreWhite += 1
                    self.Cells[y + 1][x + 1] = CellState.EMPTY
                    self.Move(x, y)
                    self.SelectedPawn["y"] = y
                    self.SelectedPawn["x"] = x
                    self.GetPossibleMoves()
                    if self.CanCapture():
                        self.Capturing = True
                    else:
                        self.Selected = False
                        self.Capturing = False
                        self.ChangeTurn()
                    return True
                else:
                    return False
            elif x + 2 == self.SelectedPawn["x"] and y - 2 == self.SelectedPawn["y"] \
                    and self.PlayerTurn == PlayerTurn.RED:
                # Down Left
                if self.Cells[y - 1][x + 1] == CellState.WHITE_KING or self.Cells[y - 1][x + 1] == CellState.WHITE_MAN:
                    print("Red player ate a White pawn")
                    self.ScoreRed += 1
                    self.Cells[y - 1][x + 1] = CellState.EMPTY
                    self.Move(x, y)
                    self.SelectedPawn["y"] = y
                    self.SelectedPawn["x"] = x
                    self.GetPossibleMoves()
                    if self.CanCapture():
                        self.Capturing = True
                    else:
                        self.Selected = False
                        self.Capturing = False
                        self.ChangeTurn()
                    return True
                else:
                    return False
            elif x - 2 == self.SelectedPawn["x"] and y + 2 == self.SelectedPawn["y"] \
                    and self.PlayerTurn == PlayerTurn.WHITE:
                # Top Right
                if self.Cells[y + 1][x - 1] == CellState.RED_KING or self.Cells[y + 1][x - 1] == CellState.RED_MAN:
                    print("White player ate a Red pawn")
                    self.ScoreWhite += 1
                    self.Cells[y + 1][x - 1] = CellState.EMPTY
                    self.Move(x, y)
                    self.SelectedPawn["y"] = y
                    self.SelectedPawn["x"] = x
                    self.GetPossibleMoves()
                    if self.CanCapture():
                        self.Capturing = True
                    else:
                        self.Selected = False
                        self.Capturing = False
                        self.ChangeTurn()
                    return True
                else:
                    return False
            elif x - 2 == self.SelectedPawn["x"] and y - 2 == self.SelectedPawn["y"] \
                    and self.PlayerTurn == PlayerTurn.RED:
                # Down Right
                if self.Cells[y - 1][x - 1] == CellState.WHITE_KING or self.Cells[y - 1][x - 1] == CellState.WHITE_MAN:
                    print("Red player ate a White pawn")
                    self.ScoreRed += 1
                    self.Cells[y - 1][x - 1] = CellState.EMPTY
                    self.Move(x, y)
                    self.SelectedPawn["y"] = y
                    self.SelectedPawn["x"] = x
                    self.GetPossibleMoves()
                    if self.CanCapture():
                        self.Capturing = True
                    else:
                        self.Selected = False
                        self.Capturing = False
                        self.ChangeTurn()
                    return True
                else:
                    return False
        return False

    """
    Verifies if the selected king can move at the clicked position
    """
    def PerformKingMove(self, x, y):
        # If the destination is one cell away
        if abs(x - self.SelectedPawn["x"]) == 1 and \
                abs(y - self.SelectedPawn["y"]) == 1 and \
                (x, y) in self.PossibleMoves:
            self.Move(x, y)
            self.ChangeTurn()
            self.Selected = False
            return True
        # If the destination is two cells away
        elif abs(x - self.SelectedPawn["x"]) == 2 and \
                abs(y - self.SelectedPawn["y"]) == 2 and \
                self.Cells[y][x] == CellState.EMPTY:
            if x + 2 == self.SelectedPawn["x"] and y + 2 == self.SelectedPawn["y"]:
                # Top Left
                if (self.Cells[y + 1][x + 1] == CellState.WHITE_KING or self.Cells[y + 1][x + 1] == CellState.WHITE_MAN) \
                        and self.PlayerTurn == PlayerTurn.RED:
                    print("Black player ate a White pawn")
                    self.ScoreRed += 1
                    self.Cells[y + 1][x + 1] = CellState.EMPTY
                    self.Move(x, y)
                    self.SelectedPawn["y"] = y
                    self.SelectedPawn["x"] = x
                    self.GetPossibleMoves()
                    if self.CanCapture():
                        self.Capturing = True
                    else:
                        self.Selected = False
                        self.Capturing = False
                        self.ChangeTurn()
                    return True
                elif (self.Cells[y + 1][x + 1] == CellState.RED_KING or self.Cells[y + 1][x + 1] == CellState.RED_MAN) \
                        and self.PlayerTurn == PlayerTurn.WHITE:
                    print("White player ate a Black pawn")
                    self.ScoreWhite += 1
                    self.Cells[y + 1][x + 1] = CellState.EMPTY
                    self.Move(x, y)
                    self.SelectedPawn["y"] = y
                    self.SelectedPawn["x"] = x
                    self.GetPossibleMoves()
                    if self.CanCapture():
                        self.Capturing = True
                    else:
                        self.Selected = False
                        self.Capturing = False
                        self.ChangeTurn()
                    return True
                else:
                    return False
            elif x + 2 == self.SelectedPawn["x"] and y - 2 == self.SelectedPawn["y"]:
                # Down Left
                if (self.Cells[y - 1][x + 1] == CellState.WHITE_KING or self.Cells[y - 1][x + 1] == CellState.WHITE_MAN) \
                        and self.PlayerTurn == PlayerTurn.RED:
                    print("Black player ate a White pawn")
                    self.ScoreRed += 1
                    self.Cells[y - 1][x + 1] = CellState.EMPTY
                    self.Move(x, y)
                    self.SelectedPawn["y"] = y
                    self.SelectedPawn["x"] = x
                    self.GetPossibleMoves()
                    if self.CanCapture():
                        self.Capturing = True
                    else:
                        self.Selected = False
                        self.Capturing = False
                        self.ChangeTurn()
                    return True
                elif (self.Cells[y - 1][x + 1] == CellState.RED_KING or self.Cells[y - 1][x + 1] == CellState.RED_MAN) \
                        and self.PlayerTurn == PlayerTurn.WHITE:
                    print("White player ate a Black pawn")
                    self.ScoreWhite += 1
                    self.Cells[y - 1][x + 1] = CellState.EMPTY
                    self.Move(x, y)
                    self.SelectedPawn["y"] = y
                    self.SelectedPawn["x"] = x
                    self.GetPossibleMoves()
                    if self.CanCapture():
                        self.Capturing = True
                    else:
                        self.Selected = False
                        self.Capturing = False
                        self.ChangeTurn()
                    return True
                else:
                    return False
            elif x - 2 == self.SelectedPawn["x"] and y + 2 == self.SelectedPawn["y"]:
                # Top Right
                if (self.Cells[y + 1][x - 1] == CellState.WHITE_KING or self.Cells[y + 1][x - 1] == CellState.WHITE_MAN) \
                        and self.PlayerTurn == PlayerTurn.RED:
                    print("Black player ate a White pawn")
                    self.ScoreRed += 1
                    self.Cells[y + 1][x - 1] = CellState.EMPTY
                    self.Move(x, y)
                    self.SelectedPawn["y"] = y
                    self.SelectedPawn["x"] = x
                    self.GetPossibleMoves()
                    if self.CanCapture():
                        self.Capturing = True
                    else:
                        self.Selected = False
                        self.Capturing = False
                        self.ChangeTurn()
                    return True
                elif (self.Cells[y + 1][x - 1] == CellState.RED_KING or self.Cells[y + 1][x - 1] == CellState.RED_MAN) \
                        and self.PlayerTurn == PlayerTurn.WHITE:
                    print("White player ate a Black pawn")
                    self.ScoreWhite += 1
                    self.Cells[y + 1][x - 1] = CellState.EMPTY
                    self.Move(x, y)
                    self.SelectedPawn["y"] = y
                    self.SelectedPawn["x"] = x
                    self.GetPossibleMoves()
                    if self.CanCapture():
                        self.Capturing = True
                    else:
                        self.Selected = False
                        self.Capturing = False
                        self.ChangeTurn()
                    return True
                else:
                    return False
            elif x - 2 == self.SelectedPawn["x"] and y - 2 == self.SelectedPawn["y"]:
                # Down Right
                if (self.Cells[y - 1][x - 1] == CellState.WHITE_KING or self.Cells[y - 1][x - 1] == CellState.WHITE_MAN) \
                        and self.PlayerTurn == PlayerTurn.RED:
                    print("Black player ate a White pawn")
                    self.ScoreRed += 1
                    self.Cells[y - 1][x - 1] = CellState.EMPTY
                    self.Move(x, y)
                    self.SelectedPawn["y"] = y
                    self.SelectedPawn["x"] = x
                    self.GetPossibleMoves()
                    if self.CanCapture():
                        self.Capturing = True
                    else:
                        self.Selected = False
                        self.Capturing = False
                        self.ChangeTurn()
                    return True
                elif (self.Cells[y - 1][x - 1] == CellState.RED_KING or self.Cells[y - 1][x - 1] == CellState.RED_MAN) \
                        and self.PlayerTurn == PlayerTurn.WHITE:
                    print("White player ate a Black pawn")
                    self.ScoreWhite += 1
                    self.Cells[y - 1][x - 1] = CellState.EMPTY
                    self.Move(x, y)
                    self.SelectedPawn["y"] = y
                    self.SelectedPawn["x"] = x
                    self.GetPossibleMoves()
                    if self.CanCapture():
                        self.Capturing = True
                    else:
                        self.Selected = False
                        self.Capturing = False
                        self.ChangeTurn()
                    return True
                else:
                    return False
        return False

    """
    Defines if a move is possible
    """
    def PerformMove(self, x, y):
        # If the pawn is a man
        if self.Cells[self.SelectedPawn["y"]][self.SelectedPawn["x"]] == CellState.WHITE_MAN or \
                self.Cells[self.SelectedPawn["y"]][self.SelectedPawn["x"]] == CellState.RED_MAN:
            return self.PerformManMove(x, y)
        # If the pawn is a king
        elif self.Cells[self.SelectedPawn["y"]][self.SelectedPawn["x"]] == CellState.WHITE_KING or \
                self.Cells[self.SelectedPawn["y"]][self.SelectedPawn["x"]] == CellState.RED_KING:
            return self.PerformKingMove(x, y)
        return False

    """
    DEBUG Method : prints the board cells differently for visibility
    """
    def PrintCells(self):
        for y in self.Cells:
            for x in y:
                if x == CellState.EMPTY:
                    print(0, end='')
                elif x == CellState.RED_MAN:
                    print(1, end='')
                elif x == CellState.RED_KING:
                    print(2, end='')
                elif x == CellState.WHITE_MAN:
                    print(3, end='')
                elif x == CellState.WHITE_KING:
                    print(4, end='')
            print("\n", end='')

    """
    DEBUG Method : prints the possible moves
    """
    def PrintPossibleMoves(self):
        for x in self.PossibleMoves:
            print(x)
