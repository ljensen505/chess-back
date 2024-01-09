from pprint import pprint

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    body = response.json()
    assert "available_routes" in body
    assert "/" in body["available_routes"]


def test_get_games():
    game_id = post_game()
    response = client.get("/games")
    assert response.status_code == 200
    body = response.json()
    pprint(body)
    assert game_id in body

    response = client.get(f"/games/{game_id}")
    assert response.status_code == 200

    response = client.delete(f"/games/{game_id}")
    assert response.status_code == 200


def test_get_game():
    game_id = post_game()
    response = client.get(f"/games/{game_id}")
    assert response.status_code == 200
    body = response.json()
    vals = [
        "board",
        "captured_pieces",
        "check",
        "checkmate",
        "game_state",
        "id",
        "turn",
        "turn_count",
    ]
    board = body["board"]
    assert len(board) == 32
    assert all(val in body for val in vals)

    response = client.delete(f"/games/{game_id}")
    assert response.status_code == 200


def post_game() -> str:
    response = client.post("/games")
    assert response.status_code == 201
    body = response.json()
    assert "id" in body
    assert isinstance(body["id"], str)
    assert len(body["id"]) == 36
    return body["id"]


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
