from pprint import pprint
from uuid import uuid4

from fastapi.testclient import TestClient

from app import app
from chess import board

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    body = response.json()
    assert "available_routes" in body
    assert "/" in body["available_routes"]


def test_get_games():
    game_ids = [post_game() for _ in range(10)]
    response = client.get("/games")
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    for game in body:
        assert "game_id" in game
        assert isinstance(game["game_id"], str)
        assert len(game["game_id"]) == 36
        assert "self" in game
        assert isinstance(game["self"], str)
        assert game["self"].startswith("/games/")

    response_ids = [game["game_id"] for game in body]

    assert all(game_id in response_ids for game_id in game_ids)
    for game_id in game_ids:
        client.delete(f"/games/{game_id}")


def test_get_game():
    game_id = post_game()
    response = client.get(f"/games/{game_id}")
    assert response.status_code == 200
    body = response.json()
    vals = [
        "board",
        "game_state",
        "game_id",
        "turn",
        "turn_count",
    ]
    board = body["board"]

    assert len(board) == 32
    assert all(val in body for val in vals)

    response = client.delete(f"/games/{game_id}")
    assert response.status_code == 200

    fake_id = uuid4()
    response = client.get(f"/games/{fake_id}")
    assert response.status_code == 404


def post_game() -> str:
    response = client.post("/games")
    assert response.status_code == 201
    body = response.json()
    assert "game_id" in body
    assert isinstance(body["game_id"], str)
    assert len(body["game_id"]) == 36
    return body["game_id"]


def test_post_game():
    game_id = post_game()
    client.delete(f"/games/{game_id}")


def test_delete_game():
    game_id = post_game()
    response = client.delete(f"/games/{game_id}")
    assert response.status_code == 200
    body = response.json()
    assert "message" in body
    assert body["message"] == f"Game {game_id} deleted"

    response = client.get("/games")
    assert response.status_code == 200
    body = response.json()
    assert game_id not in body


def test_make_move():
    game_id = post_game()
    move = {
        "start": "A2",
        "end": "A4",
    }
    response = client.patch(f"/games/{game_id}", json=move)
    assert response.status_code == 200
    body = response.json()
    assert "board" in body
    board: dict = body["board"]
    assert isinstance(board, dict)
    assert len(board) == 32
    assert "A2" not in board
    white_pawn = board["A4"]
    assert white_pawn["type"] == "pawn"
    assert white_pawn["color"] == "white"

    client.delete(f"/games/{game_id}")
