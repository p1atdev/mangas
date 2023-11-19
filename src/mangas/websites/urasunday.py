from ..url import URLConfig
from .website_utils import WebsiteMixin


class UraSunday(WebsiteMixin):
    url = URLConfig(
        scheme="https",
        hostname="urasunday.com",
    )