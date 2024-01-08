from pprint import pprint

from chess import Chess

if __name__ == "__main__":
    chess = Chess()

    chess.make_move("E2", "E4")
    print(chess)
    chess.make_move("D7", "D5")
    print(chess)

    chess.make_move("E4", "D5")
    print(chess)
    chess.make_move("D8", "D5")
    pprint(chess)
