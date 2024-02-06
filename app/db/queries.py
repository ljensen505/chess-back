from pprint import pprint
from uuid import UUID

from fastapi import HTTPException

from app.models import BaseGame, GameInfo, UserBase, UserDetails

from .conn import connect_db


def get_game_by_id(game_id: UUID) -> BaseGame:
    """Get a game by its ID"""
    query = "SELECT * FROM games WHERE id = (%s);"
    db = connect_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(query, (str(game_id),))
    data = cursor.fetchone()
    cursor.close()
    db.close()
    if data is None:
        raise HTTPException(status_code=404, detail="Game not found")
    data = dict(data)  # type: ignore
    game_id = data.get("id")  # type: ignore
    game_self = f"/games/{game_id}"
    owner_id = data.get("owner_id")  # type: ignore
    if None in (game_id, game_self, owner_id):
        raise HTTPException(status_code=500, detail="Game data is incomplete")
    return BaseGame(game_id=game_id, self=game_self, owner_id=owner_id)  # type: ignore


def get_users() -> list[UserBase]:
    """Get a list of all users without game information"""
    query = "SELECT * FROM users"
    db = connect_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    db.close()
    users: list[UserBase] = []
    for user in data:
        user_id = user.get("id")  # type: ignore
        user_self = f"/users/{user_id}"
        users.append(UserBase(id=user_id, email=user.get("email"), name=user.get("name"), auth0_id=user.get("auth0_id"), self=user_self))  # type: ignore
    return users


def get_games_by_user_id(user_id: UUID) -> list[GameInfo]:
    """Get a list of games by user ID"""
    query = "SELECT *FROM games WHERE owner_id = (%s);"
    db = connect_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(query, (str(user_id),))
    data = cursor.fetchall()
    cursor.close()
    db.close()
    games: list[GameInfo] = []

    for game in data:
        game_id = game.get("id")  # type: ignore
        game_self = f"/games/{game_id}"
        games.append(GameInfo(game_id=game_id, self=game_self, owner_id=user_id))

    return games


def get_user_by_id(user_id: UUID) -> UserBase:
    """Get a user by their ID"""
    query = "SELECT * FROM users WHERE id = (%s);"
    db = connect_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(query, (str(user_id),))
    data = cursor.fetchone()
    cursor.close()
    db.close()
    if data is None:
        raise HTTPException(status_code=404, detail="User not found")
    user_self = f"/users/{user_id}"
    return UserBase(id=user_id, email=data.get("email"), name=data.get("name"), auth0_id=data.get("auth0_id"), self=user_self)  # type: ignore


def create_user(user: UserDetails) -> UserDetails:
    """Create a new user"""
    db = connect_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "INSERT INTO users (id, username, email, name, auth0_id) VALUES (%s, %s, %s, %s, %s)",
        (str(user.id), user.email, user.name, user.auth0_id),
    )

    cursor.close()
    db.close()

    return user


def insert_game(game: BaseGame) -> BaseGame:
    """Insert a new game"""
    db = connect_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "INSERT INTO games (id, owner_id) VALUES (%s, %s)",
        (str(game.game_id), str(game.owner_id)),
    )

    db.commit()
    cursor.close()
    db.close()

    return game


def get_user_by_auth_id(auth0_id: str) -> UserBase:
    """Get a user by their auth0 ID"""
    query = "SELECT * FROM users WHERE auth0_id = (%s);"
    db = connect_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(query, (auth0_id,))
    data = cursor.fetchone()
    cursor.close()
    db.close()
    if data is None:
        raise HTTPException(status_code=404, detail="User not found")
    user_id = data.get("id")  # type: ignore
    user_self = f"/users/{user_id}"
    return UserBase(id=user_id, email=data.get("email"), name=data.get("name"), auth0_id=auth0_id, self=user_self)  # type: ignore


def delete_game(game: BaseGame) -> None:
    """Delete the current state of the game"""
    query = "DELETE FROM games WHERE id = (%s);"
    db = connect_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(query, (str(game.game_id),))
    db.commit()
    cursor.close()
    db.close()
