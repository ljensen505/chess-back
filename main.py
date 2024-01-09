import os
import pickle
import stat
from uuid import UUID

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

from chess import Chess

app = FastAPI()


@app.get("/", status_code=status.HTTP_200_OK)
def read_root():
    available_routes = ["/"]
    return {"available_routes": available_routes}


@app.get("/games", status_code=status.HTTP_200_OK)
def get_games() -> dict[str, str]:
    return {
        game.split(".")[0]: f"/games/{game.split('.')[0]}"
        for game in os.listdir("games")
        if game.endswith(".pickle")
    }


@app.post("/games", status_code=status.HTTP_201_CREATED)
def create_game() -> dict[str, UUID]:
    """Create a new game and return the game id"""
    chess = Chess()
    with open(f"games/{chess.id}.pickle", "wb") as f:
        pickle.dump(chess, f)
    return {"id": chess.id}


@app.get("/games/{game_id}")
def get_game(game_id: UUID) -> dict:
    """Get the current state of the game"""
    try:
        with open(f"games/{game_id}.pickle", "rb") as f:
            chess = pickle.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Game not found")

    return dict(chess)


@app.delete("/games/{game_id}")
def delete_game(game_id: UUID) -> dict:
    """Delete the current state of the game"""
    try:
        os.remove(f"games/{game_id}.pickle")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Game not found")
    return {"message": f"Game {game_id} deleted"}
