from pprint import pprint

from chess import SQUARE_NAMES, Board, Piece, Square

board = Board()
print(board)
pprint(type(board.piece_map().get(0)))
board.piece_at(0)
sq: Square = 0
print(sq)
sq: Square = "a1"
print(sq)
