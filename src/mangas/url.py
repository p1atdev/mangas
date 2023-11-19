from pydantic import BaseModel


class URLConfig(BaseModel):
    scheme: str = "https"
    hostname: str
    pathname: str = ""
    query: dict[str, str] = {}

    def compose(
        self,
        *args,
    ):
        url = "/".join([self.scheme + "://" + self.hostname + self.pathname, *args])
        query_string = (
            "&".join([f"{key}={value}" for key, value in self.query.items()])
            if len(self.query.keys()) > 0
            else None
        )
        if query_string is not None:
            url += "?" + query_string

        return url

    @classmethod
    def from_string(cls, url: str):
        scheme, body = url.split("://")
        hostname, *args = body.split("/")
        pathname = "/".join(args)
        query = {}
        if len(pathname.split("?")) == 2:
            pathname, query_string = pathname.split("?")
            query = dict([query.split("=") for query in query_string.split("&")])
        if pathname != "":
            pathname = "/" + pathname

        return cls(
            scheme=scheme,
            hostname=hostname,
            pathname=pathname,
            query=query,
        )
