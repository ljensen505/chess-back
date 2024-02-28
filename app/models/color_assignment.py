from uuid import UUID

from pydantic import BaseModel, validator


class AssignColor(BaseModel):
    assignee_id: UUID
    color: str

    @validator("color")
    def validate_color(cls, v):
        v = v.lower()
        if v not in ["black", "white"]:
            raise ValueError("Invalid color")
        return v
