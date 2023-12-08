"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # Initialize X and O counters
    x_counter = 0
    o_counter =0

    # Loops through board
    for row in board:
        for field in row:
            if field == X:
                x_counter += 1
            elif field == O:
                o_counter += 1
    
    # Decide which turn it is
    if x_counter > o_counter:
        return O
    elif x_counter < o_counter:
        return X
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()

    # Loops through board
    for row in range(3):
        for field in range(3):
            if board[row][field] == EMPTY:
                possible_actions.add((row, field))

    return possible_actions



def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Deep copy state of the board
    new_board_state = copy.deepcopy(board)

    # Sign that will be played by player
    sign = player(board)

    # Check if action is possible
    if action not in actions(board):
        raise Exception("Action not possible")
    
    # Update board with new state
    new_board_state[action[0]][action[1]] = sign

    return new_board_state

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check which player is expected to win
    expected_sign = None
    if player(board) is X:
        expected_sign = O
    else:
        expected_sign = X

    # Check if 3 in a row vertically
    for i in range(3):
        vertical_counter = 0
        for j in range(3):
            if board[j][i] is expected_sign:
                vertical_counter += 1
        if vertical_counter == 3:
            return expected_sign

    # Check if 3 in a row horizontally
    for i in range(3):
        horizontal_counter = 0
        for j in range (3):
            if board[i][j] is expected_sign:
                horizontal_counter += 1
        if horizontal_counter == 3:
            return expected_sign
 
    # Check if 3 in a row left diagonally
    l_diagonal_counter = 0
    for i in range(3):
        if board[i][i] is expected_sign:
            l_diagonal_counter += 1
        if l_diagonal_counter == 3:
            return expected_sign

    # Check if 3 in a row right diagonally
    r_diagonal_counter = 0
    for i in range(3):
        if board[i][2-i] is expected_sign:
            r_diagonal_counter += 1
        if r_diagonal_counter == 3:
            return expected_sign

    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # If someone won the game
    if winner(board) is not None:
        return True

    # Check if it is an uncomplete game
    for row in board:
        for field in row:
            if field is EMPTY:
                return False
            
    # If there is no EMPTY game is over
    return True

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if win is X:
        return 1
    elif win is O:
        return -1
    else:
        return 0

# Functions for minimax algorythm
def max_value(board):
    value = -math.inf

    if terminal(board):
        return utility(board)
    
    for action in actions(board):
        value = max(value, min_value(result(board, action)))

    return value

def min_value(board):
    value = math.inf

    if terminal(board):
        return utility(board)
    
    for action in actions(board):
        value = min(value, max_value(result(board, action)))

    return value

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # If board is terminal board
    if terminal(board):
        return None
    
    if player(board) is X:
        best_value = -math.inf
        best_action = None
        for action in actions(board):

            # Check how selected action ends up game score
            value = min_value(result(board, action))

            # Immediately make winner move for Max-player
            if value == 1:
                return action

            # Choose best option for Max-player
            if value > best_value:
                best_value = value
                best_action = action

        # Return best option      
        return best_action
    
    else:
        best_value = math.inf
        best_action = None
        for action in actions(board):
            
            # Check how selected action ends up game score
            value = max_value(result(board, action))

            # Immediately make winner move for Min-player
            if value == -1:
                return action
            
            # Choose best option for Min-player
            if value < best_value:
                best_value = value
                best_action = action

        # Return best option      
        return best_action

