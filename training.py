import torch
import torch.nn as nn
import numpy as np
import chess
from model import value_model, representation_model
from utils import board_to_string
from tqdm import tqdm

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
representation_model.to(device)
value_model.to(device)

tokens_to_idx = {'K': 0,
                 'k': 1,
                 'p': 2,
                 'P': 3,
                 'q': 4,
                 'R': 5,
                 'N': 6,
                 '#': 7,
                 'Q': 8,
                 '$': 9,
                 'n': 10,
                 'B': 11,
                 'r': 12,
                 'b': 13,
                 '.': 14}


def get_value(board):
    board_str = board_to_string(board)
    board_tensor = torch.tensor([[tokens_to_idx[ch] for ch in board_str]])
    with torch.no_grad():
        representation = representation_model(board_tensor.to(device))
        value = value_model(representation.pooler_output)
    return value.item()


# Self play
def make_move(board):
    moves = board.legal_moves
    values = []
    moves_list = []
    for move in moves:
        board.push(move)
        values.append(get_value(board))
        moves_list.append(move)
        board.pop()
    values = torch.tensor(values)
    if board.turn:
        best_move = moves_list[torch.argmax(values)]
    else:
        best_move = moves_list[torch.argmin(values)]
    board.push(best_move)
    return board


loss_function = nn.MSELoss()
optimizer = torch.optim.Adam(list(value_model.parameters()) + list(representation_model.parameters()), lr=1e-3)

t = tqdm(range(1000))
for i in t:
    board = chess.Board()
    while not board.is_game_over():
        board = make_move(board)
    # making data for the model
    # we need the board_strs and the assigned values
    result = board.result()
    # if draw ignore game
    if board.result() == '1/2-1/2':
        value = 0
    elif board.result() == '1-0':
        value = 1
    else:
        value = -1
    board_strs = [torch.tensor([[tokens_to_idx[ch] for ch in board_to_string(board)]])]
    board_values = np.linspace(0, value, num=len(board.move_stack) + 1, dtype=np.float32)[::-1].copy()

    while board != chess.Board():
        board.pop()
        board_strs.append(torch.tensor([[tokens_to_idx[ch] for ch in board_to_string(board)]]))
    assert len(board_strs) == len(board_values)
    board_strs = torch.concat(board_strs, 0)
    board_values = torch.from_numpy(board_values).reshape(-1, 1)
    representation = representation_model(board_strs.to(device))
    value = value_model(representation.pooler_output)
    loss = loss_function(value, board_values.to(device))
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    t.set_description(f'Loss: {loss.item()} {result}')
