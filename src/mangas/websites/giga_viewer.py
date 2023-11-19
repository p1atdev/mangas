from .website_utils import WebsiteMixin
from ..parsers import GigaAtomParser, GigaEpisodeParser
from ..url import URLConfig


# choJuGiga: baku 形式の website
class GigaViewer(WebsiteMixin):
    atom_parser: type[GigaAtomParser] = GigaAtomParser
    episode_parser: type[GigaEpisodeParser] = GigaEpisodeParser

    def parse_atom(self):
        atom = self.atom_parser(
            url=URLConfig.from_string(self.url.compose("atom"))
        ).parse()
        return atom

    def _parse_episode_id(self, url: str):
        return [component for component in url.split("/") if component.strip() != ""][
            -1
        ]

    def _get_episode_json(self, episode_id: str):
        return self.episode_parser(
            url=self.url.compose("atom", "series", episode_id)
        ).parse()
