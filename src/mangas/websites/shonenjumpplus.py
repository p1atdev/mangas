import requests
import random

from ..url import URLConfig
from .giga_viewer import GigaViewer
from ..auth import AuthConfigMixin, ChromePC


ShonenJumpPlusURL = URLConfig(
    scheme="https",
    hostname="shonenjumpplus.com",
)


class ShonenJumpPlusAuthConfig(AuthConfigMixin):
    _url: URLConfig = ShonenJumpPlusURL

    user_agent: str = ChromePC.user_agent

    token: str | None = None

    def compose_headers(self) -> dict[str, str]:
        headers = super().compose_headers()

        if self.token is not None:
            headers["Cookie"] = f"glsc={self.token}"

        return headers


class ShonenJumpPlus(GigaViewer):
    auth: ShonenJumpPlusAuthConfig = ShonenJumpPlusAuthConfig()
    url: URLConfig = ShonenJumpPlusURL

    def login(self, email: str, password: str) -> ShonenJumpPlusAuthConfig:
        headers = self.auth.compose_headers()
        boundary = self._random_boundary()
        headers["Content-Type"] = "multipart/form-data; boundary=" + boundary
        headers["X-Requested-With"] = "XMLHttpRequest"

        data = (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="email_address"\r\n\r\n'
            f"{email}\r\n"
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="password"\r\n\r\n'
            f"{password}\r\n"
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="return_location_path"\r\n\r\n'
            f"/\r\n"
            f"--{boundary}--\r\n"
        )

        res = requests.post(
            url=self.url.compose(pathname="/user_account/login"),
            headers=headers,
            data=data,
        )

        cookies = res.cookies.get_dict()
        token = cookies.get("glsc")

        if token is None:
            raise Exception("Login failed")

        auth = ShonenJumpPlusAuthConfig(
            token=token,
            **self.auth.model_dump(exclude=set(["token"])),
        )

        return auth

    @classmethod
    def _random_boundary(cls, length: int = 30):
        return "---------------------------" + "".join(
            [str(random.randint(0, 9)) for _ in range(length)]
        )
