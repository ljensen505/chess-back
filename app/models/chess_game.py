from uuid import UUID

from pydantic import BaseModel

from chess import Chess


class ChessGame(BaseModel):
    """Chess game model for serialization of a Chess object"""

    board: dict[str, dict[str, str]]
    game_state: str
    game_id: UUID
    turn: str
    turn_count: int


def game_to_response(chess: Chess) -> ChessGame:
    """Build a ChessGame object from a Chess object"""
    turn = chess.turn.lower()
    return ChessGame(
        board=dict(chess.board),
        game_state=chess.game_state,
        game_id=chess.id,
        turn=turn,
        turn_count=chess.turn_count,
    )
