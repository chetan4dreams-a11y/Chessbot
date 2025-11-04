# analyzer.py
# Chess engine logic using python-chess
import chess
import math
import random

PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000
}

def evaluate_board(board: chess.Board) -> int:
    """
    Simple evaluation function: material + mobility.
    Positive values favor White, negative values favor Black.
    """
    if board.is_checkmate():
        # If side to move is checkmated, very bad for that side
        return -999999 if board.turn else 999999
    if board.is_stalemate() or board.is_insufficient_material():
        return 0

    material = 0
    for piece_type in PIECE_VALUES:
        material += len(board.pieces(piece_type, chess.WHITE)) * PIECE_VALUES[piece_type]
        material -= len(board.pieces(piece_type, chess.BLACK)) * PIECE_VALUES[piece_type]

    # Mobility: number of legal moves
    mobility = len(list(board.legal_moves))
    # Flip mobility sign for black to get relative mobility
    board_push = board.copy(stack=False)
    board_push.turn = not board.turn
    opp_mobility = len(list(board_push.legal_moves))
    mobility_score = mobility - opp_mobility

    eval_score = material + mobility_score * 10
    return eval_score

def minimax_root(board: chess.Board, depth: int, is_white: bool=True):
    """
    Wrapper used to select the best move at root using minimax with alpha-beta.
    Returns a chess.Move object.
    """
    best_move = None
    best_value = -math.inf if is_white else math.inf
    alpha = -math.inf
    beta = math.inf

    moves = list(board.legal_moves)
    # small shuffle for variety among equal moves
    random.shuffle(moves)

    for move in moves:
        board.push(move)
        value = minimax(board, depth - 1, alpha, beta, not is_white)
        board.pop()

        if is_white:
            if value > best_value:
                best_value = value
                best_move = move
            alpha = max(alpha, best_value)
        else:
            if value < best_value:
                best_value = value
                best_move = move
            beta = min(beta, best_value)
    return best_move

def minimax(board: chess.Board, depth: int, alpha: float, beta: float, is_maximizing: bool) -> float:
    """
    Minimax search with alpha-beta pruning.
    """
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    if is_maximizing:
        max_eval = -math.inf
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            if eval > max_eval:
                max_eval = eval
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = math.inf
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            if eval < min_eval:
                min_eval = eval
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def select_best_move(board: chess.Board, depth: int=3) -> chess.Move:
    """
    Convenience function to return the best move for the side to move.
    Default depth is 3 which is quick but not very strong. Increase depth for stronger play.
    """
    is_white = board.turn == chess.WHITE
    return minimax_root(board, depth, is_white)
