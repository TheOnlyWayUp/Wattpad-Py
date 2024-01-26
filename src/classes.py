from models import UserModel, user_fields_T, story_fields_T
from utils import get_fields, build_url, get_url
from typing import cast


class User:
    """User Model"""

    def __init__(self, username, **kwargs):
        self.username = username
        self.data = UserModel(username=username, **kwargs)

    def __repr__(self) -> str:
        return f"<User username={self.username}>"

    async def create(self, include: bool | list[story_fields_T] = False):
        if include is True:
            include_fields: list[user_fields_T] = get_fields(UserModel)  # type: ignore
            include_fields.remove("username")
        elif include is False:
            include_fields: list[user_fields_T] = ["description"]
        else:
            include_fields = cast(list[user_fields_T], include)

        data = await get_url(
            build_url(f"users/{self.data.username}", fields=include_fields)  # type: ignore
        )

        self.data = UserModel(username=self.username, **data)

        return self
