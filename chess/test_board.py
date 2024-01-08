from pytest import raises

import chess
from chess import board
from chess.board import Board
from chess.pieces import BLACK, WHITE, Piece, piece
from chess.pieces.bishop import Bishop
from chess.pieces.queen import Queen
from chess.pieces.rook import Rook


def test_init():
    board = Board()
    assert board.active_pieces["A2"].color == WHITE
    assert board.active_pieces["A2"].position == "A2"
    assert board.active_pieces["A2"].has_moved == False
    assert board.active_pieces["A2"].icon == "♟︎"
    assert len(board.active_pieces["A2"].available_moves) > 0


def test_repr():
    board = Board()
    icons = ["♜", "♞", "♝", "♛", "♚", "♝", "♞", "♜"]
    for icon in icons:
        assert icon in repr(board)


def test_iter():
    board = Board()

    assert dict(board) == {
        "A2": {"color": "white", "type": "pawn"},
        "A7": {"color": "black", "type": "pawn"},
        "B2": {"color": "white", "type": "pawn"},
        "B7": {"color": "black", "type": "pawn"},
        "C2": {"color": "white", "type": "pawn"},
        "C7": {"color": "black", "type": "pawn"},
        "D2": {"color": "white", "type": "pawn"},
        "D7": {"color": "black", "type": "pawn"},
        "E2": {"color": "white", "type": "pawn"},
        "E7": {"color": "black", "type": "pawn"},
        "F2": {"color": "white", "type": "pawn"},
        "F7": {"color": "black", "type": "pawn"},
        "G2": {"color": "white", "type": "pawn"},
        "G7": {"color": "black", "type": "pawn"},
        "H2": {"color": "white", "type": "pawn"},
        "H7": {"color": "black", "type": "pawn"},
        "B1": {"color": "white", "type": "knight"},
        "B8": {"color": "black", "type": "knight"},
        "G1": {"color": "white", "type": "knight"},
        "G8": {"color": "black", "type": "knight"},
        "A1": {"color": "white", "type": "rook"},
        "A8": {"color": "black", "type": "rook"},
        "H1": {"color": "white", "type": "rook"},
        "H8": {"color": "black", "type": "rook"},
        "C1": {"color": "white", "type": "bishop"},
        "C8": {"color": "black", "type": "bishop"},
        "F1": {"color": "white", "type": "bishop"},
        "F8": {"color": "black", "type": "bishop"},
        "D1": {"color": "white", "type": "queen"},
        "D8": {"color": "black", "type": "queen"},
        "E1": {"color": "white", "type": "king"},
        "E8": {"color": "black", "type": "king"},
    }


def test_get_piece():
    board = Board()
    piece = board.get_piece("A2")
    assert piece is not None
    assert piece.color == WHITE
    assert piece.position == "A2"
    assert piece.has_moved == False
    assert piece.icon == "♟︎"
    assert len(piece.available_moves) > 0
    assert board.get_piece("A9") is None


def test_move_pawn():
    board = Board()
    piece = board.get_piece("A2")
    assert piece is not None
    assert piece.has_moved is False
    assert piece.color == WHITE
    board.move_piece(piece, "A3")
    moved_piece = board.get_piece("A3")
    assert moved_piece is not None
    assert moved_piece is piece
    assert moved_piece.has_moved is True
    assert moved_piece.available_moves == {"A4"}
    assert board.get_piece("A2") is None

    # test invalid move
    with raises(ValueError):
        board.move_piece(piece, "A5")
    with raises(ValueError):
        board.move_piece(piece, "A2")
    with raises(ValueError):
        board.move_piece(piece, "E5")


def test_knight_moves():
    board = Board()
    piece = board.get_piece("B1")
    assert piece is not None
    assert piece.color == WHITE
    assert piece.position == "B1"
    assert piece.has_moved is False
    assert piece.icon == "♞"
    assert piece.available_moves == {"A3", "C3"}
    board.move_piece(piece, "C3")
    moved_piece = board.get_piece("C3")
    assert moved_piece is not None
    assert moved_piece is piece
    assert moved_piece.has_moved is True
    assert moved_piece.available_moves == {"A4", "B5", "D5", "E4", "B1"}
    assert board.get_piece("B1") is None

    # test invalid move
    with raises(ValueError):
        board.move_piece(piece, "C5")
    with raises(ValueError):
        board.move_piece(piece, "C2")
    with raises(ValueError):
        board.move_piece(piece, "A2")
    with raises(ValueError):
        board.move_piece(piece, "D3")


def test_bishop_moves():
    board = Board()
    piece = board.get_piece("C1")
    assert isinstance(piece, Bishop)
    assert piece.available_moves == set()


def test_queen_moves():
    board = Board()
    piece = board.get_piece("D1")
    assert isinstance(piece, Queen)
    assert piece.available_moves == set()


def test_rook_moves():
    board = Board()
    piece = board.get_piece("A1")
    assert isinstance(piece, Rook)
    assert piece.available_moves == set()


# TODO: add tests for other piece moves as they are implemented
