import logging
from collections import namedtuple
from threading import local


LIBRARY_PATH = None
API_THREAD_LOCAL = local()
LOGGER = logging.getLogger('steampak.libsteam')

# Function argument which will contain additional function result.
# Expects ctypes type as a parameter.
ResultArg = namedtuple('ResultArg', ['ctype'])


class _EnumBase(object):
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

    def __init__(self, iface=None):  # todo remove none
        self.iface = iface


class FriendFilter(object):
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
    ALL = 0xFFFF
