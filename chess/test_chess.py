from calendar import c
from uuid import UUID

from pytest import raises

import chess
from chess import Chess
from chess.pieces import BLACK, WHITE, Piece
from chess.pieces.king import King
from chess.pieces.knight import Knight
from chess.pieces.pawn import Pawn
from chess.pieces.queen import Queen
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


def test_king_targets():
    chess = Chess()
    white_king = chess.board.get_piece("E1")
    black_king = chess.board.get_piece("E8")
    assert isinstance(white_king, King)
    assert isinstance(black_king, King)
    chess.make_move("E2", "E4")
    assert white_king.targets == set()
    chess.make_move("E7", "E5")
    assert black_king.targets == set()
    chess.make_move("E1", "E2")
    chess.make_move("E8", "E7")
    chess.make_move("E2", "E3")
    chess.make_move("E7", "E6")
    chess.make_move("E3", "D4")
    assert white_king.targets == {"E5"}
    assert black_king.targets == set()
    chess.make_move("E6", "D5")
    assert black_king.targets == {"E4", "D4"}


def test_queen_targets():
    chess = Chess()
    white_queen = chess.board.get_piece("D1")
    black_queen = chess.board.get_piece("D8")
    assert isinstance(white_queen, Queen)
    assert isinstance(black_queen, Queen)
    chess.make_move("E2", "E4")
    assert white_queen.targets == set()
    chess.make_move("E7", "E5")
    assert black_queen.targets == set()
    chess.make_move("D1", "H5")
    assert white_queen.targets == {"F7", "H7", "E5"}
    chess.make_move("D8", "H4")
    assert black_queen.targets == {"H2", "F2", "H5", "E4"}


def test_bishop_targets():
    chess = Chess()
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


def test_pawn_targets():
    chess = Chess()
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


def test_knight_targets():
    chess = Chess()
    chess.make_move("A2", "A4")
    chess.make_move("B7", "B5")
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


def test_rook_targets():
    chess = Chess()
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


def test_capture():
    chess = Chess()
    num_active_pieces = len(chess.board.active_pieces)
    num_captured_pieces = len(chess.board.captured_pieces)
    white_pawn = chess.board.get_piece("E2")
    black_pawn = chess.board.get_piece("D7")
    assert isinstance(white_pawn, Pawn)
    assert isinstance(black_pawn, Pawn)
    chess.make_move("E2", "E4")
    chess.make_move("D7", "D5")
    assert white_pawn.targets == {"D5"}
    assert black_pawn.targets == {"E4"}
    chess.make_move("E4", "D5")
    assert white_pawn.targets == set()
    assert black_pawn.is_captured
    assert len(chess.board.active_pieces) == num_active_pieces - 1
    assert len(chess.board.captured_pieces) == num_captured_pieces + 1
    assert chess.board.get_piece("D5") is white_pawn
    assert black_pawn not in chess.board.active_pieces.values()
    assert black_pawn in chess.board.captured_pieces
    assert not black_pawn.position  # should be an empty string
    assert white_pawn.position == "D5"
    assert chess.board.get_piece("D5") is white_pawn

    black_queen = chess.board.get_piece("D8")
    assert isinstance(black_queen, Queen)
    assert black_queen.targets == {"D5"}
    chess.make_move("D8", "D5")
    assert white_pawn.is_captured
    assert len(chess.board.active_pieces) == num_active_pieces - 2
    assert len(chess.board.captured_pieces) == num_captured_pieces + 2
    assert black_queen.position == "D5"
    assert chess.board.get_piece("D5") is black_queen


def test_castling():
    chess = Chess()
    white_castle_dest = "G1"
    black_castle_dest = "C8"
    white_king = chess.board.get_piece("E1")
    black_king = chess.board.get_piece("E8")
    assert isinstance(white_king, King)
    assert isinstance(black_king, King)

    chess.make_move("E2", "E4")
    assert white_castle_dest not in white_king.available_moves
    assert black_castle_dest not in black_king.available_moves
    chess.make_move("E7", "E5")
    assert white_castle_dest not in white_king.available_moves
    assert black_castle_dest not in black_king.available_moves

    with raises(ValueError):
        chess.make_move("E1", "G1")

    chess.make_move("F1", "C4")
    assert white_castle_dest not in white_king.available_moves
    assert black_castle_dest not in black_king.available_moves
    chess.make_move("F8", "C5")
    assert white_castle_dest not in white_king.available_moves
    assert black_castle_dest not in black_king.available_moves

    chess.make_move("G1", "F3")
    assert white_castle_dest in white_king.available_moves
    assert black_castle_dest not in black_king.available_moves

    chess.make_move("G8", "F6")
    assert white_castle_dest in white_king.available_moves
    assert black_castle_dest not in black_king.available_moves

    chess.make_move("E1", "G1")
    assert white_king.position == white_castle_dest
    castled_rook = chess.board.get_piece("F1")
    assert isinstance(castled_rook, Rook)
    assert castled_rook.has_moved
    assert white_king.has_moved

    moves = [
        ("D8", "E7"),
        ("B2", "B3"),
        ("B7", "B6"),
        ("C1", "A3"),
        ("C8", "A6"),
        ("B1", "C3"),
        ("B8", "C6"),
        ("A3", "B4"),
    ]

    for move in moves:
        chess.make_move(*move)
    assert black_castle_dest in black_king.available_moves
    chess.make_move("E8", "C8")
    castled_rook = chess.board.get_piece("D8")
    assert isinstance(castled_rook, Rook)
    assert castled_rook.has_moved
    assert black_king.has_moved
    assert black_king.position == black_castle_dest
