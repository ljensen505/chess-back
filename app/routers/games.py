import os
from uuid import UUID

from fastapi import APIRouter, Security, status

from app.admin.utils import VerifyToken
from app.controllers.controller import APIController
from app.models.color_assignment import AssignColor
from app.models.game import BaseGame, DetailedGame
from app.models.move import Move

GAMES_DIR = os.path.join(os.path.dirname(__file__), os.path.pardir, "games")

router = APIRouter(
    prefix="/games",
    tags=["games"],
    responses={404: {"description": "Not found"}},
)

auth = VerifyToken()

controller = APIController()


@router.get("/", status_code=status.HTTP_200_OK)
async def get_games_route(auth_result=Security(auth.verify)) -> list[BaseGame]:
    """Get a list of all games belonging to an autnenticated user"""
    return controller.get_games_by_auth_token(auth_result.get("sub"))


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_game_route(auth_result=Security(auth.verify)) -> UUID:
    """Create a new game and return the game id"""
    return controller.create_game(auth_result.get("sub"))


@router.get("/{game_id}")
async def get_game_route(game_id: UUID) -> DetailedGame:
    """Get the current state of the game"""
    return controller.get_detailed_game(game_id)


@router.delete("/{game_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_game_route(game_id: UUID, auth_result=Security(auth.verify)) -> None:
    """Delete the game by id, if found"""
    controller.delete_game(game_id, auth_result.get("sub"))


@router.patch("/{game_id}", status_code=status.HTTP_200_OK)
async def make_move(
    game_id: UUID, move: Move, auth_result=Security(auth.verify)
) -> DetailedGame | None:
    """Make a move in the game"""
    return controller.make_move(auth_result.get("sub"), game_id, move)


@router.patch("/{game_id}/assign", status_code=status.HTTP_200_OK)
async def assign_game_to_player_route(
    game_id: UUID, assignment: AssignColor, auth_result=Security(auth.verify)
) -> BaseGame:
    """Assign a game to a non-owner player. The owner will be autoassigned to the other color."""
    return controller.assign_player(
        game_id, auth_result.get("sub"), assignment.assignee_id, assignment.color
    )
