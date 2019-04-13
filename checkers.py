from typing import List, Dict

WHITE = True    # X
BLACK = False   # O


def is_position_on_board(x, y):
    return 0 <= x < 10 and 0 <= y < 10


class Checker:
    """
    Checker is defined by it's color (checkers.WHITE OR checkers.BLACK) and if it has been crowned.

    White checkers are printed as "x" (if crowned, "X").

    Black checkers are printed as "o" (if crowned, "O")
    """
    color: bool
    crowned: bool

    def __init__(self, color: bool):
        self.color = color
        self.crowned = False

    def __str__(self):
        if self.color == WHITE:
            return "X" if self.crowned else "x"
        else:
            return "O" if self.crowned else "o"


class Move:
    """
    TODO...
    """
    checker: Checker
    move_from: (int, int)
    move_to: (int, int)

    def __init__(self, ch, xf, yf, xt, yt):
        self.checker = ch
        self.move_from = (xf, yf)
        self.move_to = (xt, yt)

    def __str__(self):
        return f"Move[{self.checker},f{self.move_from},t{self.move_to}]"


class Board:
    """
    Holds state of a game of checkers.
    """

    state: Dict[int, Dict[int, Checker]]
    move_stack: List[Move] = []
    color: bool = WHITE

    def __init__(self):
        """
        Creates a new checkers board with initial starting configuration
        """
        self.state = {}
        for i in range(10):
            self.state[i] = {}

        for i in range(1, 10, 2):
            self.state[0][i] = Checker(BLACK)
            self.state[2][i] = Checker(BLACK)
            self.state[6][i] = Checker(WHITE)
            self.state[8][i] = Checker(WHITE)

        for i in range(0, 10, 2):
            self.state[1][i] = Checker(BLACK)
            self.state[3][i] = Checker(BLACK)
            self.state[7][i] = Checker(WHITE)
            self.state[9][i] = Checker(WHITE)

    def __str__(self):
        s = ""
        for x in range(0, 10):
            for y in range(0, 10):
                if y in self.state[x]:
                    s += str(self.state[x][y]) + " "
                else:
                    s += ". "
            s += "\n"
        return s

    def legal_moves(self):
        """
        TODO
        """
        moves: List[Move] = []

        for x, rows in self.state.items():
            for y, checker in rows.items():
                # generate moves for current player
                if checker.color == self.color:
                    # check for moves when a checker can do a jump and remove other player's checker.
                    # By international checkers ruleset, jumps can be done in all four directions (backwards too!)
                    # TODO

                    # additionally, jumps can also be chained together, and if there's another jump available, player
                    # MUST perform it
                    # TODO

                    # by international ruleset, if there's a jump move available, player MUST perform a jump, rather
                    # than a normal move.
                    # additionally, player MUST perform the longest series of jumps available
                    # TODO

                    # for default moves, white checkers go up (-y), black checkers go down (+y)
                    if self.color == WHITE:
                        if is_position_on_board(x - 1, y - 1) and y - 1 not in self.state[x - 1]:
                            moves.append(Move(self.state[x][y], x, y, x - 1, y - 1))
                        if is_position_on_board(x - 1, y + 1) and y + 1 not in self.state[x - 1]:
                            moves.append(Move(self.state[x][y], x, y, x - 1, y + 1))
                    else:
                        if is_position_on_board(x + 1, y - 1) and y - 1 not in self.state[x + 1]:
                            moves.append(Move(self.state[x][y], x, y, x + 1, y - 1))
                        if is_position_on_board(x + 1, y + 1) and y + 1 not in self.state[x + 1]:
                            moves.append(Move(self.state[x][y], x, y, x + 1, y + 1))

        return moves

    def push(self, move: Move):
        """
        TODO
        :param move:
        :return:
        """
        # move checker from position move_from to position move_to
        self.move_stack.append(move)

        fx, fy = move.move_from
        tx, ty = move.move_to
        del self.state[fx][fy]
        self.state[tx][ty] = move.checker

        # set other player's round
        self.color = not self.color

    def pop(self):
        """
        TODO
        :return:
        """
        # undo the move on the top of move stack
        move = self.move_stack.pop()

        fx, fy = move.move_from
        tx, ty = move.move_to
        del self.state[tx][ty]
        self.state[fx][fy] = move.checker
