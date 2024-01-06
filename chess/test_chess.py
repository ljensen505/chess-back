from uuid import UUID

from .chess import Chess


def test_init():
    chess = Chess()
    assert isinstance(chess, Chess)
    assert isinstance(chess.id, UUID)
    assert len(str(chess.id)) == 36


def test_repr():
    chess = Chess()
    assert repr(chess) == f"Chess({chess.id})\n\n{chess.board}\n"


def test_iter():
    chess = Chess()

    vals = ["id", "board", "game_state", "turn_count", "turn", "captured_pieces"]
    assert all([val in dict(chess) for val in vals])
    board = dict(chess)["board"]
    assert isinstance(board, dict)
    assert len(board) == 32
    assert all([isinstance(p, dict) for p in board.values()])
