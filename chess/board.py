from colorama import Back, Fore, Style, init

from chess.pieces import Bishop, King, Knight, Pawn, Piece, Queen, Rook

init(autoreset=True)

COLS = "ABCDEFGH"
ROWS = "12345678"
WHITE = "WHITE"
BLACK = "BLACK"


class Board:
    def __init__(self):
        self.pieces: dict[str, Piece] = {}

        for col in COLS:
            self.pieces[f"{col}2"] = Pawn(WHITE, f"{col}2")
            self.pieces[f"{col}7"] = Pawn(BLACK, f"{col}7")
        for col in COLS[1:8:5]:
            self.pieces[f"{col}1"] = Knight(WHITE, f"{col}1")
            self.pieces[f"{col}8"] = Knight(BLACK, f"{col}8")
        for col in COLS[0:8:7]:
            self.pieces[f"{col}1"] = Rook(WHITE, f"{col}1")
            self.pieces[f"{col}8"] = Rook(BLACK, f"{col}8")
        for col in COLS[2:7:3]:
            self.pieces[f"{col}1"] = Bishop(WHITE, f"{col}1")
            self.pieces[f"{col}8"] = Bishop(BLACK, f"{col}8")
        self.pieces["E1"] = Queen(WHITE, "E1")
        self.pieces["E8"] = Queen(BLACK, "E8")
        self.pieces["D1"] = King(WHITE, "D1")
        self.pieces["D8"] = King(BLACK, "D8")

    def __repr__(self) -> str:
        board_str = "   " + " ".join(COLS) + "\n"
        for row in reversed(ROWS):
            board_str += row + " "
            for col in COLS:
                square = f"{col}{row}"
                piece = self.pieces.get(square)
                background_color = (
                    Back.CYAN if (COLS.index(col) + int(row)) % 2 == 0 else Back.GREEN
                )
                if piece:
                    color = Fore.RED if piece.color == BLACK else Fore.WHITE
                    board_str += f"{background_color}{color}{piece.icon} "
                else:
                    board_str += f"{background_color}  "
            board_str += f"{Fore.RESET}{Back.RESET} {row}\n"
        return board_str + "   " + " ".join(COLS)

    def __iter__(self):
        return iter({p[0]: dict(p[1]) for p in self.pieces.items()}.items())

    def move_piece(self, start: str, end: str) -> None:
        piece = self.pieces.get(start)
        if not piece:
            raise ValueError("No piece at that position")

        self.pieces[end] = piece
        del self.pieces[start]
        piece.position = end

    def get_piece(self, position: str) -> Piece | None:
        return self.pieces.get(position)
