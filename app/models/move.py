from pydantic import BaseModel


class Move(BaseModel):
    """Move model for serialization of a move"""

    start: str
    end: str
