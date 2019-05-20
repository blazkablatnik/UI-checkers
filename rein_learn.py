import copy

from checkers import Board, Move
from random import randint, random
from alphabeta import alpha_beta_search

# ~ Player 1 is us ~

# [Q-learning] :
# For any finite Markov decision process (FMDP), Q-learning finds a policy that is optimal in the sense
# that it maximizes the expected value of the total reward over any and all successive steps,
# starting from the current state.
#
# It involves:
# - Agent
# - set of states S -> [s1, s2, s3, ... , sn]
# - set A of actions per state -> [s1:[a1, a2, a3,...], s2:[a1, a2, a3,...], ... , sn:[a1, a2, a3,...]]
#
# We perform action and transition between states. We put value on action based on its state.
# The goal is to find the policy to maximize this value.
#
#
# [DEFINING Q-TABLE]
#      a1   a2   a3  ... an
#  s1
#  s2
#  s3
#  .
#  .
#  .
#  sn
#
# a) All possible states:
#       [1]: If a player 1 can attack, he must (no choice there).
#       [2]: Player 1 wins (all the points)
#       [3]: Player 1 looses (all the negative points)
#       [4]: Player 1 is attacked:
#               o by 1 or by 2
#               o will cost us 1,2,3.. lost pieces
#       [5]: None of the above:
#               o can we prepare attack?
#               o if we get under attack, that's bad
#
# b) All possible actions:
#       [0]: Action that will get us in one of the above states


########################################################################
#########################                  #############################
#########################     ALGORITEM    #############################
#########################                  #############################
########################################################################

## ~ INITIALIZATION ~

# Discount factor (0 <= _delta <= 1)
# - has the effect of valuing rewards received earlier higher than those received later
#  (reflecting the value of a "good start")
# - may also be interpreted as the probability to succeed (or survive) at every step
_delta = 0.1

# Learning rate (0 <= _alpha <= 1)
_alpha = 0.9

# Number of learning iterations
nmb_of_learning_iterations = 0

# Switch for learning
learning = True

our_pics = 'x'
their_pics = 'o'
our_kings = 'X'
their_kings = 'O'

# State
class State:
    def __init__(self,
                 n_our_un_crwn_pices,
                 n_their_un_crwn_pices,
                 n_our_king,
                 n_their_king,
                 n_pcs_on_edge,
                 own_center_of_mass,
                 their_center_of_mass):
        self.n_our_un_crwn_pices = n_our_un_crwn_pices
        self.n_their_un_crwn_pices = n_their_un_crwn_pices
        self.n_our_king = n_our_king
        self.n_their_king = n_their_king
        self.n_pcs_on_edge = n_pcs_on_edge
        self.own_center_of_mass = own_center_of_mass
        self.their_center_of_mass = their_center_of_mass

    def to_string(self):
        return str(self.n_our_un_crwn_pices) + "_" + \
               str(self.n_their_un_crwn_pices) + "_" + \
               str(self.n_our_king) + "_" + \
               str(self.n_their_king) + "_" + \
               str(self.n_pcs_on_edge) + "_" + \
               str(self.own_center_of_mass) + "_" + \
               str(self.their_center_of_mass)

    def get_value(self):
        return self.n_our_un_crwn_pices + \
               -1 * self.n_their_un_crwn_pices + \
               5 * self.n_our_king + \
               -5 * self.n_their_king + \
               6 * self.n_pcs_on_edge




def get_transition_key(from_state, to_state):
    return from_state.to_string() + "->" + to_state.to_string()

def get_from_and_to(transition_key):
    return transition_key.split('->')


def get_pics_on_edge(pics_mark, king_mark, board):
    counter = 0;
    for row in board.get_board().split(','):
        if row.startswith(pics_mark) or row.startswith(king_mark) or row.endswith(pics_mark) or row.endswith(king_mark):
            counter += 1
    return counter


def get_state(move: Move, board: Board):
    board.push(move)
    n_our_un_crwn_pices = board.get_board().count(our_pics)
    n_their_un_crwn_pices = board.get_board().count(their_pics)
    n_our_king = board.get_board().count(our_kings)
    n_their_king = board.get_board().count(their_kings)
    n_pcs_on_edge = get_pics_on_edge(our_pics, our_kings, board)
    own_center_of_mass = 0
    their_center_of_mass = 0

    board.pop()

    return State(n_our_un_crwn_pices,
                 n_their_un_crwn_pices,
                 n_our_king,
                 n_their_king,
                 n_pcs_on_edge,
                 own_center_of_mass,
                 their_center_of_mass)


def get_transitions(current_state: State, legal_moves, board: Board):
    transitions = {}
    for move in legal_moves:
        new_state = get_state(move, board)
        transiton_key = get_transition_key(current_state, new_state)
        transitions[transiton_key] = [current_state, new_state]

    return transitions


# Actions
# Is a transition between state

# Q-table -> Q[State][Action]
# Q - table is dynamic and is names Transition table, as it is in key (transition) value format
# It is 2D dictionary:
#   o first key is a "from" state
#   o second key is a "to" state
T = {}

# Exploration rate (0 <= ex_rate <= 1)
# Rate at which AI tries to make new moves
ex_rate = 0.5

if learning:
    for i in range(nmb_of_learning_iterations):

        # Init board
        board = Board()

        # Init starting state
        current_state = State(20, 20, 0, 0, 4, 0, 0)

        while True:

            # Generate all moves
            legal_moves = board.legal_moves()

            # Check if game over
            if len(legal_moves) <= 0:
                print("prisel do konca")
                # If we won
                T[current_state][new_state.to_string()] *= 100

                # If we lost
                T[current_state][new_state.to_string()] *= -100
                break

            # For every move calculate the state it produces
            transitions = get_transitions(current_state, legal_moves, board)

            explore = random.uniform(0, 1) <= ex_rate

            new_transitions = {}

            if not T:
                # Empty dictionary: 100% explore
                new_transitions = transitions
                explore = True
            else:
                # If one or more transition is unknown, then explore or choose the highest value with ration ex_rate
                max_value = 0
                max_transition = []

                for transition_key, states in transitions.items():
                    if transition_key not in T:
                        new_transitions[transition_key] = states
                    else:
                        value = T[transition_key]
                        if value > max_value:
                            max_value = value
                            max_transition_key = transition_key

            if explore:
                # Choose random new transition
                new_state = new_transitions.keys()[randint(0, len(new_transitions) - 1)]
                old_transition_value = 0
            else:
                # Choose mac transition
                new_state = max_transition
                old_transition_value = max_value

            value_of_transition = old_transition_value - new_state.get_value()

            # Get max optimal future value
            if new_state.to_string() not in T:
                optimal_future_value = 0
            else:
                key_of_max = max(T[new_state.to_string()].keys(), key=(lambda k: T[k]))
                optimal_future_value = T[new_state.to_string()][key_of_max]

            # Now we update transition table:
            # new_value <- (1-_alpha)old_value + _alpha*(reward_for_transition + _delta*(max (all_new_potential_transitions - current_transition)))
            T[current_state][new_state.to_string()] = old_transition_value + _alpha*value_of_transition + _delta*optimal_future_value

            # AlphaBeta makes move
            # !! important: work with this copy of a board to prevent
            # accidental changes to actual game state.
            board_copy = copy.deepcopy(board)
            board.push(alpha_beta_search(board_copy, 4))
