import feedparser

from ..url import URLConfig
from .website_utils import WebsiteMixin
from ..parsers import GigaParser, ParserMixin


# choJuGiga: baku 形式の website
class GigaViewer(WebsiteMixin):
    parser: type[GigaParser] = GigaParser

    def parse_atom(self):
        atom = self.parser(url=self.url.compose("atom")).parse()
        return atom
