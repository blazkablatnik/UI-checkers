import unittest

import math

from checkers import Board, Move, WHITE, BLACK

MAX = True
MIN = False
INF = 999999


def alpha_beta_search(board: Board, max_depth: int) -> Move:
    """
    Returns best Move for given Board, found by performing minimax algorithm with alpha-beta pruning.
    :param board: Board to start search from
    :param max_depth: Maximum tree depth to search
    :return: best found Move
    """

    # By international checker rules and for given board_value function, board_value has a range of [-20, 20]
    best_move, best_value = None, -INF

    # Perform MAX step explicitly, storing best move and it's value
    player_color = True
    for move in board.legal_moves():
        board.push(move)
        value = _alpha_beta(board, player_color, max_depth, -INF, +INF, MAX)
        board.pop()

        if value > best_value:
            best_move = move

    return best_move


def _alpha_beta(board: Board, color: bool, depth: int, alpha: int, beta: int, opt: bool):
    """
    Implementation of minimax with alpha-beta pruning follows the pseudo-code on Wikipedia:
    https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning#Pseudocode

    :param board:
    :param depth: Maximum tree depth to search. Decreases with recursive calls.
    :param alpha:
    :param beta:
    :param opt:
    :return:
    """

    # if reached max depth or there's no legal moves left, return board value
    if depth == 0 or len(board.legal_moves()) <= 0:
        return _board_value(board, color)

    # if searching for optimal move when it's player's turn, look for MAX value
    if opt == MAX:
        value = -INF
        for move in board.legal_moves():
            board.push(move)
            value = max(value, _alpha_beta(board, color, depth - 1, alpha, beta, MIN))
            board.pop()

            alpha = max(alpha, value)
            if alpha >= beta:
                break  # beta-prune

        return value

    # else (it's other player's turn), look for MIN value (that'd be MAX from other player's perspective)
    else:  # opt == MIN
        value = +INF
        for move in board.legal_moves():
            board.push(move)
            value = min(value, _alpha_beta(board, color, depth - 1, alpha, beta, MAX))
            board.pop()
            beta = min(beta, value)
            if alpha >= beta:
                break  # alpha-prune

        return value


def _board_value(board: Board, color: bool) -> int:
    """
    Returns value of the board. Value is calculated as +1 for each checker of given color and -1 for each checker of
    other color.
    :param board:
    :param color:
    :return:
    """
    total = 1
    for (x, y, checker) in board.get_checkers():
        total += (+1 if checker.color == color else -1) * (5 if checker.crowned else 1)
    return total


class BoardValueTests(unittest.TestCase):

    def test_1(self):
        b = Board()
        b.set_board("x")
        self.assertEqual(1, _board_value(b, WHITE))
        self.assertEqual(-1, _board_value(b, BLACK))

    def test_2(self):
        b = Board()
        b.set_board("X")
        self.assertEqual(3, _board_value(b, WHITE))
        self.assertEqual(-3, _board_value(b, BLACK))

    def test_3(self):
        b = Board()
        b.set_board("Xxxxxoo")
        self.assertEqual(3+4-2, _board_value(b, WHITE))
        self.assertEqual(-3-4+2, _board_value(b, BLACK))

    def test_4(self):
        b = Board()
        b.set_board("XXXOOOxoxo")
        self.assertEqual(0, _board_value(b, WHITE))
        self.assertEqual(0, _board_value(b, BLACK))