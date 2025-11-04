# app.py
# Simple CLI interface to play against the AI from analyzer.py
import argparse
import chess
import sys
from analyzer import select_best_move

def print_board(board):
    # Use ASCII board for terminal
    print(board)
    print()

def human_move(board):
    while True:
        try:
            user_in = input("Your move (in UCI, e.g. e2e4) or 'quit': ").strip()
            if user_in.lower() in ('quit', 'exit'):
                sys.exit(0)
            move = chess.Move.from_uci(user_in)
            if move in board.legal_moves:
                return move
            else:
                print("Illegal move. Try again.")
        except Exception as e:
            print("Invalid input. Use UCI like e2e4. Error:", e)

def main():
    parser = argparse.ArgumentParser(description='Play vs ChessBot (simple minimax AI).')
    parser.add_argument('--depth', type=int, default=3, help='Search depth for AI (default: 3).')
    parser.add_argument('--human-color', choices=['white', 'black'], default='white',
                        help='Which color you want to play as (default: white).')
    args = parser.parse_args()

    board = chess.Board()
    human_is_white = args.human_color == 'white'

    print("Starting game. You are playing as", args.human_color)
    print_board(board)

    while not board.is_game_over():
        if board.turn == chess.WHITE:
            side = 'White'
        else:
            side = 'Black'

        if (board.turn == chess.WHITE and human_is_white) or (board.turn == chess.BLACK and not human_is_white):
            print(f"{side} to move — your turn.")
            move = human_move(board)
            board.push(move)
        else:
            print(f"{side} to move — AI thinking (depth={args.depth})...")
            move = select_best_move(board, depth=args.depth)
            if move is None:
                print('AI resigns (no move found).')
                break
            print('AI plays:', move.uci())
            board.push(move)

        print_board(board)

    print('Game over:', board.result())
    print('Reason:', 'Checkmate' if board.is_checkmate() else board.outcome())

if __name__ == '__main__':
    main()
