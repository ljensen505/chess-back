class Piece:
    def __init__(self, color: str, position: str):
        self.color = color
        self.position = position
        self.has_moved = False
        self.icon = "?"

        if len(self.position) != 2:
            raise ValueError("Position must be two characters long")

    def __repr__(self) -> str:
        piece_type = type(self).__name__
        return f"{piece_type}({self.color}, {self.position})"

    def __str__(self) -> str:
        return f"{self.icon}"

    def __iter__(self):
        return iter(
            {
                "color": self.color.lower(),
                "type": type(self).__name__.lower(),
            }.items()
        )
