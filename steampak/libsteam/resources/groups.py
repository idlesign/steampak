import ctypes

from .base import _FriendsBase


class Group(_FriendsBase):
    """Exposes methods to get user groups (clans) data."""

    def __init__(self, group_id):
        self.group_id = group_id

    @property
    def stats(self):
        stats_online = ctypes.c_int()
        stats_ingame = ctypes.c_int()
        stats_chatting = ctypes.c_int()

        self._call(
            'GetClanActivityCounts', [
                self._handle, self.group_id,
                ctypes.byref(stats_online),
                ctypes.byref(stats_ingame),
                ctypes.byref(stats_chatting),
            ])

        return {
            'online': stats_online,
            'ingame': stats_ingame,
            'chatting': stats_chatting,
        }

    @property
    def name(self):
        """Name of a group.

        :return:
        """
        return self._get_str('GetClanName', (self._handle, self.group_id))

    @property
    def alias(self):
        """Alias (short name) of a group.

        :return:
        """
        return self._get_str('GetClanTag', (self._handle, self.group_id))


class Groups(_FriendsBase):
    """Exposes methods to get user groups data. Groups are also known as clans."""

    def __len__(self):
        """Returns a number of current user groups (clans).

        :rtype: int
        :return:
        """
        return self._call('GetClanCount', (self._handle,))

    def __call__(self):
        """Generator. Returns Group objects.

        :rtype: Group
        :return:
        """
        for idx in range(len(self)):
            yield Group(self._get_ptr('GetClanByIndex', (self._handle, idx)))
