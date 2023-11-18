from ..url import URLConfig
from .giga_viewer import GigaViewer


class ShonenJumpPlus(GigaViewer):
    url: URLConfig = URLConfig(
        scheme="https",
        domain="shonenjumpplus.com",
    )
