import os
import pickle
from uuid import UUID

from fastapi import FastAPI, HTTPException, status

from __version__ import __version__
from app.models import AvailableRoutes, ChessGame, GameInfo, Move, game_to_response
from chess import Chess

app = FastAPI()

GAMES_DIR = os.path.join(os.path.dirname(__file__), "games")


@app.get("/", status_code=status.HTTP_200_OK)
async def read_root() -> AvailableRoutes:
    return AvailableRoutes(
        available_routes=[
            "/",
            "/games",
            "/games/{game_id}",
        ],
        version=__version__,
    )


@app.get("/games", status_code=status.HTTP_200_OK)
async def get_games() -> list[GameInfo]:
    """Get a list of all games"""
    game_files = [g for g in os.listdir(GAMES_DIR) if g.endswith(".pickle")]
    game_ids: list[UUID] = [UUID(g.split(".")[0]) for g in game_files]
    return [GameInfo(game_id=game_id, self=f"/games/{game_id}") for game_id in game_ids]


@app.post("/games", status_code=status.HTTP_201_CREATED)
async def create_game() -> GameInfo:
    """Create a new game and return the game id"""
    chess = Chess()
    print(GAMES_DIR)
    with open(os.path.join(GAMES_DIR, f"{chess.id}.pickle"), "wb") as f:
        pickle.dump(chess, f)
    return GameInfo(game_id=chess.id, self=f"/games/{chess.id}")


@app.get("/games/{game_id}")
async def get_game(game_id: UUID) -> ChessGame:
    """Get the current state of the game"""

    try:
        with open(os.path.join(GAMES_DIR, f"{game_id}.pickle"), "rb") as f:
            chess = pickle.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Game not found")

    chess_model = game_to_response(chess)

    return chess_model


@app.delete("/games/{game_id}", status_code=status.HTTP_200_OK)
def delete_game(game_id: UUID) -> dict:
    """Delete the current state of the game"""
    try:
        os.remove(os.path.join(GAMES_DIR, f"{game_id}.pickle"))

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Game not found")
    return {"message": f"Game {game_id} deleted"}


@app.patch("/games/{game_id}", status_code=status.HTTP_200_OK)
async def make_move(game_id: UUID, move: Move) -> ChessGame:
    """Make a move in the game"""
    try:
        with open(os.path.join(GAMES_DIR, f"{game_id}.pickle"), "rb") as f:
            chess: Chess = pickle.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Game not found")

    try:
        chess.make_move(move.start, move.end)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    with open(os.path.join(GAMES_DIR, f"{game_id}.pickle"), "wb") as f:
        pickle.dump(chess, f)

    return game_to_response(chess)
