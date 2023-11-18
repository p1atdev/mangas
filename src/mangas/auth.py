from pydantic import BaseModel


class AuthConfigMixin(BaseModel):
    def compose_header(self) -> dict[str, str]:
        raise NotImplementedError


class BearerAuthConfig(AuthConfigMixin):
    token: str

    def compose_header(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.token}"}
