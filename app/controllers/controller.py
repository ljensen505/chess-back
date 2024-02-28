from uuid import UUID

import black
from fastapi import HTTPException
from icecream import ic

from app.models.game import BaseGame, BasicUserInfo, DetailedGame
from app.models.move import Move
from app.models.users import BaseUser, DetailedUser, NewUser

from .games import GameController
from .users import UserController


class APIController:
    def __init__(self) -> None:
        self.uc = UserController()
        self.gc = GameController()

    def create_game(self, auth0_id: str) -> UUID:
        user = self.uc.get_user_by_auth_id(auth0_id)
        return self.gc.create_game(user)

    def get_base_user(self, user_id: UUID) -> BaseUser:
        user = self.uc.get_user_by_uuid(user_id)
        games = self.get_games_by_user_id(user.user_id)
        user.games = games
        return user

    def get_base_users(self) -> list[BaseUser]:
        detailed_users = self.uc.get_all_users()
        for user in detailed_users:
            user.games = self.get_games_by_user_id(user.user_id)
        users = [BaseUser(**user.model_dump()) for user in detailed_users]
        return users

    def get_detailed_user(self, requesting_auth0_id: str) -> DetailedUser:
        return self.uc.get_user_by_auth_id(requesting_auth0_id)

    def get_games_by_user_id(self, user_id: UUID) -> list[BaseGame]:
        user = self.uc.get_user_by_uuid(user_id)
        games_data = self.gc.queries.select_all_by_user_id(user.user_id)
        return [self.get_base_game(game["game_id"]) for game in games_data]

    def _process_players(self, game: BaseGame) -> None:
        owner = self.uc.get_user_by_uuid(game.owner.user_id)
        white = (
            self.uc.get_user_by_uuid(game.white_player.user_id)
            if game.white_player
            else None
        )
        black = (
            self.uc.get_user_by_uuid(game.black_player.user_id)
            if game.black_player
            else None
        )
        game.owner = BasicUserInfo(
            user_id=owner.user_id,
            self=f"/users/{owner.user_id}",
            username=owner.username,
        )
        game.white_player = (
            BasicUserInfo(
                user_id=white.user_id,
                self=f"/users/{white.user_id}",
                username=white.username,
            )
            if white
            else None
        )
        game.black_player = (
            BasicUserInfo(
                user_id=black.user_id,
                self=f"/users/{black.user_id}",
                username=black.username,
            )
            if black
            else None
        )

    def get_games_by_auth_token(self, auth0_id: str) -> list[BaseGame]:
        owner = self.get_detailed_user(auth0_id)
        return self.get_games_by_user_id(owner.user_id)

    def get_detailed_game(self, game_id: UUID) -> DetailedGame:
        game = self.gc.get_detailed_game_by_uuid(game_id)
        self._process_players(game)

        return game

    def get_base_game(self, game_id: UUID) -> BaseGame:
        game = self.gc.get_base_game_by_uuid(game_id)
        self._process_players(game)
        return game

    def delete_game(self, game_id: UUID, auth0_id: str) -> None:
        user = self.uc.get_user_by_auth_id(auth0_id)
        self.gc.delete_game(game_id, user.user_id)

    def assign_player(
        self, game_id: UUID, owner_auth0_id: str, assignee_id: UUID, color: str
    ) -> BaseGame:
        owner = self.uc.get_user_by_auth_id(owner_auth0_id)
        assignee = self.uc.get_user_by_uuid(assignee_id)
        ic(owner, assignee, color)
        if owner.user_id == assignee.user_id:
            raise HTTPException(
                status_code=400,
                detail="Owner cannot assign themselves to a game. Assign another player instead.",
            )
        game = self.gc.get_detailed_game_by_uuid(game_id)
        if owner.user_id != game.owner.user_id:
            raise HTTPException(status_code=403, detail="User does not own game")
        if game.black_player is not None or game.white_player is not None:
            raise HTTPException(
                status_code=400,
                detail="Players already assigned",
            )
        self.gc.assign_player(game.game_id, assignee.user_id, color)
        owner_color = "white" if color == "black" else "black"
        self.gc.assign_player(game.game_id, owner.user_id, owner_color)
        return self.gc.get_base_game_by_uuid(game_id)

    def make_move(self, auth0_id: str, game_id: UUID, move: Move) -> DetailedGame:
        user = self.uc.get_user_by_auth_id(auth0_id)
        game = self.gc.get_detailed_game_by_uuid(game_id)
        if game.black_player is None or game.white_player is None:
            raise HTTPException(
                status_code=400,
                detail="Both players must be assigned before making a move",
            )
        if user.user_id not in [game.black_player.user_id, game.white_player.user_id]:
            raise HTTPException(
                status_code=403,
                detail="User is not a player in this game",
            )
        self.gc.make_move(game, move)
        return self.get_detailed_game(game_id)

    def create_user(self, user: NewUser, auth_result: dict) -> BaseUser:
        return self.uc.create_user(user, auth_result)
