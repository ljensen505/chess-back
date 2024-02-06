from uuid import UUID

from pydantic import BaseModel
from .game_info import GameInfo


class UserBase(BaseModel):
    """
    User model for serialization of a user
    Does not include game information
    """

    id: UUID
    email: str
    name: str
    auth0_id: str
    self: str


class UserDetails(UserBase):
    """
    User model for serialization of a user
    Includes game information
    """

    games: list[GameInfo]
