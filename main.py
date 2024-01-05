from chess import Chess

if __name__ == "__main__":
    chess = Chess()
    print(chess)
    chess.make_move("E2", "E4")
    print(chess)
    chess.make_move("E7", "E5")
    print(chess)
