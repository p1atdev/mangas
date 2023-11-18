import time
from pydantic import BaseModel


class ParserMixin(BaseModel):
    pass


class Atom10ParseOutput(BaseModel):
    namespaces: dict[str, str]
    version: str
    encoding: str
    status: int
    href: str
    headers: dict[str, str]
    feed: dict
    entries: list[dict[str, str]]
    bozo: int | None
