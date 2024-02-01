"""Copyright (C) 2024 TheOnlyWayUp

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see https://www.gnu.org/licenses/.

---

Pydantic Models representing Wattpad API Responses. Thanks https://jsontopydantic.com."""

from __future__ import annotations


from typing import List, Optional
from pydantic import BaseModel, Field


class InboxModel(BaseModel):
    """Represents a User's Inbox."""

    unread: int
    total: int


class NotificationsModel(BaseModel):
    """Represents a User's Notifications."""

    unread: int


class ConnectedServicesModel(BaseModel):
    """Represents a User's Connected Services."""

    facebook: bool
    twitter: bool


class UserModel(BaseModel):
    """Represents a User."""

    username: str

    avatar: Optional[str] = None
    is_private: Optional[bool] = Field(None, alias="isPrivate")
    background_url: Optional[str] = Field(None, alias="backgroundUrl")
    follower: Optional[bool] = None
    following: Optional[bool] = None
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    gender: Optional[str] = None
    gender_code: Optional[str] = Field(None, alias="genderCode")
    language: Optional[int] = None
    locale: Optional[str] = None
    create_date: Optional[str] = Field(None, alias="createDate")
    modify_date: Optional[str] = Field(None, alias="modifyDate")
    location: Optional[str] = None
    verified: Optional[bool] = None
    ambassador: Optional[bool] = None
    facebook: Optional[str] = None
    twitter: Optional[str] = None
    website: Optional[str] = None
    lulu: Optional[str] = None
    smashwords: Optional[str] = None
    bubok: Optional[str] = None
    votes_received: Optional[int] = Field(None, alias="votesReceived")
    num_stories_published: Optional[int] = Field(None, alias="numStoriesPublished")
    num_following: Optional[int] = Field(None, alias="numFollowing")
    num_followers: Optional[int] = Field(None, alias="numFollowers")
    num_messages: Optional[int] = Field(None, alias="numMessages")
    num_lists: Optional[int] = Field(None, alias="numLists")
    verified_email: Optional[bool] = None
    preferred_categories: Optional[List] = None
    allow_crawler: Optional[bool] = Field(None, alias="allowCrawler")
    deeplink: Optional[str] = None
    is_muted: Optional[bool] = Field(None, alias="isMuted")
    birthdate: Optional[str] = None
    inbox: Optional[InboxModel] = None
    notifications: Optional[NotificationsModel] = None
    connected_services: Optional[ConnectedServicesModel] = Field(
        None, alias="connectedServices"
    )
    age: Optional[int] = None
    email: Optional[str] = None
    has_password: Optional[bool] = None


class LanguageModel(BaseModel):
    """Represents a Language."""

    id: int
    name: str


class FirstPublishedPartModel(BaseModel):
    """Represents the first published part of a Story."""

    id: int
    create_date: str = Field(..., alias="createDate")


class LastPublishedPartModel(BaseModel):
    """Represents the last (most recent) published part of a Story."""

    id: int
    create_date: str = Field(..., alias="createDate")


class PartModel(BaseModel):
    """Represents a Part of a Story."""

    id: int
    title: str
    url: str
    modify_date: str = Field(..., alias="modifyDate")
    create_date: str = Field(..., alias="createDate")
    comment_count: int = Field(..., alias="commentCount")
    vote_count: int = Field(..., alias="voteCount")
    read_count: int = Field(..., alias="readCount")


class TagRankingModel(BaseModel):
    """Represents a Story's Tag Rankings."""

    name: str
    rank: Optional[int] = None
    total: Optional[int] = None


class StoryModel(BaseModel):
    """Represents a Story."""

    id: str

    title: Optional[str] = None
    create_date: Optional[str] = Field(None, alias="createDate")
    modify_date: Optional[str] = Field(None, alias="modifyDate")
    vote_count: Optional[int] = Field(None, alias="voteCount")
    read_count: Optional[int] = Field(None, alias="readCount")
    comment_count: Optional[int] = Field(None, alias="commentCount")
    description: Optional[str] = None
    completed: Optional[bool] = None
    tags: Optional[List[str]] = None
    rating: Optional[int] = None
    mature: Optional[bool] = None
    url: Optional[str] = None
    is_paywalled: Optional[bool] = Field(None, alias="isPaywalled")
    cover: Optional[str] = None
    cover_timestamp: Optional[str] = None
    categories: Optional[List[int]] = None
    copyright: Optional[int] = None
    first_part_id: Optional[int] = Field(None, alias="firstPartId")
    num_parts: Optional[int] = Field(None, alias="numParts")
    deleted: Optional[bool] = None

    first_published_part: Optional[FirstPublishedPartModel] = Field(
        None, alias="firstPublishedPart"
    )
    last_published_part: Optional[LastPublishedPartModel] = Field(
        None, alias="lastPublishedPart"
    )
    language: Optional[LanguageModel] = None
    user: Optional[UserModel] = None
    parts: List[PartModel] = []
    tag_rankings: list[TagRankingModel] = Field([], alias="tagRankings")


class ListModel(BaseModel):
    """Represents a User's List."""

    id: int
    name: str
    stories: List[StoryModel]
