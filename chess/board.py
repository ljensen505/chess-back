from colorama import Back, Fore, init

from chess.pieces import BLACK, WHITE, Bishop, King, Knight, Pawn, Piece, Queen, Rook

init(autoreset=True)

COLS = "ABCDEFGH"
ROWS = "12345678"


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
        self.active_pieces["D1"] = Queen(WHITE, "D1")
        self.active_pieces["D8"] = Queen(BLACK, "D8")
        self.active_pieces["E1"] = King(WHITE, "E1")
        self.active_pieces["E8"] = King(BLACK, "E8")

        self.set_piece_moves()

    def move_piece(self, piece: Piece, end: str, target: Piece | None = None) -> None:
        if end not in piece.available_moves.union(piece.targets):
            raise ValueError("Invalid move")
        if target and target.color == piece.color:
            raise ValueError("Can't take your own piece")

        if target:
            self._capture_piece(target)

        self.active_pieces[end] = piece
        del self.active_pieces[piece.position]

        piece.set_position(end)
        piece.set_has_moved()
        self.set_piece_moves()

    def get_piece(self, position: str) -> Piece | None:
        return self.active_pieces.get(position)

    def set_piece_moves(self) -> None:
        move_table = {
            "pawn": self._pawn_moves,
            "knight": self._knight_moves,
            "rook": self._rook_moves,
            "bishop": self._bishop_moves,
            "queen": self._queen_moves,
            "king": self._king_moves,
        }
        for piece in self.active_pieces.values():
            if piece.type in move_table:
                available_moves, available_targets = move_table[piece.type](piece)
                piece.set_available_moves(available_moves)
                piece.set_targets(available_targets)
            else:
                # this should never happen
                raise ValueError(f"Invalid piece type: {piece.type}")

    def _capture_piece(self, piece: Piece) -> None:
        """Removes a piece from the board and adds it to the captured pieces list"""
        self.captured_pieces.append(piece)
        del self.active_pieces[piece.position]
        piece.set_is_captired()

    def _pawn_moves(self, piece: Piece) -> tuple[set[str], set[str]]:
        """Returns a tuple of available moves and targets for a pawn"""
        possible_moves: set[str] = set()
        direction = 1 if piece.color == WHITE else -1
        possible_moves.add(f"{piece.position[0]}{int(piece.position[1]) + direction}")
        if not piece.has_moved:
            possible_moves.add(
                f"{piece.position[0]}{int(piece.position[1]) + direction * 2}"
            )
        available_moves = {m for m in possible_moves if self.get_piece(m) is None}

        # pawn speific target finding
        diagonal_targets = {
            f"{chr(ord(piece.position[0]) + 1)}{int(piece.position[1]) + direction}",
            f"{chr(ord(piece.position[0]) - 1)}{int(piece.position[1]) + direction}",
        }
        targets = self._find_targets(piece, diagonal_targets)

        return available_moves, targets

    def _knight_moves(self, piece: Piece) -> tuple[set[str], set[str]]:
        """Returns a tuple of available moves and targets for a knight"""
        possible_moves = {
            f"{chr(ord(piece.position[0]) + 2)}{int(piece.position[1]) + 1}",
            f"{chr(ord(piece.position[0]) + 2)}{int(piece.position[1]) - 1}",
            f"{chr(ord(piece.position[0]) - 2)}{int(piece.position[1]) + 1}",
            f"{chr(ord(piece.position[0]) - 2)}{int(piece.position[1]) - 1}",
            f"{chr(ord(piece.position[0]) + 1)}{int(piece.position[1]) + 2}",
            f"{chr(ord(piece.position[0]) + 1)}{int(piece.position[1]) - 2}",
            f"{chr(ord(piece.position[0]) - 1)}{int(piece.position[1]) + 2}",
            f"{chr(ord(piece.position[0]) - 1)}{int(piece.position[1]) - 2}",
        }
        available_moves = {
            m
            for m in possible_moves
            if self.get_piece(m) is None
            and len(m) == 2
            and m[0] in COLS
            and m[1] in ROWS
        }
        targets = self._find_targets(piece, possible_moves)
        return available_moves, targets

    def _find_targets(self, piece: Piece, possible_moves) -> set[str]:
        """Returns a set of targets for a piece based on a set of possible moves"""
        targets = set()
        for move in possible_moves:
            target = self.get_piece(move)
            if target is not None and target.color != piece.color:
                targets.add(move)
        return targets

    def _check_up_down(
        self, piece: Piece, direction: list
    ) -> tuple[set[str], set[str]]:
        """Returns a tuple of available moves and targets for a piece moving up or down"""
        possible_moves = set()
        targets = set()
        for pos in direction:
            square = f"{pos[0]}{pos[1]}"
            occupying_piece = self.get_piece(square)
            if occupying_piece is not None:
                if occupying_piece.color != piece.color:
                    targets.add(square)
                break
            possible_moves.add(square)
        return possible_moves, targets

    def _check_diagonal(
        self, piece: Piece, direction: list
    ) -> tuple[set[str], set[str]]:
        """Returns a tuple of available moves and targets for a piece moving diagonally"""
        possible_moves = set()
        targets = set()
        for pos in direction:
            square = f"{pos[0]}{pos[1]}"
            occupying_piece = self.get_piece(square)
            if occupying_piece is not None:
                if occupying_piece.color != piece.color:
                    targets.add(square)
                break
            possible_moves.add(square)
        return possible_moves, targets

    def _rook_moves(self, piece: Piece) -> tuple[set[str], set[str]]:
        """Returns a tuple of available moves and targets for a rook"""
        possible_moves = set()
        targets = set()
        directions = self._get_up_down_dirs(piece)
        for direction in directions:
            direction_moves, direction_targets = self._check_up_down(piece, direction)
            possible_moves.update(direction_moves)
            targets.update(direction_targets)
        return possible_moves, targets

    def _get_up_down_dirs(self, piece: Piece) -> list[list[tuple[str, str]]]:
        return [
            [
                (piece.position[0], row)
                for row in ROWS[ROWS.index(piece.position[1]) + 1 :]
            ],  # up
            [
                (piece.position[0], row)
                for row in reversed(ROWS[: ROWS.index(piece.position[1])])
            ],  # down
            [
                (col, piece.position[1])
                for col in reversed(COLS[: COLS.index(piece.position[0])])
            ],  # left
            [
                (col, piece.position[1])
                for col in COLS[COLS.index(piece.position[0]) + 1 :]
            ],  # right
        ]

    def _bishop_moves(self, piece: Piece) -> tuple[set[str], set[str]]:
        """Returns a tuple of available moves and targets for a bishop"""
        possible_moves = set()
        targets = set()

        directions = self._get_diagonal_dirs(piece)

        for direction in directions:
            direction_moves, direction_targets = self._check_diagonal(piece, direction)
            possible_moves.update(direction_moves)
            targets.update(direction_targets)
        return possible_moves, targets

    def _get_diagonal_dirs(self, piece: Piece) -> list[list[tuple[str, str]]]:
        # up right
        up_right: list[tuple[str, str]] = []
        r, c = ROWS.index(piece.position[1]) + 1, COLS.index(piece.position[0]) + 1
        while r < len(ROWS) and c < len(COLS):
            up_right.append((COLS[c], ROWS[r]))
            r += 1
            c += 1

        # down right
        down_right: list[tuple[str, str]] = []
        r, c = ROWS.index(piece.position[1]) - 1, COLS.index(piece.position[0]) + 1
        while r >= 0 and c < len(COLS):
            down_right.append((COLS[c], ROWS[r]))
            r -= 1
            c += 1

        # up left
        up_left: list[tuple[str, str]] = []
        r, c = ROWS.index(piece.position[1]) + 1, COLS.index(piece.position[0]) - 1
        while r < len(ROWS) and c >= 0:
            up_left.append((COLS[c], ROWS[r]))
            r += 1
            c -= 1

        # down left
        down_left: list[tuple[str, str]] = []
        r, c = ROWS.index(piece.position[1]) - 1, COLS.index(piece.position[0]) - 1
        while r >= 0 and c >= 0:
            down_left.append((COLS[c], ROWS[r]))
            r -= 1
            c -= 1

        return [up_right, down_right, up_left, down_left]

    def _queen_moves(self, piece: Piece) -> tuple[set[str], set[str]]:
        """Returns a list of available moves for a queen"""
        possible_moves = set()
        targets = set()
        diagonals = self._get_diagonal_dirs(piece)
        up_down = self._get_up_down_dirs(piece)
        directions = diagonals + up_down
        for direction in directions:
            direction_moves, direction_targets = self._check_up_down(piece, direction)
            possible_moves.update(direction_moves)
            targets.update(direction_targets)

        return possible_moves, targets

    def _king_moves(self, piece: Piece) -> tuple[set[str], set[str]]:
        """Returns a list of available moves for a king"""
        adjacent_squares = {
            f"{chr(ord(piece.position[0]) + 1)}{int(piece.position[1])}",
            f"{chr(ord(piece.position[0]) - 1)}{int(piece.position[1])}",
            f"{piece.position[0]}{int(piece.position[1]) + 1}",
            f"{piece.position[0]}{int(piece.position[1]) - 1}",
            f"{chr(ord(piece.position[0]) + 1)}{int(piece.position[1]) + 1}",
            f"{chr(ord(piece.position[0]) + 1)}{int(piece.position[1]) - 1}",
            f"{chr(ord(piece.position[0]) - 1)}{int(piece.position[1]) + 1}",
            f"{chr(ord(piece.position[0]) - 1)}{int(piece.position[1]) - 1}",
        }
        available_moves = {
            m
            for m in adjacent_squares
            if self.get_piece(m) is None
            and len(m) == 2
            and m[0] in COLS
            and m[1] in ROWS
        }
        targets = self._find_targets(piece, adjacent_squares)
        return available_moves, targets
