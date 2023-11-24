from typing import Literal, Any
from datetime import datetime
from pydantic import BaseModel

from ..parser_utils import JSONParserMixin

IchijinPlusComicsNsfwInclude = Literal["all"] | None
IchijinPlusComicsSortOrder = Literal["asc", "desc"]
IchijinPlusComicsSortBy = Literal["title_yomigana"]


class IchijinPlusComicsAuthor(BaseModel):
    creator_id: str
    name: str
    role: str


class IchijinPlusComicsGenre(BaseModel):
    id: str
    name: str
    comics_count: int


class IchijinPlusComicsLabel(BaseModel):
    id: str
    name: str
    name_yomigana: str
    logo_image_url: str
    name_alias: str
    primary_color: str
    background_color: str
    catchphrase: str | None = None


IchijinPlusComicsNsfwType = Literal["any", "none"]


class IchijinPlusComicsLatestEpisode(BaseModel):
    id: str
    comic_id: str
    title: str
    thumbnail_image_url: str
    published_at: datetime
    episode_status: Literal["free_viewing"]
    episode_order: int
    price: int
    expire_seconds: None
    promotion: IchijinPlusComicsNsfwType


class IchijinPlusComicsResource(BaseModel):
    id: str
    title: str
    title_yomigana: str
    description: str
    description_tag: str
    cover_image_url: str
    nsfw_type: IchijinPlusComicsNsfwType
    authors: list[IchijinPlusComicsAuthor]
    labels: list[IchijinPlusComicsLabel]
    genres: list[IchijinPlusComicsGenre]
    curations: list[Any]
    good_count: int
    copyright: str | None = None
    next_episode_update_at: datetime | None = None
    latest_episode: IchijinPlusComicsLatestEpisode | None = None


class IchijinPlusComicsParseOutput(BaseModel):
    nsfw_count: int
    next_cursor: str
    resources: list[IchijinPlusComicsResource]


class IchijinPlusComicsParser(JSONParserMixin):
    def parse(self, url: str):
        output = IchijinPlusComicsParseOutput.model_validate_json(self._get_text(url))
        return output
