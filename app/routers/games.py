import os
import pickle
from pprint import pprint
from uuid import UUID

from fastapi import APIRouter, HTTPException, Security, status

from app.admin import VerifyToken
from app.db import queries
from app.models import ChessGame, GameInfo, Move, game_to_response
from app.models.chess_game import BaseGame
from app.models.users import UserBase
from chess import Chess

GAMES_DIR = os.path.join(os.path.dirname(__file__), os.path.pardir, "games")

router = APIRouter(
    prefix="/games",
    tags=["games"],
    responses={404: {"description": "Not found"}},
)

auth = VerifyToken()


def get_games(auth0_id: str) -> list[GameInfo]:
    user = queries.get_user_by_auth_id(auth0_id)
    games = queries.get_games_by_user_id(user.id)
    return games


@router.get("/", status_code=status.HTTP_200_OK)
async def get_games_route(auth_result=Security(auth.verify)) -> list[GameInfo]:
    """Get a list of all games belonging to an autnenticated user"""
    auth0_id = auth_result.get("sub")
    return get_games(auth0_id)


def create_game(owner_id: UUID) -> GameInfo:
    chess = Chess(owner=str(owner_id))

    with open(os.path.join(GAMES_DIR, f"{chess.id}.pickle"), "wb") as f:
        pickle.dump(chess, f)

    base_game = BaseGame(game_id=chess.id, self=f"/games/{chess.id}", owner_id=owner_id)
    queries.insert_game(base_game)
    return GameInfo(game_id=chess.id, self=f"/games/{chess.id}", owner_id=owner_id)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_game_route(auth_result=Security(auth.verify)) -> GameInfo | None:
    """Create a new game and return the game id"""
    # TODO: this should be behind auth and use the user id
    auth0_id = auth_result.get("sub")
    user = queries.get_user_by_auth_id(auth0_id)
    return create_game(user.id)


def get_game(game_id: UUID) -> ChessGame:
    try:
        with open(os.path.join(GAMES_DIR, f"{game_id}.pickle"), "rb") as f:
            chess = pickle.load(f)
    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Game not found"
        )
    game = queries.get_game_by_id(game_id)
    chess_model = game_to_response(chess, game.owner_id)
    return chess_model


@router.get("/{game_id}")
async def get_game_route(game_id: UUID) -> ChessGame:
    """Get the current state of the game"""
    return get_game(game_id)


def delete_game(game: BaseGame, User: UserBase) -> None:
    """Delete the current state of the game"""
    if game.owner_id != User.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User does not own game"
        )
    try:
        os.remove(os.path.join(GAMES_DIR, f"{game.game_id}.pickle"))
        queries.delete_game(game)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Game not found")


@router.delete("/{game_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_game_route(game_id: UUID, auth_result=Security(auth.verify)) -> None:
    """Delete the current state of the game"""
    auth0_id = auth_result.get("sub")
    user = queries.get_user_by_auth_id(auth0_id)
    game = queries.get_game_by_id(game_id)
    return delete_game(game, user)


def make_move(game: BaseGame, user: UserBase, move: Move) -> ChessGame:
    if game.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User does not own game"
        )
    try:
        with open(os.path.join(GAMES_DIR, f"{game.game_id}.pickle"), "rb") as f:
            chess: Chess = pickle.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Game not found")

    try:
        chess.make_move(move.start, move.end)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    with open(os.path.join(GAMES_DIR, f"{game.game_id}.pickle"), "wb") as f:
        pickle.dump(chess, f)
    game = queries.get_game_by_id(game.game_id)
    return game_to_response(chess, game.owner_id)


@router.patch("/{game_id}", status_code=status.HTTP_200_OK)
async def make_move_route(
    game_id: UUID, move: Move, auth_result=Security(auth.verify)
) -> ChessGame:
    """Make a move in the game"""
    # TODO: untested
    auth0_id = auth_result.get("sub")
    user = queries.get_user_by_auth_id(auth0_id)
    game = queries.get_game_by_id(game_id)

    return make_move(game, user, move)
