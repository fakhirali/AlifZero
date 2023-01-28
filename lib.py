import chess
import numpy as np
import time
import os
import chess.pgn
from tqdm import tqdm

#reading data
def read_data(path):
    file = open(path, encoding="utf-8")
    games = []
    a = chess.pgn.read_game(file)
    while a:
        games.append(a)
        try:
            a = chess.pgn.read_game(file)
        except:
            print(f'could not read game number {len(games)}')
    return games


def get_positions_moves(game):
    '''
    given a games returns the moves(uci) and board positions(fen)
    Note: The board positions do not include the first position
    '''
    main_line = game.next()
    if main_line is None:
    	return [], []
    positions = []
    moves = []
    while main_line.next():
        positions.append(main_line.board().fen())
        moves.append(main_line.move)
        main_line = main_line.next()
    return positions, moves




