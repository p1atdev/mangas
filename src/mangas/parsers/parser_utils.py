import json
import requests
from pydantic import BaseModel

from ..auth import AuthConfigMixin, DefaultAuthConfig


class ParserMixin(BaseModel):
    auth: AuthConfigMixin = DefaultAuthConfig


class JSONParserMixin(ParserMixin):
    def _get_text(self, url: str):
        res = requests.get(url, headers=self.auth.compose_headers())
        return res.text

    def _get_json(self, url: str):
        return json.loads(self._get_text(url))


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
