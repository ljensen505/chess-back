from colorama import Back, Fore, Style, init

from chess.pieces import Bishop, King, Knight, Pawn, Piece, Queen, Rook

init(autoreset=True)

COLS = "ABCDEFGH"
ROWS = "12345678"
WHITE = "WHITE"
BLACK = "BLACK"


class Board:
    def __init__(self):
        self.active_pieces: dict[str, Piece] = {}
        self.captured_pieces: list[Piece] = []

        self._init_pieces()

    def __repr__(self) -> str:
        board_str = "\n   " + " ".join(COLS) + "\n"
        for row in reversed(ROWS):
            board_str += row + " "
            for col in COLS:
                square = f"{col}{row}"
                piece = self.active_pieces.get(square)
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
        return iter({p[0]: dict(p[1]) for p in self.active_pieces.items()}.items())

    def _init_pieces(self) -> None:
        for col in COLS:
            self.active_pieces[f"{col}2"] = Pawn(WHITE, f"{col}2")
            self.active_pieces[f"{col}7"] = Pawn(BLACK, f"{col}7")
        for col in COLS[1:8:5]:
            self.active_pieces[f"{col}1"] = Knight(WHITE, f"{col}1")
            self.active_pieces[f"{col}8"] = Knight(BLACK, f"{col}8")
        for col in COLS[0:8:7]:
            self.active_pieces[f"{col}1"] = Rook(WHITE, f"{col}1")
            self.active_pieces[f"{col}8"] = Rook(BLACK, f"{col}8")
        for col in COLS[2:7:3]:
            self.active_pieces[f"{col}1"] = Bishop(WHITE, f"{col}1")
            self.active_pieces[f"{col}8"] = Bishop(BLACK, f"{col}8")
        self.active_pieces["E1"] = Queen(WHITE, "E1")
        self.active_pieces["E8"] = Queen(BLACK, "E8")
        self.active_pieces["D1"] = King(WHITE, "D1")
        self.active_pieces["D8"] = King(BLACK, "D8")

        self.set_available_moves()

    def move_piece(self, start: str, end: str) -> None:
        piece = self.active_pieces.get(start)
        if piece is None:
            raise ValueError("No piece at that position")
        if end not in piece.available_moves:
            raise ValueError("Invalid move")

        self.active_pieces[end] = piece
        del self.active_pieces[start]
        piece.set_position(end)
        piece.set_has_moved()
        self.set_available_moves()

    def get_piece(self, position: str) -> Piece | None:
        return self.active_pieces.get(position)

    def set_available_moves(self) -> None:
        move_table = {
            "pawn": self._pawn_moves,
        }
        for piece in self.active_pieces.values():
            if piece.type in move_table:
                piece.set_available_moves(move_table[piece.type](piece))

    def _pawn_moves(self, piece: Piece) -> list[str]:
        moves: list[str] = []
        direction = 1 if piece.color == WHITE else -1
        if not piece.has_moved:
            moves.append(
                f"{piece.position[0]}{int(piece.position[1]) + (2 * direction)}"
            )
        moves.append(f"{piece.position[0]}{int(piece.position[1]) + direction}")

        return moves

    def _knight_moves(self, piece: Piece) -> list[str]:
        raise NotImplementedError

    def _bishop_moves(self, piece: Piece) -> list[str]:
        raise NotImplementedError

    def _rook_moves(self, piece: Piece) -> list[str]:
        raise NotImplementedError

    def _queen_moves(self, piece: Piece) -> list[str]:
        raise NotImplementedError

    def _king_moves(self, piece: Piece) -> list[str]:
        raise NotImplementedError
