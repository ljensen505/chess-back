from datetime import datetime
from re import U
from uuid import UUID

from chess import Piece, Square
from fastapi import HTTPException
from pydantic import BaseModel


class PieceModel(BaseModel):
    """Piece model for serialization"""

    type: str
    color: str
    square: str


class BasicUserInfo(BaseModel):
    """Basic user info for serialization"""

    username: str
    user_id: UUID
    self: str


class BaseGame(BaseModel):
    """Base game model for serialization of a game id and self link"""

    game_id: UUID
    self: str
    owner: BasicUserInfo
    black_player: BasicUserInfo | None = None
    white_player: BasicUserInfo | None = None
    created_at: datetime | None = None  # will be set by the database automatically
    last_updated_at: datetime | None = None


class DetailedGame(BaseGame):
    """Chess game model for serialization of a Chess object"""

    turn: str  # "white" or "black"
    turn_count: int
    game_state: str
    board: dict[str, PieceModel]
