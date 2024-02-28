from uuid import UUID

from fastapi import HTTPException
from icecream import ic

from app.db.users import UserQueries
from app.models.game import BasicUserInfo
from app.models.users import BaseUser, DetailedUser, NewUser


class UserController:
    def __init__(self) -> None:
        self.queries = UserQueries()

    def construct_user(self, user_data: dict) -> DetailedUser:
        try:
            return DetailedUser(
                self=f"users/{user_data['user_id']}",
                user_id=user_data["user_id"],
                username=user_data["username"],
                email=user_data["email"],
                name=user_data["name"],
                auth0_id=user_data["auth0_id"],
            )
        except Exception as e:
            ic(e)
            raise ValueError("Error constructing user")

    def get_all_users(self) -> list[DetailedUser]:
        users_data = self.queries.get_all_users()
        return [self.construct_user(user) for user in users_data]

    def get_user_by_uuid(self, user_id: UUID) -> DetailedUser:
        user_data = self.queries.get_by_uuid(user_id)
        if user_data is None:
            raise HTTPException(status_code=404, detail="User not found")
        return self.construct_user(user_data)

    def create_user(self, user: NewUser, auth_result: dict) -> BaseUser:
        # THIS HAS NOT YET BEEN FULLY TESTED
        new_id = self.queries.insert_user(user, auth_result["sub"])
        return self.get_user_by_uuid(new_id)

    def get_user_by_auth_id(self, auth0_id: str) -> DetailedUser:
        data = self.queries.get_auth0_id(auth0_id)
        if data is None:
            raise HTTPException(status_code=404, detail="User not found")
        return self.construct_user(data)
