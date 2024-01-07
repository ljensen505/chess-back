from .piece import BLACK, WHITE, Piece


class Pawn(Piece):
    def __init__(self, color: str, position: str):
        super().__init__(color, position)
        self.icon = "♟︎"
