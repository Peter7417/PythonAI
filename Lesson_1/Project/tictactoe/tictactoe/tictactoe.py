"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None

# Debugging
# def printer(board):
#     length = len(board)
#     for i in range(length):
#         print(board[i])


def explored(board):
    lst = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                lst.append(tuple((i,j)))

    if lst == [] and board != initial_state():
        terminal(board)

    return lst


def counter(board):
    x = None
    y = None
    for i in range(3):
        for j in range(3):
            if board[i][j] != EMPTY:
                x = i
                y = j

    choice = cells(x, y, board)
    return choice


def Xcounter(board):
    count = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == X:
                count += 1

    return count


def Ocounter(board):
    count = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == O:
                count += 1

    return count


def cells(x,y,board):
    pairs = explored(board)

    if x is None and y is None:
        # print(pairs)
        return pairs
    for i in range(len(pairs)):
        if pairs[i] == (x,y):
            del pairs[i]
            break
    return pairs


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
    if board == initial_state():
        return X

    v1 = Xcounter(board)

    v2 = Ocounter(board)

    if v1 > v2:
        return O
    else:
        return X

    raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    count = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                count += 1
    if count == 9:
        val = cells(None,None,board)
        return val
    else:
        val = counter(board)
        return val



    raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # check action against board boundaries
    if action[0] < 0 or action[0] > 2 or action[1] < 0 or action[1] > 2:
        raise Exception("action value outside boundary, fatal error")

    # check if given action is a tuple
    if len(action) != 2:
        raise Exception("action expected to be a tuple, action not accepted")

    y, x = action[0], action[1]

    # make a deep copy to run possible state spaces
    board_copy = copy.deepcopy(board)

    if board_copy[y][x] != EMPTY:
        raise Exception("action coordinate is not empty, fatal error")
    else:
        # here we use the player function to know which letter to put in the copy
        board_copy[y][x] = player(board)
        return board_copy



def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # horizontal win

    for i in range(3):
        if board[i] == [X,X,X]:
            return X
        if board[i] == [O,O,O]:
            return O

    # vertical win

    for i in range(3):
        if board[0][i] != EMPTY and board[0][i] == board[1][i] and board[1][i] == board[2][i]:
            return board[0][i]

    # diagonal win 1

    if board[0][0] != EMPTY and board[0][0] == board[1][1] and board[1][1] == board[2][2]:
        return board[0][0]

    # diagonal win 2

    if board[0][2] != EMPTY and board[0][2] == board[1][1] and board[1][1] == board[2][0]:
        return board[0][2]

    # if board ends in tie
    count = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] != EMPTY:
                count += 1
    if count == 9:
        return None

    # if the game is still on-going
    return 0

    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) == X or winner(board) == O or winner(board) is None:
        return True
    else:
        return False


    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0

    raise NotImplementedError


def min_value(board):
    # if the game has ended, show winner and end session
    if terminal(board):
        return utility(board)

    # find and return the smallest of all maximum possible outcomes
    min_of_max_val = math.inf
    for action in actions(board):
        min_of_max_val = min(min_of_max_val, max_value(result(board,action)))
    return min_of_max_val


def max_value(board):
    # if the game has ended, show winner and end session
    if terminal(board):
        return utility(board)

    # find and return the largest of all minimum possible outcomes
    max_of_min_val = -math.inf
    for action in actions(board):
        max_of_min_val = max(max_of_min_val,min_value(result(board,action)))
    return max_of_min_val


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    # set up alpha beta pruning
    alpha = -math.inf
    beta = math.inf

    if terminal(board):
        return None

    # playing as X, the best move is to get a value of 1, so we must call the min_value function to get the
    # smallest possible value to be compared against the true small value: alpha,
    # if the found value is greater than alpha a goal has been reached
    if player(board) == X:
        best_move = None
        for action in actions(board):
            min_val = min_value(result(board, action))
            if min_val > alpha:
                alpha = min_val
                best_move = action
        # return the action that corresponds to the largest min_val
        return best_move

    # playing as O, the worst move is to get a value of -1, so we must call the max_value function to get the
    # largest possible value to be compared against the true large value: beta,
    # if the found value is smaller than beta a goal has been reached
    if player(board) == O:
        best_move = None
        for action in actions(board):
            max_val = max_value(result(board,action))
            if max_val < beta:
                best_move = action
                beta = max_val
        # return the action that corresponds to the smallest max_val
        return best_move

    raise NotImplementedError




