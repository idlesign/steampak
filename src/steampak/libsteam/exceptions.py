from ..exceptions import SteampakError


class SteamApiError(SteampakError):
    """Base Steam API exception class."""


class SteamApiStartupError(SteamApiError):
    """Errors raised when trying to bootstrap API."""
