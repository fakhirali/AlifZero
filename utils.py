import chess

def board_to_string(board: chess.Board):
    return str(board).replace(' ', '').replace('\n', '') + ('#' if board.turn else '$')
