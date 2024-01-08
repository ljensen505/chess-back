from .piece import Piece


class King(Piece):
    def __init__(self, color: str, position: str):
        super().__init__(color, position)
        self.icon = "♚"
        self.check = False
