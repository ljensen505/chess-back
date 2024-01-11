from pydantic import BaseModel


class AvailableRoutes(BaseModel):
    """Available routes model for serialization of available routes"""

    available_routes: list[str]
    version: str
