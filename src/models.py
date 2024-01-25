from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


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
    total_stories: int = Field(0, alias="total")
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
    language: Optional[LanguageModel] = None
    user: Optional[UserModel] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    tags: Optional[List[str]] = None
    rating: Optional[int] = None
    mature: Optional[bool] = None
    url: Optional[str] = None
    first_published_part: Optional[FirstPublishedPartModel] = Field(
        None, alias="firstPublishedPart"
    )
    last_published_part: Optional[LastPublishedPartModel] = Field(
        None, alias="lastPublishedPart"
    )
    parts: List[PartModel] = []
    tag_rankings: list[TagRankingModel] = Field([], alias="tagRankings")
    is_paywalled: Optional[bool] = Field(None, alias="isPaywalled")

    cover: Optional[str] = None
    cover_timestamp: Optional[str] = None
    categories: Optional[List[int]] = None
    copyright: Optional[int] = None
    first_part_id: Optional[int] = Field(None, alias="firstPartId")
    num_parts: Optional[int] = Field(None, alias="numParts")
    deleted: Optional[bool] = None

    recommended: list[StoryModel] = []


class ListModel(BaseModel):
    id: int
    name: str
    stories: List[StoryModel]
