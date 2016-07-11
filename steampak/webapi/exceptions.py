from ..exceptions import SteampakError


class SteamWebApiError(SteampakError):
    """Base Steam Web API exception class."""


class ResponseError(SteamWebApiError):
    """Exception generated on server response errors."""

    def __init__(self, description, url):
        self.description = description
        self.url = url

    def __str__(self):
        return self.description
