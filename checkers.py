from typing import List, Dict

WHITE = True    # X
BLACK = False   # O


class Checker:
    """
    Checker is defined by it's color (checkers.WHITE OR checkers.BLACK) and if it has been crowned.

    White checkers are printed as "x" (if crowned, "X").

    Black checkers are printed as "o" (if crowned, "O")
    """
    color: bool
    crowned: bool

    def __init__(self, color: bool, crowned: bool = False):
        self.color = color
        self.crowned = crowned

    def __str__(self):
        if self.color == WHITE:
            return "X" if self.crowned else "x"
        else:
            return "O" if self.crowned else "o"

    def set_crowned(self, w):
        self.crowned = w
        return self


class Move:
    """
    Move denotes a change in position for a checker from position (fx, fy) to position (tx, ty).
    It also stores information if the move results in a promotion of a checker, and the removed checker if the move
    was a jump.
    """
    checker: Checker
    move_from: (int, int)
    move_to: (int, int)
    is_promotion: bool
    removed_checker: Checker

    def __init__(self, ch: Checker, xf: int, yf: int, xt: int, yt: int, prom: bool = False, removed: Checker = None):
        """
        :param ch: Checker that is moving
        :param xf: from x
        :param yf: from y
        :param xt: to x
        :param yt: to y
        :param prom: If moving Checker was promoted
        :param removed: Checker that was removed with a jump, or None of jump was not made
        """
        self.checker = ch
        self.move_from = (xf, yf)
        self.move_to = (xt, yt)
        self.is_promotion = prom
        self.removed_checker = removed

    def __str__(self):
        return self.__repr__()

    def __repr__(self) -> str:
        return f"Move<{self.checker},f{self.move_from},t{self.move_to}>"


class Board:
    """
    Holds state of a game of checkers.
    """

    state: Dict[int, Dict[int, Checker]] = {}
    # state contains positions of all the checkers that are on board
    # each dictionary is a row in a board, therefore state should be queried first by Y coordinate, and then
    # by X coordinate, e.g. self.state[y][x].
    # Example: self.state[3][7] would contain checker in 4th row (from top to bottom, starting with 0) and 8th column
    # (from left to right, starting with 0)

    move_stack: List[List[Move]] = []
    # move_stack is a list of performed "moves", note that a "move" is a list as it can consist of multiple Moves
    # (i.e. chaining jumps)

    color: bool = WHITE
    # color denotes which player is currently on the turn, and is updated when making a move (calling push) or undoing
    # a move (calling pop)

    def __init__(self):
        """
        Creates a new checkers board with initial starting configuration
        """
        self.clear_board()
        self.set_board(".o.o.o.o.o,o.o.o.o.o.,.o.o.o.o.o,o.o.o.o.o.,,,.x.x.x.x.x,x.x.x.x.x.,.x.x.x.x.x,x.x.x.x.x.")

    def __str__(self):
        """
        A nice output of the board. For checkers notation output, use get_board()!
        :return:
        """
        s = ""
        for y in range(0, 10):
            for x in range(0, 10):
                if self.state[y].get(x) is not None:
                    s += str(self.state[y][x]) + " "
                else:
                    s += ". "
            s += "\n"
        return s

    def set_board(self, notation: str):
        """
        Clears the board and initializes new board from given checkers notation
        :param notation:
        :return:
        """
        self.clear_board()

        for y, row in enumerate(notation.split(",")):
            for x, state in enumerate(row):
                if state == "x":
                    ch = Checker(WHITE)
                    self.state[y][x] = ch
                elif state == "X":
                    ch = Checker(WHITE)
                    ch.crowned = True
                    self.state[y][x] = ch
                elif state == "o":
                    ch = Checker(BLACK)
                    self.state[y][x] = ch
                elif state == "O":
                    ch = Checker(BLACK)
                    ch.crowned = True
                    self.state[y][x] = ch
                elif state == ".":
                    pass
                else:
                    raise ValueError("Invalid character in notation: " + str(state))

    def get_board(self):
        """
        Notation output of the board. For a nicer output of the whole board, use str(board)!
        :return:
        """
        s = ""
        first = True
        for row in range(0, 10):
            if not first:
                s += ","
            first = False

            if len(self.state[row]) == 0:
                continue

            for col in range(0, 10):
                if col in self.state[row]:
                    s += str(self.state[row][col])
                else:
                    s += "."
        return s

    def clear_board(self):
        """
        Empties the board (removes all checkers), clears move stack and sets player color to WHITE.
        :return:
        """
        self.state.clear()
        for i in range(10):
            self.state[i] = {}

        self.move_stack.clear()
        self.color = WHITE

    def legal_moves(self):
        """
        TODO doc
        :return:
        """
        moves: List[List[Move]] = []

        for y, rows in self.state.items():
            for x, checker in rows.items():
                # generate moves for current player
                if checker.color == self.color:

                    # check for moves when a checker can do a jump and remove other player's checker.
                    # By international checkers ruleset, jumps can be done in all four directions (backwards too!).
                    # Additionally, jumps can also be chained together, and if there's another jump available, player
                    # MUST perform it. By international ruleset, if there's a jump move available, player MUST perform
                    # a jump, rather than a normal move.

                    chains = get_longest_jump_chains(self, x, y, [], [[]])
                    if len(chains) != 0 and len(chains[0]) != 0:
                        # return list of longest chains
                        return chains
                    else:
                        # for default moves, white checkers go up (-y) diagonally,
                        # black checkers go down (+y) diagonally
                        if self.color == WHITE:
                            for (nx, ny) in [(x-1, y-1), (x+1, y-1)]:
                                if is_position_on_board(nx, ny) and self.checker_at(nx, ny) is None:
                                    chk = self.state[y][x]
                                    moves.append([Move(chk, x, y, nx, ny, will_get_crowned(chk.color, ny))])
                        else:
                            for (nx, ny) in [(x-1, y+1), (x+1, y+1)]:
                                if is_position_on_board(nx, ny) and self.checker_at(nx, ny) is None:
                                    chk = self.state[y][x]
                                    moves.append([Move(chk, x, y, nx, ny, will_get_crowned(chk.color, ny))])

        return moves

    def push(self, move: List[Move]):
        """
        Moves checker from starting to ending position of a move (or move chain).
        :param move:
        :return:
        """
        self.move_stack.append(move)

        fx, fy = move[0].move_from
        tx, ty = move[-1].move_to
        chk = move[0].checker
        # remove checker from starting position
        del self.state[fy][fx]
        # place checker at ending position
        self.state[ty][tx] = chk

        # remove all jumped opponent's checkers
        for m in move:
            mfx, mfy = m.move_from
            mtx, mty = m.move_to
            if abs(mfx - mtx) == 2:
                atk_x = (mfx + mtx) // 2
                atk_y = (mfy + mty) // 2
                del self.state[atk_y][atk_x]

        # set checker crowned if last move in chain is promotion
        if move[-1].is_promotion:
            chk.crowned = True

        # set other player's round
        self.color = not self.color

    def pop(self):
        """
        Undoes the move on top of the stack, returning board in a state before the move was made.
        :return:
        """
        move = self.move_stack.pop()

        fx, fy = move[0].move_from
        tx, ty = move[-1].move_to
        chk = move[-1].checker
        # remove checker from ending position
        del self.state[ty][tx]
        # ... and place it back on starting position
        self.state[fy][fx] = chk

        # restore all jumped opponent's checkers
        for m in move:
            if m.removed_checker is not None:
                mfx, mfy = m.move_from
                mtx, mty = m.move_to
                atk_x = (mfx + mtx) / 2
                atk_y = (mfy + mty) / 2
                self.state[atk_y][atk_x] = m.removed_checker

        # set checker not crowned if last move in chain was promotion
        if move[-1].is_promotion:
            chk.crowned = False

        # set other player's round
        self.color = not self.color

    def checker_at(self, x: int, y: int):
        return self.state[y].get(x)

