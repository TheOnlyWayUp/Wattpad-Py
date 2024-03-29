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
from .models import (
    ListModel,
    StoryModel,
    UserModel,
)
from .model_types import ListModelFieldsType, UserModelFieldsType, StoryModelFieldsType
from .utils import (
    get_fields,
    convert_from_aliases,
    build_url,
    fetch_url,
    construct_fields,
    create_singleton,
)


class User(metaclass=create_singleton()):
    """A representation of a User on Wattpad.
    **Note**: Users are singletons, unique as per their username. Two user classes with the same username are the _same_.

    Attributes:
        username (str): Lowercased username of this User.
        stories (list[Story]): Stories authored by this User.
        followers (list[User]): Users that follow this User.
        following (list[User]): Users this User follows.
        lists (set[List]): Lists created by this User.
        data (UserModel): User Data from the Wattpad API.
    """

    def __init__(self, username: str, **kwargs):
        """Create a User object.

        Args:
            username (str): The username of this User.
            **kwargs (any): Arguments to pass directly to the underlying `UserModel`. These are ignored if the User has been instantiated earlier in the runtime.
        """
        self.username = username.lower()
        self.stories: list[Story] = []
        self.followers: set[User] = set()
        self.following: set[User] = set()
        self.lists: set[List] = set()

        self.data = UserModel(username=self.username, **kwargs)

    def __repr__(self) -> str:
        return f"<User username={self.username}>"

    async def fetch(self, include: bool | UserModelFieldsType = False) -> dict:
        """Populates a User's data. Call this method after instantiation.

        Args:
            include (bool | UserModelFieldsType, optional): Fields to fetch. True fetches all fields. Defaults to False.

        Returns:
            dict: The raw API Response.
        """
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
        """Fetch a User's authored stories.

        Args:
            include (bool | StoryModelFieldsType, optional): Fields of authored stories to fetch. True fetches all fields. Defaults to False.

        Returns:
            dict: The raw API Response.
        """
        if include is False:
            include_fields: StoryModelFieldsType = {}
        elif include is True:
            include_fields: StoryModelFieldsType = {
                key: True for key in get_fields(StoryModel)  # type: ignore
            }
        else:
            include_fields: StoryModelFieldsType = include

        include_fields["id"] = True

        if "tagRankings" in include_fields:
            if type(include_fields["tagRankings"]) is dict:
                include_fields["tagRankings"]["name"] = True

        if "parts" in include_fields:
            if type(include_fields["parts"]) is dict:
                include_fields["parts"]["id"] = True

        url = (
            build_url(f"users/{self.data.username}/stories", fields=None)
            + f"&fields=stories({construct_fields(dict(include_fields))})"  # ! The field format for story retrieval differs here. It's /stories?fields=stories(<fields>). Compared to the usual /path?fields=<fields>. For this reason, we need to manually edit the fields in.
        )
        data = cast(dict, await fetch_url(url))

        stories: list[Story] = []
        for story in data["stories"]:
            if "user" in story:
                story.pop("user")

            id_ = story.pop("id")

            story_cls = Story(
                user=self, id=id_
            )  # ! This code is an artefact of the singleton design model. If a user already exists, their data will not be updated otherwise.
            story_cls._update_data(**story)

            stories.append(story_cls)

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
        """Fetches the User's followers.

        Args:
            include (bool | UserModelFieldsType, optional): Fields of the following users' to fetch. True fetches all fields. Defaults to False.
            limit (Optional[int], optional): Maximum number of users to return at once. Use this alongside `offset` for better performance. Defaults to None.
            offset (Optional[int], optional): Number of users to skip before returning followers. Use this alongside `limit` for better performance. Defaults to None.

        Returns:
            dict: The raw API Response.
        """
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

        followers: set[User] = set()
        for user in data["users"]:
            username = user.pop("username")
            user_cls = User(
                username=username
            )  # ! This code is an artefact of the singleton design model. If a user already exists, their data will not be updated otherwise.
            user_cls.following.add(
                self
            )  # ! The current user is followed by this fetched user
            user_cls._update_data(**user)
            followers.add(user_cls)

        self.followers.update(followers)
        self.data.num_followers = len(self.followers)

        return data

    async def fetch_following(
        self,
        include: bool | UserModelFieldsType = False,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> dict:
        """Fetch the users this User follows.

        Args:
            include (bool | UserModelFieldsType, optional): Fields of the followed users' to fetch. True fetches all fields. Defaults to False.
            limit (Optional[int], optional): Maximum number of users to return at once. Use this alongside `offset` for better performance. Defaults to None.
            offset (Optional[int], optional): Number of users to skip before returning followers. Use this alongside `limit` for better performance. Defaults to None.

        Returns:
            dict: The raw API Response.
        """
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

        following: set[User] = set()
        for user in data["users"]:
            username = user.pop("username")

            user_cls = User(
                username=username
            )  # ! This code is an artefact of the singleton design model. If a user already exists, their data will not be updated otherwise.
            user_cls.followers.add(self)  # ! The current user follows this fetched user
            user_cls._update_data(**user)

            following.add(user_cls)

        self.followers.update(following)
        self.data.num_following = len(self.following)

        return data

    async def fetch_lists(
        self,
        include: bool | ListModelFieldsType = False,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> dict:
        """Fetch a User's lists.

        Args:
            include (bool | ListModelFieldsType, optional): Fields of the lists to fetch. True fetches all fields. Defaults to False.
            limit (Optional[int], optional): Maximum number of users to return at once. Use this alongside `offset` for better performance. Defaults to None.
            offset (Optional[int], optional): Number of users to skip before returning followers. Use this alongside `limit` for better performance. Defaults to None.

        Returns:
            dict: The raw API Response.
        """
        if include is False:
            include_fields: ListModelFieldsType = {}
        elif include is True:
            include_fields: ListModelFieldsType = {
                key: True for key in get_fields(ListModel)  # type: ignore
            }
        else:
            include_fields: ListModelFieldsType = include

        include_fields["id"] = True

        if "stories" in include_fields:
            if type(include_fields["stories"]) is dict:
                include_fields["stories"]["id"] = True

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

        lists: set[List] = set()
        for list_ in data["lists"]:
            id_ = list_.pop("id")
            list_cls = List(
                id=id_, user=self
            )  # ! This code is an artefact of the singleton design model. If a list already exists, its data will not be updated otherwise.

            stories: set[Story] = set()
            for story in list_["stories"]:
                s_id_ = story.pop("id")
                story_cls = Story(id=s_id_)
                story_cls._update_data(**story)
                stories.add(story_cls)

            list_cls.stories.update(stories)
            lists.add(list_cls)

        self.lists.update(lists)
        self.data.num_lists = len(self.lists)

        return data

    def _update_data(self, **kwargs):
        """Updates self.data with kwargs, overwriting any duplicate values with a preference towards kwargs.

        Returns:
            None: Nothing is returned.
        """
        self.data = self.data.model_copy(
            update=convert_from_aliases(kwargs, self.data), deep=True
        )


# --- #


class Story(metaclass=create_singleton()):
    """A representation of a Story on Wattpad.
    **Note**: Stories are singletons, unique as per their ID. Two story classes with the same ID are the _same_.

    Attributes:
        id (str): Lowercased ID of this Story.
        user (User): The User who authored this Story.
        recommended (list[Story]): Stories recommended from this Story.
        data (StoryModel): Story Data from the Wattpad API.
    """

    def __init__(self, id: str, user: Optional[User] = None, **kwargs):
        """Create a Story object.

        Args:
            id (str): The ID of the Story.
            user (User): The User who authored this Story.
        """
        self.id = id.lower()
        self.user: Optional[User] = user
        self.recommended: list[Story] = []
        # self.parts: list[Part]  # ! NotImplemented. In the future, if Part text retrieval is a part of this library, that would warrant the creation of a seperate Part singleton. Right now, having self.parts would cause inconsistency with the rest of the library.
        self.data = StoryModel(id=self.id, **kwargs)

    def __repr__(self) -> str:
        return f"<Story id={self.id}>"

    async def fetch(self, include: bool | StoryModelFieldsType = False) -> dict:
        """Populates a Story's data. Call this method after instantiation.

        Args:
            include (bool | StoryModelFieldsType, optional): Fields to fetch. True fetches all fields. Defaults to False.

        Returns:
            dict: The raw API Response.
        """
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
        if "user" in data:
            user_data = data.pop("user")
            user = User(user_data.pop("username"))
            user._update_data(**user_data)
            self.user = user

        self.data = StoryModel(id=self.id, **data)

        return data

    async def fetch_recommended(
        self,
        include: bool | StoryModelFieldsType = False,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> list:
        """Fetch Stories recommended from this Story.

        Args:
            include (bool | StoryModelFieldsType, optional): Fields to fetch of the recommended stories. True fetches all fields. Defaults to False.
            limit (Optional[int], optional): Maximum number of users to return at once. Use this alongside `offset` for better performance. Defaults to None.
            offset (Optional[int], optional): Number of users to skip before returning followers. Use this alongside `limit` for better performance. Defaults to None.

        Returns:
            dict: The raw API Response.
        """
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

    def _update_data(self, **kwargs):
        """Updates self.data with kwargs, overwriting any duplicate values with a preference towards kwargs.

        Returns:
            None: Nothing is returned.
        """
        self.data = self.data.model_copy(
            update=convert_from_aliases(kwargs, self.data), deep=True
        )


# --- #


class List(metaclass=create_singleton()):
    """A representation of a List on Wattpad.
    **Note**: Lists are singletons, unique as per their ID. Two List classes with the same ID are the _same_.

    Attributes:
        id (str): Lowercased ID of this List.
        name (str): The name of this List.
        user (User): The User who created this List.
        stories (list[Story]): Stories included within this List.
    """

    def __init__(
        self, id: int, user: User, name: str = "", stories: set[Story] = set()
    ):
        """Creates a List object.

        Args:
            id (str): The ID of this List.
            user (User): The User who created this List.
            name (str, optional): The name of this List. Defaults to "".
            stories (list[Story], optional): The Stories within this List. Defaults to [].
        """
        self.id = id
        self.name: str = name
        self.user: User = user
        self.stories: set[Story] = stories

    def __repr__(self) -> str:
        return f"<List id={self.id}>"

    def _update_data(
        self,
        name: Optional[str] = None,
        user: Optional[User] = None,
        stories: Optional[set[Story]] = None,
    ):
        """Updates self.data with the provided arguments, overwriting any duplicate values with a preference towards provided arguments.

        Returns:
            None: Nothing is returned.
        """
        if name:
            self.name = name
        if user:
            self.user = user
        if stories:
            self.stories = stories
