from datetime import datetime
from uuid import UUID, uuid4

from icecream import ic

from app.db.conn import connect_db


class GameQueries:
    def __init__(self) -> None:
        self.table = "games"

    def delete_game(self, game_id: UUID) -> None:
        query = f"DELETE FROM {self.table} WHERE game_id = (%s);"
        db = connect_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute(query, (str(game_id),))
        cursor.close()
        db.commit()
        db.close()

    def select_all_by_user_id(self, owner_id: UUID) -> list[dict]:
        query = f"SELECT * FROM {self.table} WHERE owner_id = (%s) OR black_player_id = (%s) OR white_player_id = (%s);"
        db = connect_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute(query, (str(owner_id),) * 3)
        data_res = cursor.fetchall()
        cursor.close()
        db.close()
        data: list[dict] = [row for row in data_res]  # type: ignore
        return data

    def select_by_id(self, game_id: UUID) -> dict | None:
        query = f"SELECT * FROM {self.table} WHERE game_id = (%s);"
        db = connect_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute(query, (str(game_id),))
        db_data = cursor.fetchone()
        cursor.close()
        db.close()
        if db_data is None:
            return None
        data: dict = db_data  # type: ignore
        return data

    def insert_game(self, owner_id: UUID) -> UUID:
        """Insert a new game"""
        query = f"INSERT INTO {self.table} (game_id, owner_id) VALUES (%s, %s)"
        new_id = uuid4()
        db = connect_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute(query, (str(new_id), str(owner_id)))
        cursor.close()
        db.commit()
        db.close()
        return new_id

    def assign_player(self, game_id: UUID, user_id: UUID, color: str) -> None:
        """Assign a player to a game"""
        query = f"UPDATE {self.table} SET {color}_player_id = (%s) WHERE game_id = (%s)"
        db = connect_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute(query, (str(user_id), str(game_id)))
        cursor.close()
        db.commit()
        db.close()

    def update_last_updated_at(self, game_id: UUID) -> None:
        """Update the last_updated_at field for a game"""
        now = datetime.now()
        query = f"UPDATE {self.table} SET last_updated_at = (%s) WHERE game_id = (%s)"
        db = connect_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            query,
            (
                now,
                str(game_id),
            ),
        )
        cursor.close()
        db.commit()
        db.close()
