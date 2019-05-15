import math

from checkers import Board, Move

MAX = True
MIN = False


def alpha_beta_search(board: Board, max_depth: int) -> Move:
    """
    Returns best Move for given Board, found by performing minimax algorithm with alpha-beta pruning.
    :param board: Board to start search from
    :param max_depth: Maximum tree depth to search
    :return: best found Move
    """
    best_move, best_value = None, -math.inf

    # Perform MAX step explicitly, storing best move and it's value
    for move in board.legal_moves():
        board.push(move)
        value = _alpha_beta(board, max_depth, -math.inf, +math.inf, MIN) # continue minimax with MIN step
        board.pop()

        if value > best_value:
            best_move = move

    return best_move


def _alpha_beta(board: Board, depth: int, alpha: float, beta: float, opt: bool):
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
    if depth == 0 or len(board.legal_moves()) <= 0:
        return __board_value(board)

    if opt == MAX:
        value = -math.inf
        for move in board.legal_moves():
            board.push(move)
            value = max(value, _alpha_beta(board, depth - 1, alpha, beta, MIN))
            board.pop()
            alpha = max(alpha, value)
            if alpha >= beta:
                break  # beta-prune

        return value

    else:  # opt == MIN
        value = +math.inf
        for move in board.legal_moves():
            board.push(move)
            value = min(value, _alpha_beta(board, depth - 1, alpha, beta, MAX))
            board.pop()
            beta = min(beta, value)
            if alpha >= beta:
                break  # alpha-prune

        return value


def __board_value(board: Board) -> int:
    total = 0
    for (x, y, checker) in board.get_checkers():
        total += 1 if checker.color == board.color else 0
    return total
