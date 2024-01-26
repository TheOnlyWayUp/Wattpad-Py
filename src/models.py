"""Pydantic Models representing Wattpad API Responses. Thanks https://jsontopydantic.com. Thanks to Tushar Sadhwani (https://sadh.life) for helping me understand the Literal type (used in an earlier version of this code)."""

from __future__ import annotations

from typing import List, Optional, Literal, TypedDict
from typing_extensions import NotRequired

from pydantic import BaseModel, Field


class InboxModelFieldsType(TypedDict):
    unread: NotRequired[bool]
    total: NotRequired[bool]


class NotificationsModelFieldsType(TypedDict):
    unread: NotRequired[bool]


class ConnectedServicesModelFieldsType(TypedDict):
    facebook: NotRequired[bool]
    twitter: NotRequired[bool]


class UserModelFieldsType(TypedDict):
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
    id: NotRequired[bool]
    name: NotRequired[bool]


class PublishedModelFieldsType(TypedDict):
    id: NotRequired[bool]
    createDate: NotRequired[bool]


class PartModelFieldsType(TypedDict):
    id: NotRequired[bool]
    title: NotRequired[bool]
    url: NotRequired[bool]
    modifyDate: NotRequired[bool]
    createDate: NotRequired[bool]
    commentCount: NotRequired[bool]
    voteCount: NotRequired[bool]
    readCount: NotRequired[bool]


class TagRankingModelFieldsType(TypedDict):
    name: NotRequired[bool]
    rank: NotRequired[bool]
    total: NotRequired[bool]


class StoryModelFieldsType(TypedDict):
    id: NotRequired[bool]
    title: NotRequired[bool]
    createDate: NotRequired[bool]
    modifyDate: NotRequired[bool]
    voteCount: NotRequired[bool]
    readCount: NotRequired[bool]
    commentCount: NotRequired[bool]
    user: NotRequired[bool]
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


class ListModelFieldsType(TypedDict):
    id: NotRequired[bool]
    name: NotRequired[bool]

    stories: NotRequired[StoryModelFieldsType | bool]


class InboxModel(BaseModel):
    unread: int
    total: int


class NotificationsModel(BaseModel):
    unread: int


class ConnectedServicesModel(BaseModel):
    facebook: bool
    twitter: bool


class UserModel(BaseModel):
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

    following_users: list[UserModel] = []
    followed_by_users: list[UserModel] = []
    stories: List[StoryModel] = []
    lists: List[ListModel] = []


class LanguageModel(BaseModel):
    id: int
    name: str


class FirstPublishedPartModel(BaseModel):
    id: int
    create_date: str = Field(..., alias="createDate")


class LastPublishedPartModel(BaseModel):
    id: int
    create_date: str = Field(..., alias="createDate")


class PartModel(BaseModel):
    id: int
    title: str
    url: str
    modify_date: str = Field(..., alias="modifyDate")
    create_date: str = Field(..., alias="createDate")
    comment_count: int = Field(..., alias="commentCount")
    vote_count: int = Field(..., alias="voteCount")
    read_count: int = Field(..., alias="readCount")


class TagRankingModel(BaseModel):
    name: str
    rank: int
    total: int


class StoryModel(BaseModel):
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

    recommended: list[StoryModel] = []
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
    id: int
    name: str
    stories: List[StoryModel]
