from typing import Any
from datetime import datetime, date
from pydantic import BaseModel

from ..parser_util import JSONParserMixin


class MangaCrossEpisodeViewerComic(BaseModel):
    title: str
    created_at: datetime
    updated_at: datetime
    dir_name: str
    author: list[str]
    comic_page_promotions: list[Any]


class MangaCrossEpisodeViewerGeometry(BaseModel):
    width: int
    height: int


class MangaCrossEpisodeViewerImage(BaseModel):
    pc_url: str
    sp_url: str
    thumbnail_url: str
    original_url: str
    pc_geometry: MangaCrossEpisodeViewerGeometry
    sp_geometry: MangaCrossEpisodeViewerGeometry
    thumbnail_geometry: MangaCrossEpisodeViewerGeometry
    original_geometry: MangaCrossEpisodeViewerGeometry


class MangaCrossEpisodeViewerEpisodePage(BaseModel):
    order_index: int
    image: MangaCrossEpisodeViewerImage
    is_spread_start_page: bool


class MangaCrossEpisodeViewerEpisodePublishSpan(BaseModel):
    publish_start: datetime
    publish_end: None


class MangaCrossEpisodeViewerEpisodeViewerSetting(BaseModel):
    page_direction: str
    is_start_spread_page: bool
    page_direction_changeable: bool
    vertical_margin_enable: bool


class MangaCrossEpisodeViewerParseOutput(BaseModel):
    sort_volume: int
    created_at: datetime
    updated_at: datetime
    volume: str
    title: str
    page_count: int
    episode_viewer_setting: MangaCrossEpisodeViewerEpisodeViewerSetting
    episode_publish_spans: list[MangaCrossEpisodeViewerEpisodePublishSpan]
    ogp: str
    thumbnail: str
    comic: MangaCrossEpisodeViewerComic
    episode_pages: list[MangaCrossEpisodeViewerEpisodePage]


class MangaCrossEpisodeViewerParser(JSONParserMixin):
    url: str

    def parse(self):
        output = MangaCrossEpisodeViewerParseOutput.model_validate_json(
            self._get_text(self.url)
        )
        return output
