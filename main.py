from pprint import pprint

from chess import Chess

if __name__ == "__main__":
    chess = Chess()

    chess.make_move("E2", "E4")
    chess.make_move("E7", "E5")
    chess.make_move("D1", "H5")
