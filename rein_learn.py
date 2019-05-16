from checkers import Board, WHITE

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
_delta = 0.9

# Number of learning iterations
nmb_of_learning_iterations = 0

# Switch for learning
learning = True

# States
S = []

# Actions
A = []

# Q-table
Q = [[0 for i in range(len(A))] for i in range(len(S))]


if(learning):
    for i in range(nmb_of_learning_iterations):

        # Init board
        board = Board()

        while():
            pass

