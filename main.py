from pprint import pprint

from chess import Chess

if __name__ == "__main__":
    chess = Chess()

    chess.make_move("A2", "A4")
    chess.make_move("A7", "A5")
    chess.make_move("A1", "A3")
    chess.make_move("A8", "A6")
