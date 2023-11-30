from enum import Enum
from typing import Any, Literal
from datetime import datetime, date
from pydantic import BaseModel

from ..parser_utils import JSONParserMixin

from .ichijin_plus_common import IchijinPlusNsfwType


class IchijinPlusSeriesAuthor(BaseModel):
    creator_id: str
    name: str
    role: str


class IchijinPlusSeriesGenre(BaseModel):
    id: str
    name: str
    comics_count: int


class IchijinPlusSeriesLabel(BaseModel):
    id: str
    name: str
    name_yomigana: str
    logo_image_url: str
    name_alias: str
    primary_color: str
    background_color: str
    catchphrase: str | None


class IchijinPlusSeriesLatestEpisode(BaseModel):
    id: str
    comic_id: str
    title: str
    thumbnail_image_url: str
    published_at: datetime
    episode_status: Literal["free_viewing"]
    episode_order: int
    price: int
    expire_seconds: None
    promotion: str


class IchijinPlusSeriesParseOutput(BaseModel):
    id: str
    title: str
    title_yomigana: str
    description: str
    description_tag: str
    copyright: None
    cover_image_url: str
    next_episode_update_at: None
    nsfw_type: IchijinPlusNsfwType
    latest_episode: IchijinPlusSeriesLatestEpisode
    authors: list[IchijinPlusSeriesAuthor]
    labels: list[IchijinPlusSeriesLabel]
    genres: list[IchijinPlusSeriesGenre]
    curations: list[Any]
    good_count: int


class IchijinPlusSeriesParser(JSONParserMixin):
    def parse(self, url: str):
        output = IchijinPlusSeriesParseOutput.model_validate_json(self._get_text(url))
        return output
