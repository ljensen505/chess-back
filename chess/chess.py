from uuid import uuid4

from chess.pieces.piece import Piece

from .board import BLACK, WHITE, Board


class Chess:
    def __init__(self):
        self.id = uuid4()
        self.board = Board()
        self.game_state = "active"
        self.check = False
        self.checkmate = False
        self.turn_count = 0
        self.turn = WHITE

    def __repr__(self) -> str:
        return f"Chess({self.id})\n\n{self.board}\n"

    def __iter__(self):
        return iter(
            {
                "id": self.id,
                "board": dict(self.board),
                "game_state": self.game_state,
                "turn_count": self.turn_count,
                "turn": self.turn,
                "captured_pieces": self.board.captured_pieces,
                "check": self.check,
                "checkmate": self.checkmate,
            }.items()
        )

    def make_move(self, start: str, end: str) -> None:
        start = start.upper()
        end = end.upper()
        self._validate_move(start, end)
        piece = self.board.get_piece(start)
        target = self.board.get_piece(end)
        if piece is None:
            raise ValueError("No piece at that position")

        self._validate_piece_and_target(piece, target, end)

        self.turn_count += 1
        self.turn = BLACK if self.turn == WHITE else WHITE
        self.board.move_piece(piece, end)

    def _validate_piece_and_target(
        self, piece: Piece, target: Piece | None, end: str
    ) -> None:
        if piece.color != self.turn:
            raise ValueError("Not your turn")
        if target and target.color == piece.color:
            raise ValueError("Can't take your own piece")
        if end not in piece.available_moves:
            raise ValueError("Invalid move")

    def _validate_move(self, start: str, end: str) -> None:
        if len(start) != 2 or len(end) != 2:
            raise ValueError("Positions must be two characters long")
        if start == end:
            raise ValueError("Start and end positions must be different")
        if (start[0] not in "ABCDEFGH" or start[1] not in "12345678") or (
            end[0] not in "ABCDEFGH" or end[1] not in "12345678"
        ):
            raise ValueError("Invalid position")
        if self.game_state != "active":
            raise ValueError("Game is over")
