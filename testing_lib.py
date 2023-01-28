import lib


games = lib.read_data('data/Player/Kasparov.pgn') 
print(len(games))
game = games[0]
positions, moves = lib.get_positions_moves(game)
print(moves)
