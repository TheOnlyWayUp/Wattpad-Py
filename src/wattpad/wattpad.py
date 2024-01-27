"""Copyright (C) 2024 TheOnlyWayUp

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see https://www.gnu.org/licenses/.

---

The main module for the wattpad package. This contains the User, Story, and List classes.

>>> u = User("<username>")
>>> await u.fetch()
>>> print(u.data)

Use `help(User)` for information. Refer to the documentation for more.
"""

from __future__ import annotations
from typing import Optional, cast
from models import (
    ListModel,
    StoryModel,
    UserModel,
)
from model_types import ListModelFieldsType, UserModelFieldsType, StoryModelFieldsType
from utils import get_fields, build_url, fetch_url, construct_fields, singleton


@singleton
class User:
    """User Model"""

    def __init__(self, username: str, **kwargs):
        self.username = username.lower()
        self.stories: list[Story] = []
        self.following: list[User] = []
        self.followers: list[User] = []
        self.lists: list[List] = []

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

        stories: list[Story] = []
        for story in data["stories"]:
            if "user" in story:
                story.pop("user")
            stories.append(
                Story(user=self, **story)
            )  # TODO: Make Stories, Parts, and Users singletons for memory-efficiency.

        self.stories = stories
        self.data.num_stories_published = len(
            self.stories
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

        self.followers = [User(**user) for user in data["users"]]
        self.data.num_followers = len(self.followers)

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

        self.following = [User(**user) for user in data["users"]]
        self.data.num_following = len(self.following)

        return data

    async def fetch_lists(
        self,
        include: bool | ListModelFieldsType = False,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> dict:
        """Populate a User's lists. The API can slow down for large responses. Use the limit and offset parameters for efficiency. List IDs are _always_ returned."""
        if include is False:
            include_fields: ListModelFieldsType = {}
        elif include is True:
            include_fields: ListModelFieldsType = {
                key: True for key in get_fields(ListModel)  # type: ignore
            }
        else:
            include_fields: ListModelFieldsType = include

        include_fields["id"] = True

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

        self.lists = [List(**list_) for list_ in data["lists"]]
        self.data.num_lists = len(self.lists)

        return data


# --- #


@singleton
class Story:
    """Story Model"""

    def __init__(self, id: str, user: User, **kwargs):
        self.id = id.lower()
        self.user: User = user
        self.recommended: list[Story] = []
        # self.parts: list[Part]  # ! NotImplemented. In the future, if Part text retrieval is a part of this library, that would warrant the creation of a seperate Part singleton. Right now, having self.parts would cause inconsistency with the rest of the library.
        self.data = StoryModel(id=self.id, **kwargs)

    def __repr__(self) -> str:
        return f"<Story id={self.id}>"

    async def fetch(self, include: bool | StoryModelFieldsType = False) -> dict:
        """Fetch the Story's data. The author's username is _always_ returned."""
        if include is False:
            include_fields: StoryModelFieldsType = {}
        elif include is True:
            include_fields: StoryModelFieldsType = {
                key: True for key in get_fields(StoryModel)  # type: ignore
            }
        else:
            include_fields: StoryModelFieldsType = include

        if "user" in include_fields:
            if include_fields["user"] is True:
                include_fields["user"] = cast(
                    UserModelFieldsType, {key: True for key in get_fields(UserModel)}  # type: ignore
                )
            elif include_fields["user"] is False:
                include_fields["user"] = {"username": True}
            else:
                include_fields["user"]["username"] = True
        else:
            include_fields["user"] = {"username": True}

        data = cast(
            dict,
            await fetch_url(
                build_url(f"stories/{self.data.id}", fields=dict(include_fields))
            ),
        )
        if "id" in data:
            data.pop("id")

        self.data = StoryModel(id=self.id, **data)

        return data

    async def fetch_recommended(
        self,
        include: bool | StoryModelFieldsType = False,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> list:
        """Populate a Story's recommended stories. The story's ID, and the author's username are _always_ returned."""
        if include is False:
            include_fields: StoryModelFieldsType = {}
        elif include is True:
            include_fields: StoryModelFieldsType = {
                key: True for key in get_fields(StoryModel)  # type: ignore
            }
        else:
            include_fields: StoryModelFieldsType = include

        include_fields["id"] = True

        if "user" in include_fields:
            if include_fields["user"] is True:
                include_fields["user"] = cast(
                    UserModelFieldsType, {key: True for key in get_fields(UserModel)}  # type: ignore
                )
            elif include_fields["user"] is False:
                include_fields["user"] = {"username": True}
            else:
                include_fields["user"]["username"] = True
        else:
            include_fields["user"] = {"username": True}

        data = cast(
            list[dict],
            await fetch_url(
                build_url(
                    f"stories/{self.data.id}/recommended",
                    fields=dict(include_fields),
                    limit=limit,
                    offset=offset,
                )
            ),
        )

        self.recommended = [Story(**story) for story in data]

        return data


# --- #


@singleton
class List:
    """List Model"""

    def __init__(self, id: str, name: str = "", stories: list[Story] = []):
        self.id = id.lower()
        self.name: str = name
        self.stories: list[Story] = stories

    def __repr__(self) -> str:
        return f"<List id={self.id}>"
