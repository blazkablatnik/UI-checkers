import copy

from alphabeta import alpha_beta_search
from checkers import Board, WHITE

board = Board()
board.set_board(",......x.x.,,,.....o,o.o.o.....,...o...o,,,O")
while len(board.legal_moves()) > 0:

    # !! important: work with this copy of a board to prevent
    # accidental changes to actual game state.
    board_copy = copy.deepcopy(board)

    # store your selected move (returned by your algorithm) into this variable
    selected_move = None

    if board.color == WHITE:
        # AI Player 1 (Minimax with alpha-beta prunning)
        selected_move = alpha_beta_search(board_copy, 5)

        pass

    else: # brd.color == BLACK
        # AI Player 2 (TODO)

        selected_move = board_copy.legal_moves()[0]

        pass

    board.push(selected_move)

    print("-----")
    print(board.color)
    print(board)
