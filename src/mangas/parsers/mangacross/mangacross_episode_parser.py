from typing import Any
from datetime import datetime, date
from pydantic import BaseModel

from ..parser_utils import JSONParserMixin


class MangaCrossEpisodeComic(BaseModel):
    title: str
    created_at: datetime
    updated_at: datetime
    dir_name: str
    author: list[str]
    comic_page_promotions: list[Any]


class MangaCrossEpisodeGeometry(BaseModel):
    width: int
    height: int


class MangaCrossEpisodeImage(BaseModel):
    pc_url: str
    sp_url: str
    thumbnail_url: str
    original_url: str
    pc_geometry: MangaCrossEpisodeGeometry
    sp_geometry: MangaCrossEpisodeGeometry
    thumbnail_geometry: MangaCrossEpisodeGeometry
    original_geometry: MangaCrossEpisodeGeometry


class MangaCrossEpisodePage(BaseModel):
    order_index: int
    image: MangaCrossEpisodeImage
    is_spread_start_page: bool


class MangaCrossEpisodePublishSpan(BaseModel):
    publish_start: datetime
    publish_end: None


class MangaCrossEpisodeViewerSetting(BaseModel):
    page_direction: str
    is_start_spread_page: bool
    page_direction_changeable: bool
    vertical_margin_enable: bool


class MangaCrossEpisodeParseOutput(BaseModel):
    sort_volume: int
    created_at: datetime
    updated_at: datetime
    volume: str
    title: str
    page_count: int
    episode_viewer_setting: MangaCrossEpisodeViewerSetting
    episode_publish_spans: list[MangaCrossEpisodePublishSpan]
    ogp: str
    thumbnail: str
    comic: MangaCrossEpisodeComic
    episode_pages: list[MangaCrossEpisodePage]


class MangaCrossEpisodeParser(JSONParserMixin):
    def parse(self, url: str):
        output = MangaCrossEpisodeParseOutput.model_validate_json(self._get_text(url))
        return output
