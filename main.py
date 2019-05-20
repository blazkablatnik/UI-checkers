import copy
import random

from alphabeta import alpha_beta_search
from checkers import Board, WHITE, BLACK

board = Board()
# board.set_board(".X...o.o..,,...o,,,.........o,...x,x.x.x.x.x.")
# board.color = BLACK

print(board)
print("----- ************* -----")

while len(board.legal_moves()) > 0:
    print("Player " + str("WHITE" if board.color else "BLACK") + " has " + str(len(board.legal_moves())) + " available moves.")

    # !! important: work with this copy of a board to prevent
    # accidental changes to actual game state.
    board_copy = copy.deepcopy(board)

    # store your selected move (returned by your algorithm) into this variable
    selected_move = None

    if board.color == BLACK:
        # AI Player 1 (Minimax with alpha-beta prunning)
        selected_move = alpha_beta_search(board_copy, 5)
        pass

    else: # brd.color == BLACK
        # AI Player 2 (TODO)

        # selected_move = alpha_beta_search(board_copy, 4)
        selected_move = random.choice(board_copy.legal_moves())
        # selected_move = board_copy.legal_moves()[0]

        pass

    print("Chosen move: " + str(selected_move))
    board.push(selected_move)

    print(board)
    print("----- ----- -----")
