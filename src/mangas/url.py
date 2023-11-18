from pydantic import BaseModel


class URLConfig(BaseModel):
    scheme: str = "https"
    domain: str

    def compose(self, *args, **kwargs):
        return "/".join([self.scheme + "://" + self.domain, *args]).format(**kwargs)
