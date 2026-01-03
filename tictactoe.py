import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    return X if x_count <= o_count else O


def actions(board):
    if terminal(board):
        return set()

    moves = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] is EMPTY:
                moves.add((i, j))
    return moves


def result(board, action):
    i, j = action

    if board[i][j] is not EMPTY:
        raise Exception("Invalid action")

    new_board = copy.deepcopy(board)
    new_board[i][j] = player(board)
    return new_board


def winner(board):
    lines = []

    # Rows
    lines.extend(board)

    # Columns
    lines.extend([[board[i][j] for i in range(3)] for j in range(3)])

    # Diagonals
    lines.append([board[i][i] for i in range(3)])
    lines.append([board[i][2 - i] for i in range(3)])

    for line in lines:
        if line.count(X) == 3:
            return X
        if line.count(O) == 3:
            return O

    return None


def terminal(board):
    if winner(board) is not None:
        return True

    return all(cell is not EMPTY for row in board for cell in row)


def utility(board):
    w = winner(board)
    if w == X:
        return 1
    if w == O:
        return -1
    return 0


def minimax(board):
    if terminal(board):
        return None

    current_player = player(board)

    if current_player == X:
        best_value = -math.inf
        best_move = None
        for action in actions(board):
            value = min_value(result(board, action))
            if value > best_value:
                best_value = value
                best_move = action
        return best_move

    else:
        best_value = math.inf
        best_move = None
        for action in actions(board):
            value = max_value(result(board, action))
            if value < best_value:
                best_value = value
                best_move = action
        return best_move


def max_value(board):
    if terminal(board):
        return utility(board)

    v = -math.inf
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v


def min_value(board):
    if terminal(board):
        return utility(board)

    v = math.inf
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v

