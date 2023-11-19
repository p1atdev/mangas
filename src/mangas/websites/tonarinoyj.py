from ..url import URLConfig
from .giga_viewer import GigaViewer


class TonariNoYoungJump(GigaViewer):
    url: URLConfig = URLConfig(
        scheme="https",
        hostname="tonarinoyj.jp",
    )
