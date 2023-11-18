from ..url import URLConfig
from .giga_viewer import GigaViewer


class HerosWeb(GigaViewer):
    url: URLConfig = URLConfig(
        scheme="https",
        domain="viewer.heros-web.com",
    )
