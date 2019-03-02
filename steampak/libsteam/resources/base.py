from collections import namedtuple

if False:  # pragma: nocover
    from ._wrapper import Client

# Function argument which will contain additional function result.
# Expects ctypes type as a parameter.
ResultArg = namedtuple('ResultArg', ['ctype'])


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

    _iface = None
    _client = None  # type: Client

    def __init__(self, *, _contribute=None, **kwargs):
        _contribute and _contribute(self)

    def _contribute_internals(self, to, *, iface=None, client=None):
        to._iface = iface or self._iface
        to._client = client or self._client


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
