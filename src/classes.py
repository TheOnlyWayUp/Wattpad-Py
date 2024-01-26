from models import UserModel, UserModelFieldsType
from utils import get_fields, build_url, fetch_url, construct_fields
from typing import cast


class User:
    """User Model"""

    def __init__(self, username, **kwargs):
        self.username = username
        self.data = UserModel(username=username, **kwargs)

    def __repr__(self) -> str:
        return f"<User username={self.username}>"

    async def create(self, include: bool | UserModelFieldsType = False):
        if include is False:
            include_fields: UserModelFieldsType = {"description": True}
        elif include is True:
            include_fields: UserModelFieldsType = {
                key: True for key in get_fields(UserModel)  # type: ignore
            }
        else:
            include_fields: UserModelFieldsType = include

        if "username" in include_fields:
            include_fields.pop("username")

        data = await fetch_url(
            build_url(f"users/{self.data.username}", fields=dict(include_fields))
        )

        self.data = UserModel(username=self.username, **data)

        return self

    async def fetch_stories(self, include: bool | list):
        """Populate a User's authored stories."""
        ...
