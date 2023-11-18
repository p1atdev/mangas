import feedparser

from pydantic import BaseModel, field_validator

from .parser_util import ParserMixin, Atom10ParseOutput


class GigaLink(BaseModel):
    href: str
    rel: str
    type: str
    length: int | None = None


class GigaTitleDetail(BaseModel):
    type: str
    language: str | None = None
    base: str
    value: str


class GigaFeed(BaseModel):
    title: str
    title_detail: GigaTitleDetail
    subtitle: str
    subtitle_detail: GigaTitleDetail
    updated: str
    id: str
    guidislink: bool
    link: str
    links: list[GigaLink]


class GigaAuthor(BaseModel):
    name: str


class GigaEntry(BaseModel):
    title: str
    title_detail: GigaTitleDetail
    links: list[GigaLink]
    link: str
    id: str
    guidislink: bool
    updated: str
    summary: str
    authors: list[GigaAuthor]
    author_detail: GigaAuthor
    author: str


class GigaAtomParseOutput(Atom10ParseOutput):
    feed: GigaFeed
    entries: list[GigaEntry]

    @field_validator("namespaces")
    def validate_namespaces(cls, v):
        if "giga" not in v:
            raise ValueError("giga namespace not found")
        return v


class GigaParser(ParserMixin):
    url: str

    def parse(self):
        atom = self._get_atom()
        return atom

    # atom 10 じゃない場合に分岐
    def _get_atom(self) -> GigaAtomParseOutput:
        atom = feedparser.parse(self.url)

        return GigaAtomParseOutput(**atom)
