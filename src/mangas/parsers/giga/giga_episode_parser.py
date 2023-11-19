import json
import requests

from typing import Literal
from datetime import datetime
from pydantic import BaseModel, field_validator, ConfigDict

from ..parser_utils import JSONParserMixin
from ...utils import ForceCamelCaseModel


class GigaEpisodePage(ForceCamelCaseModel):
    type: Literal["backMatter", "link", "main", "other"]
    content_start: str | None = None
    content_end: str | None = None
    link_position: str | None = None
    height: int | None = None
    src: str | None = None
    width: int | None = None


class GigaEpisodePageStructure(ForceCamelCaseModel):
    cho_ju_giga: str
    pages: list[GigaEpisodePage]
    reading_direction: str
    start_position: str


class GigaEpisodeSeries(ForceCamelCaseModel):
    id: str
    thumbnail_uri: str
    title: str


class GigaEpisodeReadableProduct(ForceCamelCaseModel):
    has_purchased: bool
    id: str
    image_uris_digest: str | None
    is_public: bool
    next_readable_product_uri: str | None
    # 基本的に話数の番号を表すが、13.5のような浮動小数点が入ることもある
    number: float
    page_structure: GigaEpisodePageStructure | None  # None になるのは未購入の場合など
    permalink: str
    published_at: datetime
    series: GigaEpisodeSeries
    title: str
    type_name: str
    point_gettable_episode_when_complete_reading: None
    prev_readable_product_uri: str | None
    toc: None
    finish_reading_notification_uri: str | None = None


class GigaEpisodeParseOutput(ForceCamelCaseModel):
    readable_product: GigaEpisodeReadableProduct


class GigaEpisodeParser(JSONParserMixin):
    def parse(self, url: str):
        output = GigaEpisodeParseOutput.model_validate_json(self._get_text(url))
        return output
