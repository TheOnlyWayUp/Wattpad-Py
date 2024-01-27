"""Copyright (C) 2024 TheOnlyWayUp

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see https://www.gnu.org/licenses/.

---

Typehints for the models in `./models.py`. These types are used to specify what fields to request in API-Interfacing methods."""

from __future__ import annotations

from typing import TypedDict
from typing_extensions import NotRequired


class InboxModelFieldsType(TypedDict):
    """Typehints for the Inbox model."""

    unread: NotRequired[bool]
    total: NotRequired[bool]


class NotificationsModelFieldsType(TypedDict):
    """Typehints for the Notifications model."""

    unread: NotRequired[bool]


class ConnectedServicesModelFieldsType(TypedDict):
    """Typehints for the Notifications model."""

    facebook: NotRequired[bool]
    twitter: NotRequired[bool]


class UserModelFieldsType(TypedDict):
    """Typehints for the User model."""

    username: NotRequired[bool]
    avatar: NotRequired[bool]
    isPrivate: NotRequired[bool]
    backgroundUrl: NotRequired[bool]
    follower: NotRequired[bool]
    following: NotRequired[bool]
    name: NotRequired[bool]
    description: NotRequired[bool]
    status: NotRequired[bool]
    gender: NotRequired[bool]
    genderCode: NotRequired[bool]
    language: NotRequired[bool]
    locale: NotRequired[bool]
    createDate: NotRequired[bool]
    modifyDate: NotRequired[bool]
    location: NotRequired[bool]
    verified: NotRequired[bool]
    ambassador: NotRequired[bool]
    facebook: NotRequired[bool]
    twitter: NotRequired[bool]
    website: NotRequired[bool]
    lulu: NotRequired[bool]
    smashwords: NotRequired[bool]
    bubok: NotRequired[bool]
    votesReceived: NotRequired[bool]
    numStoriesPublished: NotRequired[bool]
    numFollowing: NotRequired[bool]
    numFollowers: NotRequired[bool]
    numMessages: NotRequired[bool]
    numLists: NotRequired[bool]
    verified_email: NotRequired[bool]
    preferred_categories: NotRequired[bool]
    allowCrawler: NotRequired[bool]
    deeplink: NotRequired[bool]
    isMuted: NotRequired[bool]
    birthdate: NotRequired[bool]
    age: NotRequired[int]
    email: NotRequired[bool]
    has_password: NotRequired[bool]

    inbox: NotRequired[InboxModelFieldsType | bool]
    notifications: NotRequired[NotificationsModelFieldsType | bool]
    connectedServices: NotRequired[ConnectedServicesModelFieldsType | bool]


class LanguageModelFieldsType(TypedDict):
    """Typehints for the Language model."""

    id: NotRequired[bool]
    name: NotRequired[bool]


class PublishedModelFieldsType(TypedDict):
    """Typehints for the Published model (for the firstPublishedPart and lastPublishedPart fields)."""

    id: NotRequired[bool]
    createDate: NotRequired[bool]


class PartModelFieldsType(TypedDict):
    """Typehints for the Part model."""

    id: NotRequired[bool]
    title: NotRequired[bool]
    url: NotRequired[bool]
    modifyDate: NotRequired[bool]
    createDate: NotRequired[bool]
    commentCount: NotRequired[bool]
    voteCount: NotRequired[bool]
    readCount: NotRequired[bool]


class TagRankingModelFieldsType(TypedDict):
    """Typehints for the TagRankings model."""

    name: NotRequired[bool]
    rank: NotRequired[bool]
    total: NotRequired[bool]


class StoryModelFieldsType(TypedDict):
    """Typehints for the Story model."""

    id: NotRequired[bool]
    title: NotRequired[bool]
    createDate: NotRequired[bool]
    modifyDate: NotRequired[bool]
    voteCount: NotRequired[bool]
    readCount: NotRequired[bool]
    commentCount: NotRequired[bool]
    description: NotRequired[bool]
    completed: NotRequired[bool]
    tags: NotRequired[bool]
    rating: NotRequired[bool]
    mature: NotRequired[bool]
    url: NotRequired[bool]
    isPaywalled: NotRequired[bool]
    cover: NotRequired[bool]
    cover_timestamp: NotRequired[bool]
    categories: NotRequired[bool]
    copyright: NotRequired[bool]
    firstPartId: NotRequired[bool]
    numParts: NotRequired[bool]
    deleted: NotRequired[bool]

    parts: NotRequired[PartModelFieldsType | bool]
    tagRankings: NotRequired[TagRankingModelFieldsType | bool]
    firstPublishedPart: NotRequired[PublishedModelFieldsType | bool]
    lastPublishedPart: NotRequired[PublishedModelFieldsType | bool]
    language: NotRequired[LanguageModelFieldsType | bool]
    user: NotRequired[UserModelFieldsType | bool]


class ListModelFieldsType(TypedDict):
    """Typehints for the List model."""

    id: NotRequired[bool]
    name: NotRequired[bool]

    stories: NotRequired[StoryModelFieldsType | bool]
