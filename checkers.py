import copy
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

    def __init__(self, color: bool):
        self.color = color
        self.crowned = False

    def __str__(self):
        if self.color == WHITE:
            return "X" if self.crowned else "x"
        else:
            return "O" if self.crowned else "o"

    def set_crowned(self, crowned: bool):
        self.crowned = crowned
        return self

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
    move_stack: List[List[Move]] = []
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

    def set_board(self, notation: str):
        self.clear_board()

        for x, row in enumerate(notation.split(",")):
            for y, state in enumerate(row):
                if state == "x":
                    ch = Checker(WHITE)
                    self.state[x][y] = ch
                elif state == "X":
                    ch = Checker(WHITE)
                    ch.crowned = True
                    self.state[x][y] = ch
                elif state == "o":
                    ch = Checker(BLACK)
                    self.state[x][y] = ch
                elif state == "O":
                    ch = Checker(BLACK)
                    ch.crowned = True
                    self.state[x][y] = ch
                elif state == ".":
                    pass
                else:
                    raise ValueError("Invalid character in notation: " + str(state))

    def get_board(self):
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
        TODO
        """
        moves: List[Move] = []

        longest_attack_path_global: List[Move] = []
        for x, rows in self.state.items():
            for y, checker in rows.items():
                # generate moves for current player
                if checker.color == self.color:

                    # check for moves when a checker can do a jump and remove other player's checker.
                    # By international checkers ruleset, jumps can be done in all four directions (backwards too!).
                    # Additionally, jumps can also be chained together, and if there's another jump available, player
                    # MUST perform it. By international ruleset, if there's a jump move available, player MUST perform
                    # a jump, rather than a normal move.

                    # Get longest attack path
                    longest_attack_path_local = get_longest_attack_path_rek(copy.deepcopy(self), self.color, x, y)

                    # Add longest path to global list if path is longer (append if the same length) or there
                    # is no global path jet.
                    if longest_attack_path_local:
                        if longest_attack_path_global:
                            if len(longest_attack_path_local[0]) > len(longest_attack_path_global[0]):
                                longest_attack_path_global = longest_attack_path_local
                            else:
                                if len(longest_attack_path_local[0]) == len(longest_attack_path_global[0]):
                                    longest_attack_path_global.extend(longest_attack_path_local)
                        else:
                            longest_attack_path_global = longest_attack_path_local



                    # for default moves, white checkers go up (-y) diagonally, black checkers go down (+y) diagonally
                    if not longest_attack_path_global:
                        if self.color == WHITE:
                            if is_position_on_board(x - 1, y - 1) and y - 1 not in self.state[x - 1]:
                                moves.append([Move(copy.deepcopy(self.state[x][y].set_crowned(will_get_crowned(self.color, x - 1))), x, y, x - 1, y - 1)])
                            if is_position_on_board(x - 1, y + 1) and y + 1 not in self.state[x - 1]:
                                moves.append([Move(copy.deepcopy(self.state[x][y].set_crowned(will_get_crowned(self.color, x - 1))), x, y, x - 1, y + 1)])
                        else:
                            if is_position_on_board(x + 1, y - 1) and y - 1 not in self.state[x + 1]:
                                moves.append([Move(copy.deepcopy(self.state[x][y].set_crowned(will_get_crowned(self.color, x + 1))), x, y, x + 1, y - 1)])
                            if is_position_on_board(x + 1, y + 1) and y + 1 not in self.state[x + 1]:
                                moves.append([Move(copy.deepcopy(self.state[x][y].set_crowned(will_get_crowned(self.color, x + 1))), x, y, x + 1, y + 1)])

        if longest_attack_path_global:
            return longest_attack_path_global
        else:
            return moves

    def push(self, move: List[Move]):
        """
        TODO
        :param move:
        :return:
        """
        # move checker from position move_from to position move_to
        self.move_stack.append(move)

        fx, fy = move[len(move)-1].move_from
        tx, ty = move[len(move)-1].move_to
        del self.state[fx][fy]
        self.state[tx][ty] = move[len(move)-1].checker

        # remove all attacked opponents checkers
        for m in move:
            attacked_x = (int)(fx+tx)/2
            attacked_y = (int)(fy+ty)/2
            del self.state[attacked_x][attacked_y]

        # set other player's round
        self.color = not self.color

        return self

    def pop(self):
        """
        TODO - put back all removed pieces
        :return:
        """
        # undo the move on the top of move stack
        move = self.move_stack.pop()

        fx, fy = move[0].move_from
        tx, ty = move[len(move)-1].move_to
        del self.state[tx][ty]
        self.state[fx][fy] = move[len(move)-1].checker

        return self

    def checker_at(self, x: int, y: int) -> Checker:
        try:
            return self.state[x][y]
        except KeyError:
            return None


class Utility:
    def moves_to_string(self, moves):
        s = ""
        for move in moves:
            if s != "":
                s+= ","
            for m in move:
                s += str(m)
        return s

###################
### ~ HELPERS ~ ###
###################
def is_position_on_board(x, y):
    return 0 <= x < 10 and 0 <= y < 10

def will_get_crowned(color: bool, x: int):
    if color and x == 0:
        return True

    if not color and x == 9:
        return True

def get_all_single_attacks(board: Board, color: bool, x: int, y: int) -> List[Move]:
    list_of_moves: List[Move] = []

    # 1. Upper-left
    ul = board.checker_at(x-1, y-1)
    if is_position_on_board(x-1, y-1) and ul and ul.color != color and is_position_on_board(x-2, y-2) and board.checker_at(x-2, y-2) == None:
        list_of_moves.append(Move(copy.deepcopy(board.checker_at(x, y)), x, y, x-2, y-2))

    # 2. Upper-right
    ur = board.checker_at(x+1, y-1)
    if is_position_on_board(x+1, y-1) and ur and ur .color != color and is_position_on_board(x+2, y-2) and board.checker_at(x+2, y-2) == None:
        list_of_moves.append(Move(copy.deepcopy(board.checker_at(x, y)), x, y, x+2, y-2))

    # 3. Bottom-left
    bl = board.checker_at(x-1, y+1)
    if is_position_on_board(x-1, y+1) and bl and bl.color != color and is_position_on_board(x-2, y+2) and board.checker_at(x-2, y+2) == None:
        list_of_moves.append(Move(copy.deepcopy(board.checker_at(x, y)), x, y, x-2, y+2))

    # 4. Bottom-right
    br = board.checker_at(x+1, y+1)
    if is_position_on_board(x+1, y+1) and br and br.color != color and is_position_on_board(x+2, y+2) and board.checker_at(x+2, y+2) == None:
        list_of_moves.append(Move(copy.deepcopy(board.checker_at(x, y)), x, y, x+2, y+2))

    return list_of_moves

def get_longest_attack_path_rek(board: Board, color: bool, x: int, y: int, moves_so_far: List[Move] = []) -> List[List[Move]]:
    all_single_attacks: List[Move] = get_all_single_attacks(board, color, x, y)
    if not all_single_attacks:

        if moves_so_far:
            if will_get_crowned(color, moves_so_far[len(moves_so_far)-1].move_to[0]):
                moves_so_far[len(moves_so_far)-1].checker = moves_so_far[len(moves_so_far)-1].checker.set_crowned(True)

        # Don't return nested empty arrays
        if not moves_so_far:
            return []
        else:
            return [moves_so_far]
    else:
        longest_path: List[List[Move]] = []
        for attack in all_single_attacks:
            board_copy = copy.deepcopy(board)
            current_path = get_longest_attack_path_rek(board_copy.push([attack]), color, attack.move_to[0], attack.move_to[1], moves_so_far + [attack])
            if longest_path and current_path:
                if len(current_path[0]) > len(longest_path[0]):
                    longest_path = current_path
                else:
                    if len(current_path[0]) == len(longest_path[0]):
                        longest_path.extend(current_path)
            else:
                longest_path = current_path

        return longest_path


