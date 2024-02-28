from uuid import UUID, uuid4

from icecream import ic

from app.db.conn import connect_db
from app.models.users import NewUser


class UserQueries:
    def __init__(self) -> None:
        self.table = "users"

    def get_all_users(self) -> list[dict]:
        query = f"SELECT * FROM {self.table}"
        db = connect_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute(query)
        data_res = cursor.fetchall()
        cursor.close()
        db.close()
        data: list[dict] = [row for row in data_res]  # type: ignore
        return data

    def get_by_uuid(self, user_id: UUID) -> dict | None:
        query = f"SELECT * FROM {self.table} WHERE user_id = (%s);"
        db = connect_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute(query, (str(user_id),))
        db_data = cursor.fetchone()
        cursor.close()
        db.close()
        if db_data is None:
            return None
        data: dict = db_data  # type: ignore
        return data

    def get_auth0_id(self, auth0_id: str) -> dict | None:
        query = f"SELECT * FROM {self.table} WHERE auth0_id = (%s);"
        db = connect_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute(query, (auth0_id,))
        db_data = cursor.fetchone()
        cursor.close()
        db.close()
        if db_data is None:
            return None
        data: dict = db_data  # type: ignore
        return data

    def insert_user(self, user: NewUser, auth0_id: str) -> UUID:
        """Insert a new user"""
        new_id = uuid4()
        query = f"INSERT INTO {self.table} (user_id, username, email, name, auth0_id) VALUES (%s, %s, %s, %s, %s)"
        db = connect_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            query,
            (str(new_id), user.username, user.email, user.name, auth0_id),
        )

        db.commit()
        cursor.close()
        db.close()
        return new_id
