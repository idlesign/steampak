from threading import local

from ctyped.types import CRef
from ..exceptions import SteamApiError

if False:  # pragma: nocover
    from ._wrapper import Client


_API_THREAD_LOCAL = local()


def _set_client(client):
    setattr(_API_THREAD_LOCAL, 'steam_client', client)


class _EnumBase:
    """Enumeration base class."""

    aliases = {}

    @classmethod
    def get_alias(cls, item_id):
        """Returns item alias by ID.

        :param int item_id: Item ID.
        :rtype: str
        """
        return cls.aliases.get(item_id)


class _ApiResourceBase:
    """Base class for Steam API classes describing various resources
    (friends, stats, music, etc.).

    """

    def __init__(self, *args, **kwargs):
        pass

    def _get_str(self, func, args, max_len=300):

        value = CRef.carray(str, size=max_len)
        args.extend([value, max_len])
        result = func(*args)

        if (isinstance(result, bool) and not result) or result == -1:
            return ''

        return str(value)

    @classmethod
    def get_client(cls):
        """

        :rtype: Client
        """
        client = getattr(_API_THREAD_LOCAL, 'steam_client', None)

        if client is None:
            raise SteamApiError('You need to initialize Api.')

        return client


class FriendFilter:
    """Filters to be provided to functions returning friends.
    Can be combined using `|`.

    """
    NONE = 0x00
    BLOCKED = 0x01
    FRIENDSHIP_REQUESTED = 0x02
    IMMEDIATE = 0x04  # "REGULAR" FRIEND
    CLAN_MEMBER = 0x08
    ON_GAME_SERVER = 0x10
    HAS_PLAYED_WITH = 0x20  # NOT CURRENTLY USED
    FRIEND_OF_FRIEND = 0x40  # NOT CURRENTLY USED
    REQUESTING_FRIENDSHIP = 0x80
    REQUESTING_INFO = 0x100
    IGNORED = 0x200
    IGNORED_FRIEND = 0x400
    SUGGESTED = 0x800
    CHAT_MEMBER = 0x1000
    ALL = 0xFFFF
