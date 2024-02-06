from uuid import UUID

import black
from pydantic import BaseModel

from chess import Chess


class BaseGame(BaseModel):
    """Base game model for serialization of a game id and self link"""

    game_id: UUID
    self: str
    owner_id: UUID
    black_player_id: UUID | None = None
    white_player_id: UUID | None = None


class ChessGame(BaseGame):
    """Chess game model for serialization of a Chess object"""

    board: dict[str, dict[str, str]]
    game_state: str
    turn: str
    turn_count: int


def game_to_response(chess: Chess, owner_id: UUID) -> ChessGame:
    """Build a ChessGame object from a Chess object"""
    turn = chess.turn.lower()
    return ChessGame(
        board=dict(chess.board),
        game_state=chess.game_state,
        game_id=chess.id,
        turn=turn,
        turn_count=chess.turn_count,
        self=f"/games/{chess.id}",
        owner_id=owner_id,
    )
