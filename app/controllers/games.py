import os
import pickle
from uuid import UUID

from chess import (
    COLOR_NAMES,
    PIECE_NAMES,
    SQUARE_NAMES,
    SQUARES,
    Board,
    IllegalMoveError,
)
from fastapi import HTTPException
from icecream import ic

from app.db.games import GameQueries
from app.models.game import BaseGame, BasicUserInfo, DetailedGame, PieceModel
from app.models.move import Move
from app.models.users import DetailedUser


class GameController:
    def __init__(self) -> None:
        self.queries = GameQueries()
        self.games_dir = os.path.join(os.path.dirname(__file__), "games")

    def construct_base_game(self, game_data: dict) -> BaseGame:
        owner: BasicUserInfo = BasicUserInfo(
            user_id=game_data["owner_id"],
            self=f"/users/{game_data['owner_id']}",
            username="TODO",
        )
        last_updated_at = (
            game_data.get("last_updated_at")
            if game_data.get("last_updated_at")
            else None
        )
        white = None
        black = None
        white_id = game_data.get("white_player_id")
        black_id = game_data.get("black_player_id")
        if white_id:
            white = BasicUserInfo(
                user_id=white_id, self=f"/users/{white_id}", username="TODO"
            )
        if black_id:
            black = BasicUserInfo(
                user_id=black_id, self=f"/users/{black_id}", username="TODO"
            )

        try:
            return BaseGame(
                game_id=game_data["game_id"],
                self=f"/games/{game_data['game_id']}",
                owner=owner,
                created_at=game_data["created_at"],
                last_updated_at=last_updated_at,
                white_player=white,
                black_player=black,
            )
        except Exception as e:
            ic(e)
            raise HTTPException(status_code=500, detail="Error constructing game")

    def construct_detailed_game(
        self, base_game: BaseGame, board: Board
    ) -> DetailedGame:
        game_state: str = "in progress" if not board.is_game_over() else "finished"
        return DetailedGame(
            game_id=base_game.game_id,
            self=base_game.self,
            owner=base_game.owner,
            turn=COLOR_NAMES[board.turn],
            turn_count=board.fullmove_number,
            game_state=game_state,
            black_player=base_game.black_player,
            white_player=base_game.white_player,
            created_at=base_game.created_at,
            last_updated_at=base_game.last_updated_at,
            board=self.construct_board(board),
        )

    @staticmethod
    def construct_board(board: Board) -> dict[str, PieceModel]:
        board_dict = {}
        for sq in SQUARES:
            piece = board.piece_at(sq)
            if piece is not None:
                sq_name = SQUARE_NAMES[sq].upper()
                board_dict[sq_name] = PieceModel(
                    type=PIECE_NAMES[piece.piece_type],
                    color=COLOR_NAMES[piece.color],
                    square=sq_name,
                )
        return board_dict

    def get_base_game_by_uuid(self, game_id: UUID) -> BaseGame:
        game_data = self.queries.select_by_id(game_id)
        if game_data is None:
            raise HTTPException(status_code=404, detail="Game not found")
        return self.construct_base_game(game_data)

    def get_detailed_game_by_uuid(self, game_id: UUID) -> DetailedGame:
        game_data = self.queries.select_by_id(game_id)
        if game_data is None:
            raise HTTPException(status_code=404, detail="Game not found")
        with open(os.path.join(self.games_dir, f"{game_id}.pickle"), "rb") as f:
            board: Board = pickle.load(f)
        base_game = self.construct_base_game(game_data)
        return self.construct_detailed_game(base_game, board)

    def create_game(self, owner: DetailedUser) -> UUID:
        game_id = self.queries.insert_game(owner.user_id)
        board = Board()
        with open(os.path.join(self.games_dir, f"{game_id}.pickle"), "wb") as f:
            pickle.dump(board, f)
        return game_id

    def get_games_by_user_id(self, user_id: UUID) -> list[BaseGame]:
        games_data = self.queries.select_all_by_user_id(user_id)
        return [self.construct_base_game(game) for game in games_data]

    def delete_game(self, game_id: UUID, user_id: UUID) -> None:
        game = self.get_detailed_game_by_uuid(game_id)
        if game.owner.user_id != user_id:
            raise HTTPException(
                status_code=403, detail="User is not authorized to delete this game"
            )
        self.queries.delete_game(game.game_id)
        os.remove(os.path.join(self.games_dir, f"{game_id}.pickle"))

    def assign_player(self, game_id: UUID, assignee_id: UUID, color: str) -> None:
        print(f"assigning {assignee_id} to {color}")
        color = color.lower()
        game = self.get_detailed_game_by_uuid(game_id)
        if color not in ["white", "black"]:
            raise ValueError("Invalid color")
        self.queries.assign_player(game.game_id, assignee_id, color)

    def make_move(self, game: DetailedGame, move: Move) -> DetailedGame:
        with open(os.path.join(self.games_dir, f"{game.game_id}.pickle"), "rb") as f:
            b = pickle.load(f)
        uci = f"{move.start}{move.end}"
        try:
            b.push_uci(uci)
        except IllegalMoveError as e:
            raise HTTPException(status_code=400, detail=f"Illegal move: {e}")
        with open(os.path.join(self.games_dir, f"{game.game_id}.pickle"), "wb") as f:
            pickle.dump(b, f)
        self.queries.update_last_updated_at(game.game_id)
        return self.get_detailed_game_by_uuid(game.game_id)
