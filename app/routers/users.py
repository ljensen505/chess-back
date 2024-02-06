from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.admin import VerifyToken
from app.db import queries
from app.models import UserDetails

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

auth = VerifyToken()


def get_all_users() -> list[UserDetails]:
    """Get a list of all users"""
    users = queries.get_users()
    users_details: list[UserDetails] = []
    for user in users:
        games = queries.get_games_by_user_id(user.id)
        users_details.append(UserDetails(**user.model_dump(), games=games))

    return users_details


@router.get("/", status_code=status.HTTP_200_OK)
async def get_users() -> list[UserDetails]:
    """Get a list of all users"""
    return get_all_users()


def get_user_by_id(user_id: UUID) -> UserDetails:
    """Get a user by their ID"""
    user = queries.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    games = queries.get_games_by_user_id(user_id)
    return UserDetails(**user.model_dump(), games=games)


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def get_user(user_id: UUID) -> UserDetails:
    """Get a user by their ID"""
    return get_user_by_id(user_id)


# TODO: add a route to insert new user into database
