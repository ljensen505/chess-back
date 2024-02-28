import uuid
from uuid import UUID

from pydantic import BaseModel, Field

from app.models.game import BaseGame


class NewUser(BaseModel):
    """
    User model for creating a new user
    """

    email: str
    name: str
    username: str


class BaseUser(BaseModel):
    """
    User model for serialization of a user
    Includes game information
    Does not include private information
    """

    self: str
    username: str
    user_id: UUID
    games: list[BaseGame] = Field(default_factory=list)


class DetailedUser(BaseUser):
    """
    User model for serialization of a user
    Includes all information
    Must only be accessed by the user themselves
    """

    auth0_id: str
    email: str
    name: str