###################
### ~ HELPERS ~ ###
###################


def is_position_on_board(x, y) -> bool:
    return 0 <= x < 10 and 0 <= y < 10


def will_get_crowned(color: bool, y: int) -> bool:
    """
    :param color:
    :param y:
    :return: True if moving into row Y with color can result into crowning
    """
    if color and y == 0:
        return True
    if not color and y == 9:
        return True
    return False


def can_perform_jump(board: Board, x: int, y: int, jx: int, jy: int) -> bool:
    checker = board.checker_at(x, y)
    if checker is None:
        # obviously, jump should be performed with a checker
        return False

    if board.checker_at(jx, jy) is not None:
        # jump can only be performed if the goal position is free
        return False

    if not checker.crowned:
        # non-crowned checker can only jump over one field
        if (jx, jy) not in [(x-2, y-2), (x-2, y+2), (x+2, y-2), (x+2, y+2)]:
            return False

        # jump can only be performed if the field between start and goal has a checker of other color
        ox, oy = (x + jx) // 2, (y + jy) // 2
        other_checker = board.checker_at(ox, oy)
        if other_checker is not None and other_checker.color != checker.color:
            return True
        else:
            return False

    else: # checker.crowned
        # TODO: crowned checkers can jump any distance, however they can jump only over one checker and must jump to
        # the field right after removed checker

        # TODO: not sure about above will check the rules
        pass


def get_possible_jumps(board: Board, x: int, y: int) -> List[Move]:
    """
    Returns a list of possible jumps from current position.
    :param board:
    :param x:
    :param y:
    :return:
    """
    moves: List[Move] = []

    # Positions in list: [upper-left, bottom-left, upper-right, bottom-right]
    for (jx, jy) in [(x-2, y-2), (x-2, y+2), (x+2, y-2), (x+2, y+2)]:
        if is_position_on_board(jx, jy) and can_perform_jump(board, x, y, jx, jy):
            jumped_checker = board.checker_at((x + jx) // 2, (y + jy) // 2)
            moves.append(Move(board.checker_at(x, y), x, y, jx, jy, removed=jumped_checker))

    return moves


def get_longest_jump_chains(board: Board, x: int, y: int, current_chain: List[Move], chains: List[List[Move]]) -> List[List[Move]]:
    """
    Recursively perform all possible jumps and return a list of longest chains.
    :param board: starting board for search
    :param x: starting x coordinate of checker
    :param y: starting y coordinate of checker
    :param current_chain: current working chain, pass [] for first call
    :param chains: list of longest chains, pass [[]] for first call
    :return:
    """
    for jump in get_possible_jumps(board, x, y):
        board.push([jump]) # push a move
        board.color = not board.color
        nx, ny = jump.move_to
        chains = get_longest_jump_chains(board, nx, ny, current_chain + [jump], chains) # recursive call from current state
        board.pop() # undo pushed move
        board.color = not board.color

    if len(current_chain) > len(chains[0]):
        # if result chains of recursion are longer, discard currently stored chains (they are shorter)
        # and store new ones
        chains = [current_chain]
    elif len(current_chain) == len(chains[0]):
        chains = chains + [current_chain]

    return chains # return list of longest found chains