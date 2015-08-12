class SteamApiError(Exception):
    """Base Steam API exception class."""


class SteamApiStartupError(SteamApiError):
    """Errors raised when trying to bootstrap API."""
