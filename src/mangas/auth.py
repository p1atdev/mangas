from pydantic import BaseModel


class DeviceEnvironment(BaseModel):
    user_agent: str


FirefoxPC = DeviceEnvironment(
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0"
)
FirefoxMobile = DeviceEnvironment(
    user_agent="Mozilla/5.0 (Android 11; Mobile; rv:92.0) Gecko/92.0 Firefox/92.0"
)
ChromePC = DeviceEnvironment(
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4585.0 Safari/537.36"
)
ChromeMobile = DeviceEnvironment(
    user_agent="Mozilla/5.0 (Linux; Android 11; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4585.0 Mobile Safari/537.36"
)
SafariPC = DeviceEnvironment(
    user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 11_5_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15"
)
SafariMobile = DeviceEnvironment(
    user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"
)


class AuthConfigMixin(BaseModel):
    user_agent: str | None = None

    def compose_headers(self) -> dict[str, str]:
        if self.user_agent is None:
            return {}

        return {
            "User-Agent": self.user_agent,
        }


DefaultAuthConfig = AuthConfigMixin()


class BearerAuthConfig(AuthConfigMixin):
    token: str

    def compose_headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.token}",
            **super().compose_headers(),
        }
