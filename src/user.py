from typing import Optional, cast
from models import (
    ListModel,
    ListModelFieldsType,
    StoryModel,
    UserModel,
    UserModelFieldsType,
    StoryModelFieldsType,
)
from utils import get_fields, build_url, fetch_url, construct_fields, singleton


@singleton
class User:
    """User Model"""

    def __init__(self, username: str, **kwargs):
        self.username = username.lower()
        self.data = UserModel(username=self.username, **kwargs)

    def __repr__(self) -> str:
        return f"<User username={self.username}>"

    async def fetch(self, include: bool | UserModelFieldsType = False) -> dict:
        if include is False:
            include_fields: UserModelFieldsType = {}
        elif include is True:
            include_fields: UserModelFieldsType = {
                key: True for key in get_fields(UserModel)  # type: ignore
            }
        else:
            include_fields: UserModelFieldsType = include

        data = cast(
            dict,
            await fetch_url(
                build_url(f"users/{self.data.username}", fields=dict(include_fields))
            ),
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
        data = cast(dict, await fetch_url(url))

        stories: list[StoryModel] = []
        for story in data["stories"]:
            if "user" in story:
                story.pop("user")
            stories.append(
                StoryModel(user=self.data, **story)
            )  # TODO: Make Stories, Parts, and Users singletons for memory-efficiency.

        self.data.stories = stories
        self.data.num_stories_published = len(
            self.data.stories
        )  # ! The data['total'] can also be used, but it isn't always present. (Based on included_fields.)

        return data

    async def fetch_followers(
        self,
        include: bool | UserModelFieldsType = False,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> dict:
        """Populate a User's followers. For best performance, use the limit and offset parameters. If the limit is too high, requests may time out. Follower's usernames are _always_ returned."""
        if include is False:
            include_fields: UserModelFieldsType = {}
        elif include is True:
            include_fields: UserModelFieldsType = {
                key: True for key in get_fields(UserModel)  # type: ignore
            }
        else:
            include_fields: UserModelFieldsType = include

        include_fields["username"] = True

        url = (
            build_url(
                f"users/{self.data.username}/followers",
                fields=None,
                limit=limit,
                offset=offset,
            )
            + f"&fields=users({construct_fields(dict(include_fields))})"  # ! Similar to story retrieval, requested fields need to be wrapped in `users(<fields>)`.
        )
        data = cast(dict, await fetch_url(url))

        self.data.followed_by_users = [UserModel(**user) for user in data["users"]]
        self.data.num_followers = len(self.data.followed_by_users)

        return data

    async def fetch_following(
        self,
        include: bool | UserModelFieldsType = False,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> dict:
        """Populate the users this User follows. For best performance, use the limit and offset parameters. if the limit is too high, requests may time out. Follower's usernames are _always_ returned."""
        if include is False:
            include_fields: UserModelFieldsType = {}
        elif include is True:
            include_fields: UserModelFieldsType = {
                key: True for key in get_fields(UserModel)  # type: ignore
            }
        else:
            include_fields: UserModelFieldsType = include

        include_fields["username"] = True

        url = (
            build_url(
                f"users/{self.data.username}/following",
                fields=None,
                limit=limit,
                offset=offset,
            )
            + f"&fields=users({construct_fields(dict(include_fields))})"  # ! Similar to story retrieval, requested fields need to be wrapped in `users(<fields>)`.
        )
        data = cast(dict, await fetch_url(url))

        self.data.following_users = [UserModel(**user) for user in data["users"]]
        self.data.num_following = len(self.data.followed_by_users)

        return data

    async def fetch_lists(
        self,
        include: bool | ListModelFieldsType = False,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> dict:
        """Populate a User's lists. The API can slow down for large responses. Use the limit and offset parameters for efficiency."""
        if include is False:
            include_fields: ListModelFieldsType = {}
        elif include is True:
            include_fields: ListModelFieldsType = {
                key: True for key in get_fields(ListModel)  # type: ignore
            }
        else:
            include_fields: ListModelFieldsType = include

        url = (
            build_url(
                f"users/{self.data.username}/lists",
                fields=None,
                limit=limit,
                offset=offset,
            )
            + f"&fields=lists({construct_fields(dict(include_fields))})"  # ! Similar to story retrieval, requested fields need to be wrapped in `lists(<fields>)`.
        )
        data = cast(dict, await fetch_url(url))

        self.data.lists = [ListModel(**list_) for list_ in data["lists"]]
        self.data.num_lists = len(self.data.lists)

        return data
