import feedparser

from datetime import datetime
from pydantic import BaseModel, field_validator

from ..parser_utils import ParserMixin, Atom10ParseOutput
from ...url import URLConfig


class GigaAtomLink(BaseModel):
    href: str
    rel: str
    type: str
    length: int | None = None


class GigaAtomTitleDetail(BaseModel):
    type: str
    language: str | None = None
    base: str
    value: str


class GigaAtomFeed(BaseModel):
    title: str
    title_detail: GigaAtomTitleDetail
    subtitle: str
    subtitle_detail: GigaAtomTitleDetail
    updated: datetime
    id: str
    guidislink: bool
    link: str
    links: list[GigaAtomLink]


class GigaAtomAuthor(BaseModel):
    name: str


class GigaAtomEntry(BaseModel):
    title: str
    title_detail: GigaAtomTitleDetail
    links: list[GigaAtomLink]
    link: str
    id: str
    guidislink: bool
    updated: datetime
    summary: str
    authors: list[GigaAtomAuthor]
    author_detail: GigaAtomAuthor
    author: str


class GigaAtomParseOutput(Atom10ParseOutput):
    feed: GigaAtomFeed
    entries: list[GigaAtomEntry]

    @field_validator("namespaces")
    def validate_namespaces(cls, v):
        if "giga" not in v:
            raise ValueError("giga namespace not found")
        return v


class GigaAtomParser(ParserMixin):
    def parse(self, url: str):
        atom = self._get_atom(url)
        return atom

    # TODO: atom 10 じゃない場合に分岐、認証
    def _get_atom(self, url: str) -> GigaAtomParseOutput:
        atom = feedparser.parse(url, request_headers=self.auth.compose_headers())

        return GigaAtomParseOutput(**atom)
