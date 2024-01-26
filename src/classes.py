from typing import Optional
from models import StoryModel, UserModel, UserModelFieldsType, StoryModelFieldsType
from utils import get_fields, build_url, fetch_url, construct_fields


class User:
    """User Model"""

    def __init__(self, username, **kwargs):
        self.username = username
        self.data = UserModel(username=username, **kwargs)

    def __repr__(self) -> str:
        return f"<User username={self.username}>"

    async def create(self, include: bool | UserModelFieldsType = False) -> dict:
        if include is False:
            include_fields: UserModelFieldsType = {}
        elif include is True:
            include_fields: UserModelFieldsType = {
                key: True for key in get_fields(UserModel)  # type: ignore
            }
        else:
            include_fields: UserModelFieldsType = include

        data = await fetch_url(
            build_url(f"users/{self.data.username}", fields=dict(include_fields))
        )
        if "username" in data:
            data.pop("username")

        self.data = UserModel(username=self.username, **data)

        return data

    async def fetch_stories(self, include: bool | StoryModelFieldsType = False) -> dict:
        """Populate a User's authored stories. The ID Field is _always_ returned."""
        if include is False:
            include_fields: StoryModelFieldsType = {}
        elif include is True:
            include_fields: StoryModelFieldsType = {
                key: True for key in get_fields(StoryModel)  # type: ignore
            }
        else:
            include_fields: StoryModelFieldsType = include

        include_fields["id"] = True

        url = (
            build_url(f"users/{self.data.username}/stories", fields=None)
            + f"&fields=stories({construct_fields(dict(include_fields))})"  # ! The field format for story retrieval differs here. It's /stories?fields=stories(<fields>). Compared to the usual /path?fields=<fields>. For this reason, we need to manually edit the fields in.
        )
        data = await fetch_url(url)

        stories: list[StoryModel] = []
        for story in data["stories"]:
            if "user" in story:
                story.pop("user")
            stories.append(
                StoryModel(user=self.data, **story)
            )  # TODO: Make Stories, Parts, and Users singletons for memory-efficiency.

        self.data.stories = stories
        self.data.total_stories = len(
            self.data.stories
        )  # ! The data['total'] can also be used, but it isn't always present. (Based on included_fields.)

        return data
