import ctypes
import logging
from os import environ
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
        return cls.aliases.get(item_id)


def get_library(lib_path=None):
    """Returns a library interface object.

    :param str lib_path: Full path to a library file `libsteam_api.so`.
    :return:
    """
    lib = getattr(API_THREAD_LOCAL, 'lib', None)

    if lib is not None:
        return lib

    global LIBRARY_PATH

    if LIBRARY_PATH is None:
        LIBRARY_PATH = lib_path

    lib = ctypes.CDLL(LIBRARY_PATH)
    if lib._name is None:
        lib = None

    API_THREAD_LOCAL.lib = lib
    return lib


class _ApiResourceBase(object):
    """Base class for Steam API classes describing various resources
    (friends, stats, music, etc.).

    """

    _res_name = ''
    _cache_handle = None

    @classmethod
    def set_app_id(cls, app_id):
        """Sets current application ID into environment.

        :param str|int app_id:
        :return:
        """
        if app_id:
            environ['SteamAppId'] = str(app_id)  # SteamGameId

    @classmethod
    def _get_api_func_name(cls, short_name):
        """Returns a full API function name constructed by adding a prefix
        and resource name (steam interface name).

        :param str short_name:
        :rtype: str
        :return:
        """
        base_prefix = 'SteamAPI'
        resource_name = cls._res_name
        if resource_name:
            resource_name = '_%s' % resource_name
        return ('%s%s_%s' % (base_prefix, resource_name, short_name)).replace('__', '_')

    @classmethod
    def _call_direct(cls, func_name, args=None, restype=None):
        """Performs API function call and returns its result.

        :param str func_name: Full name of a function w/o prefix and resource name.
        :param list|tuple args: Arguments to be passed to function.
        :param _SimpleCData restype: Ctypes type of function result.
        :return:
        """
        if args is None:
            args = []

        result_args = []
        for arg_idx, arg in enumerate(args):
            c_type = getattr(arg, 'ctype', None)  # ResultArg
            if c_type:
                arg = c_type()
                result_args.append(arg)
                args[arg_idx] = ctypes.byref(arg)

        func = getattr(get_library(), func_name)

        if restype is not None:
            func.restype = restype

        result = None
        try:
            result = func(*args)
        finally:
            LOGGER.debug('    ** %s args:  %s | result: %s' % (func_name, args, result))

        if result_args:
            result = [result]
            result.extend([getattr(arg, 'value', arg) for arg in result_args])
        
        return result

    @classmethod
    def _call(cls, func_name, args=None, restype=None):
        """Performs API function call and returns its result.

        :param str func_name: Short name of a function w/o prefix and resource name.
        :param list|tuple  args: Arguments to be passed to function.
        :param _SimpleCData restype: Ctypes type of function result.
        :return:
        """
        return cls._call_direct(cls._get_api_func_name(func_name), args, restype=restype)

    @classmethod
    def _get_str(cls, func_name, args=None, decode=True):
        """Performs API function call and returns result as a string.

        :param str func_name: Short name of a function w/o prefix and resource name.
        :param list|tuple args:Arguments to be passed to function.
        :param bool decode: Whether to decode bytestring to utf-8.
        :rtype: str
        :return:
        """
        result = cls._call(func_name, args, restype=ctypes.c_char_p)
        if not decode:
            return result
        return cls._str_decode(result)

    @classmethod
    def _str_decode(cls, val):
        """Decodes a given bytestring into utf-8.

        :param bytes|str val: Bytestring.
        :rtype: str
        :return:
        """
        return val.decode('utf-8')

    @classmethod
    def _get_ptr(cls, func_name, args=None):
        """Performs API function call and returns a pointer to a result.

        :param str func_name: Short name of function w/o prefix and resource name.
        :param list|tuple args: Arguments to be passed to function.
        :return:
        """
        return ctypes.c_void_p(cls._call(func_name, args, restype=ctypes.c_void_p))

    @classmethod
    def _get_bool(cls, func_name, args=None):
        """Performs API function call and returns result as bool.

        :param str func_name: Short name of function w/o prefix and resource name.
        :param list|tuple  args:Arguments to be passed to function.
        :rtype: bool
        :return:
        """
        return cls._call(func_name, args, restype=ctypes.c_bool)

    @property
    def _handle(self):
        if self._cache_handle is None:
            self.__class__._cache_handle = getattr(
                get_library(), self._res_name.replace('I', ''))()
        return self._cache_handle


class _FriendsBase(_ApiResourceBase):
    """Base class for functions encapsulated under ISteamFriends.
    Used as base for various steampak classes to improve API usability.

    """
    _res_name = 'ISteamFriends'


class FriendFilter(object):
    """Filters to be provided to functions returning friends.
    Can be combined using |.

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
