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
    given a game returns the moves(uci) and board positions(fen)
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

def fen_to_board_str(fen):
    b = chess.Board.from_epd(fen)[0]    
    return str(b).replace('\n', '').replace(' ', '')

def make_move(uci):
    '''
    returns the two postions of the uci(Universal Chess Interface) format
    '''
    pos1 = uci[:2]
    pos2 = uci[2:4]
    return (chess.parse_square(pos1), chess.parse_square(pos2))


