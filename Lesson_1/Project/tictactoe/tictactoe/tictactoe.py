"""
Tic Tac Toe Player
"""

import math
import random
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
    if board[action[0]][action[1]] is not None:
        raise Exception("Space not empty")

    if player(board) == X:
        (board[action[0]][action[1]]) = X
        outboard = board
        return outboard
    elif player(board) == O:
        (board[action[0]][action[1]]) = O
        outboard = board
        return outboard
    else:
        raise NotImplementedError



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


def min_value(board,alpha,beta):


    best_move = None
    min_val = math.inf
    for action in actions(board):
        board_copy = copy.deepcopy(board)
        best_move, v_min = max_value(result(board_copy,action),alpha,beta)
        if v_min < min_val:
            best_move = action
            min_val = v_min

        if min_val <= alpha:
            break;

        if min_val < beta:
            beta = min_val

    print("best min move:",best_move)
    return best_move, min_val


def max_value(board,alpha,beta):


    best_move = None
    max_val = -math.inf
    for action in actions(board):
        board_copy = copy.deepcopy(board)
        best_move, v_max = min_value(result(board_copy, action),alpha,beta)

        if v_max > max_val:
            best_move = action
            max_val = v_max

        if max_val >= beta:
            break;

        if max_val > alpha:
            alpha = max_val

    print("best max move:", best_move)
    return best_move, max_val



def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    alpha = -math.inf
    beta = math.inf

    if terminal(board):
        return None

    if player(board) == X:
        m1 = max_value(board,alpha,beta)
        return m1[0]

    if player(board) == O:
        m2 = min_value(board,alpha,beta)
        return m2[0]

    raise NotImplementedError




