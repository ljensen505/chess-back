from uuid import uuid4

from .board import BLACK, WHITE, Board


class Chess:
    def __init__(self):
        self.id = uuid4()
        self.board = Board()
        self.game_state = "active"
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
            }.items()
        )

    def make_move(self, start: str, end: str) -> None:
        start = start.upper()
        end = end.upper()
        piece = self.board.get_piece(start)
        target = self.board.get_piece(end)
        if not piece:
            raise ValueError("No piece at that position")
        if piece.color != self.turn:
            raise ValueError("Not your turn")
        if target and target.color == piece.color:
            raise ValueError("Can't take your own piece")

        self.turn_count += 1
        self.turn = BLACK if self.turn == WHITE else WHITE

        self.board.move_piece(start, end)
