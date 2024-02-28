from uuid import UUID

from fastapi import APIRouter, Security, status
from icecream import ic

from app.admin.utils import VerifyToken
from app.controllers.controller import APIController
from app.models.users import BaseUser, DetailedUser, NewUser

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

auth = VerifyToken()

controller = APIController()


@router.get("/", status_code=status.HTTP_200_OK)
async def get_users() -> list[BaseUser]:
    """
    Get a list of all users
    Only returns publicly available information
    Does not require auth
    """
    return controller.get_base_users()


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def get_user(user_id: UUID) -> BaseUser:
    """
    Get a user by their ID
    Returns publicly available information
    Does not require auth
    """
    return controller.get_base_user(user_id)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
    user: NewUser, auth_result=Security(auth.verify)
) -> BaseUser | None:
    """Create a new user"""
    return controller.create_user(user, auth_result)


@router.get("/details/", status_code=status.HTTP_200_OK)
async def get_detailed_user(auth_result=Security(auth.verify)) -> DetailedUser:
    """
    Get user details by their uuid
    Returns private information and required auth
    """
    return controller.get_detailed_user(auth_result.get("sub"))
