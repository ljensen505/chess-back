from uuid import UUID
from pydantic import BaseModel


class GameInfo(BaseModel):
    """Game info model for serialization of a game id and self link"""

    game_id: UUID
    self: str
