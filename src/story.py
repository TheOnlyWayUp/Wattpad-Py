from typing import Optional, cast
from models import (
    StoryModel,
    UserModel,
    UserModelFieldsType,
    StoryModelFieldsType,
)
from utils import get_fields, build_url, fetch_url, singleton


@singleton
class Story:
    """Story Model"""

    def __init__(self, id: str, **kwargs):
        self.id = id.lower()
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

        self.data.recommended = [StoryModel(**story) for story in data]

        return data
