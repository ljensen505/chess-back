WHITE = "WHITE"
BLACK = "BLACK"


class Piece:
    def __init__(self, color: str, position: str):
        self.color = color
        self.position = position
        self.has_moved = False
        self.is_captured = False
        self.icon = "?"
        self.available_moves: set[str] = set()
        self.targets: set[str] = set()
        self.type = type(self).__name__.lower()

        if len(self.position) != 2:
            raise ValueError("Position must be two characters long")

    def __repr__(self) -> str:
        return f"{self.type.title()}({self.color}, {self.position})"

    def __str__(self) -> str:
        return f"{self.icon}"

    def __iter__(self):
        return iter(
            {
                "color": self.color.lower(),
                "type": self.type,
            }.items()
        )

    def set_available_moves(self, moves: set[str]) -> None:
        self.available_moves = moves

    def set_targets(self, targets: set[str]) -> None:
        self.targets = targets

    def set_has_moved(self) -> None:
        self.has_moved = True

    def set_position(self, position: str) -> None:
        self.position = position

    def set_is_captired(self) -> None:
        self.position = ""
        self.is_captured = True
