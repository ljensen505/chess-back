from uuid import UUID

from pytest import raises

import chess
from chess import Chess
from chess.pieces import BLACK, WHITE, Piece
from chess.pieces.knight import Knight
from chess.pieces.pawn import Pawn
from chess.pieces.rook import Rook


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

    vals = [
        "id",
        "board",
        "game_state",
        "turn_count",
        "turn",
        "captured_pieces",
        "check",
        "checkmate",
    ]
    assert all([val in dict(chess) for val in vals])
    board = dict(chess)["board"]
    assert isinstance(board, dict)
    assert len(board) == 32
    assert all([isinstance(p, dict) for p in board.values()])


def test_make_move():
    chess = Chess()
    assert chess.turn == WHITE
    assert chess.turn_count == 0
    chess.make_move("E2", "E4")
    assert chess.turn == BLACK
    assert chess.turn_count == 1
    chess.make_move("E7", "E5")
    assert chess.turn == WHITE
    assert chess.turn_count == 2

    with raises(ValueError):
        chess.make_move("E2", "E4")
    assert chess.turn == WHITE
    assert chess.turn_count == 2
    with raises(ValueError):
        chess.make_move("A4", "A5")
    assert chess.turn == WHITE
    assert chess.turn_count == 2


def test_rook_moves():
    chess = Chess()
    with raises(ValueError):
        chess.make_move("A1", "A3")
    assert chess.turn == WHITE
    assert chess.turn_count == 0
    chess.make_move("A2", "A4")
    with raises(ValueError):
        chess.make_move("A8", "A6")
    chess.make_move("A7", "A5")
    chess.make_move("A1", "A3")
    white_rook = chess.board.get_piece("A3")
    assert isinstance(white_rook, Rook)
    assert white_rook.available_moves == {
        "B3",
        "C3",
        "D3",
        "E3",
        "F3",
        "G3",
        "H3",
        "A1",
        "A2",
    }
    chess.make_move("A8", "A6")
    black_rook = chess.board.get_piece("A6")
    assert isinstance(black_rook, Rook)
    assert black_rook.available_moves == {
        "B6",
        "C6",
        "D6",
        "E6",
        "F6",
        "G6",
        "H6",
        "A7",
        "A8",
    }
    chess.make_move("A3", "D3")
    assert chess.board.get_piece("A3") is None
    assert chess.board.get_piece("D3") is white_rook
    assert white_rook.available_moves == {
        "A3",
        "B3",
        "C3",
        "E3",
        "F3",
        "G3",
        "H3",
        "D4",
        "D5",
        "D6",
    }
    chess.make_move("A6", "D6")
    assert chess.board.get_piece("A6") is None
    assert chess.board.get_piece("D6") is black_rook
    assert black_rook.available_moves == {
        "A6",
        "B6",
        "C6",
        "E6",
        "F6",
        "G6",
        "H6",
        "D5",
        "D4",
    }


def test_targets():
    chess = Chess()
    pawn_targets(chess)
    knight_targets(chess)
    chess = Chess()
    rook_targets(chess)
    chess = Chess()
    bishop_targets(chess)


def bishop_targets(chess: Chess):
    white_bishop = chess.board.get_piece("C1")
    black_bishop = chess.board.get_piece("F8")
    assert isinstance(white_bishop, Piece)
    assert isinstance(black_bishop, Piece)
    chess.make_move("B2", "B3")
    assert white_bishop.targets == set()
    chess.make_move("G7", "G6")
    assert black_bishop.targets == set()
    chess.make_move("C1", "B2")
    assert white_bishop.targets == {"H8"}
    chess.make_move("F8", "G7")
    assert black_bishop.targets == {"B2"}
    assert white_bishop.targets == {"G7"}


def pawn_targets(chess: Chess):
    white_pawn = chess.board.get_piece("A2")
    black_pawn = chess.board.get_piece("B7")
    assert isinstance(white_pawn, Pawn)
    assert isinstance(black_pawn, Pawn)
    assert white_pawn.targets == set()
    assert black_pawn.targets == set()
    chess.make_move("A2", "A4")
    assert white_pawn.targets == set()
    assert black_pawn.targets == set()
    chess.make_move("B7", "B5")
    assert white_pawn.targets == {"B5"}
    assert black_pawn.targets == {"A4"}


def knight_targets(chess: Chess):
    white_knight = chess.board.get_piece("B1")
    black_knight = chess.board.get_piece("G8")
    assert isinstance(white_knight, Knight)
    assert isinstance(black_knight, Knight)
    assert white_knight.targets == set()
    assert black_knight.targets == set()
    chess.make_move("B1", "C3")
    assert white_knight.targets == {"B5"}
    chess.make_move("G8", "F6")
    assert black_knight.targets == set()
    chess.make_move("E2", "E4")
    assert black_knight.targets == {"E4"}


def rook_targets(chess: Chess):
    white_rook = chess.board.get_piece("A1")
    black_rook = chess.board.get_piece("H8")
    assert isinstance(white_rook, Rook)
    assert isinstance(black_rook, Rook)
    assert white_rook.targets == set()
    assert black_rook.targets == set()
    chess.make_move("A2", "A4")
    assert white_rook.targets == set()
    assert black_rook.targets == set()
    chess.make_move("H7", "H5")
    assert white_rook.targets == set()
    assert black_rook.targets == set()
    chess.make_move("A1", "A3")
    assert white_rook.targets == set()
    assert black_rook.targets == set()
    chess.make_move("H8", "H6")
    assert white_rook.targets == set()
    assert black_rook.targets == set()
    chess.make_move("A3", "C3")
    assert white_rook.targets == {"C7"}
    assert black_rook.targets == set()
    chess.make_move("H6", "E6")
    assert black_rook.targets == {"E2"}
    chess.make_move("C3", "C6")
    assert white_rook.targets == {"C7", "E6"}
    chess.make_move("B7", "B6")
    assert white_rook.targets == {"C7", "E6", "B6"}
