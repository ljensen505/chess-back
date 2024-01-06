from .bishop import Bishop
from .king import King
from .knight import Knight
from .pawn import Pawn
from .piece import Piece
from .queen import Queen
from .rook import Rook


def test_piece_init():
    assert Piece("WHITE", "A1").color == "WHITE"
    assert Piece("WHITE", "A1").position == "A1"
    assert Piece("WHITE", "A1").has_moved == False
    assert Piece("WHITE", "A1").icon == "?"
    assert Piece("WHITE", "A1").available_moves == []
    assert Piece("WHITE", "A1").type == "piece"


def test_inheritance():
    assert isinstance(Pawn("WHITE", "A1"), Piece)
    assert isinstance(Knight("WHITE", "A1"), Piece)
    assert isinstance(Bishop("WHITE", "A1"), Piece)
    assert isinstance(Rook("WHITE", "A1"), Piece)
    assert isinstance(Queen("WHITE", "A1"), Piece)
    assert isinstance(King("WHITE", "A1"), Piece)


def test_icon():
    assert Pawn("WHITE", "A1").icon == "♟︎"
    assert Knight("WHITE", "A1").icon == "♞"
    assert Bishop("WHITE", "A1").icon == "♝"
    assert Rook("WHITE", "A1").icon == "♜"
    assert Queen("WHITE", "A1").icon == "♛"
    assert King("WHITE", "A1").icon == "♚"


def test_repr():
    assert repr(Pawn("WHITE", "A1")) == "Pawn(WHITE, A1)"
    assert repr(Knight("WHITE", "A1")) == "Knight(WHITE, A1)"
    assert repr(Bishop("WHITE", "A1")) == "Bishop(WHITE, A1)"
    assert repr(Rook("WHITE", "A1")) == "Rook(WHITE, A1)"
    assert repr(Queen("WHITE", "A1")) == "Queen(WHITE, A1)"
    assert repr(King("WHITE", "A1")) == "King(WHITE, A1)"


def test_str():
    assert str(Pawn("WHITE", "A1")) == "♟︎"
    assert str(Knight("WHITE", "A1")) == "♞"
    assert str(Bishop("WHITE", "A1")) == "♝"
    assert str(Rook("WHITE", "A1")) == "♜"
    assert str(Queen("WHITE", "A1")) == "♛"
    assert str(King("WHITE", "A1")) == "♚"


def test_iter():
    assert dict(Pawn("WHITE", "A1")) == {"color": "white", "type": "pawn"}
    assert dict(Knight("WHITE", "A1")) == {"color": "white", "type": "knight"}
    assert dict(Bishop("WHITE", "A1")) == {"color": "white", "type": "bishop"}
    assert dict(Rook("WHITE", "A1")) == {"color": "white", "type": "rook"}
    assert dict(Queen("WHITE", "A1")) == {"color": "white", "type": "queen"}
    assert dict(King("WHITE", "A1")) == {"color": "white", "type": "king"}


def test_set_available_moves():
    piece = Pawn("WHITE", "A1")
    piece.set_available_moves(["A2", "A3"])
    assert piece.available_moves == ["A2", "A3"]


def test_set_has_moved():
    piece = Pawn("WHITE", "A1")
    assert piece.has_moved == False
    piece.set_has_moved()
    assert piece.has_moved == True


def test_set_position():
    piece = Pawn("WHITE", "A1")
    assert piece.position == "A1"
    piece.set_position("A2")
    assert piece.position == "A2"
