import ctypes

from .base import _ApiResourceBase


class Group(_ApiResourceBase):
    """Exposes methods to get user groups (clans) data.

    Instances can be accessed through ``api.groups()``:

    .. code-block:: python

        for group in api.groups():
            print(group.name)

    """

    _res_name = 'ISteamFriends'

    def __init__(self, group_id):
        self.group_id = group_id

    @property
    def stats(self):
        """Basic group statistics.

        Returned dict has the following keys:

            'online' - users online count
            'ingame' - users currently in game count
            'chatting' - users chatting count

        :return: dict
        """
        stats_online = ctypes.c_int()
        stats_ingame = ctypes.c_int()
        stats_chatting = ctypes.c_int()

        self._call(
            'GetClanActivityCounts', [
                self._ihandle(), self.group_id,
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

        :rtype: str
        """
        return self._get_str('GetClanName', (self._ihandle(), self.group_id))

    @property
    def alias(self):
        """Alias (short name) of a group.

        :rtype: str
        """
        return self._get_str('GetClanTag', (self._ihandle(), self.group_id))

    def show_page(self):
        """Shows overlay with group page."""
        self._call('ActivateGameOverlayToUser', (self._ihandle(), 'steamid', self.group_id))

    def open_chat(self):
        """Shows overlay with group chat window."""
        self._call('ActivateGameOverlayToUser', (self._ihandle(), 'chat', self.group_id))


class Groups(_ApiResourceBase):
    """Exposes methods to get user groups data. Groups are also known as clans.

    Interface can be accessed through ``api.groups()``:

    .. code-block:: python

        for group in api.groups():
            print(group.name)

    """

    _res_name = 'ISteamFriends'

    def __len__(self):
        """Returns a number of current user groups (clans).

        :rtype: int
        """
        return self._call('GetClanCount', (self._ihandle(),))

    def __call__(self):
        """Generator. Returns Group objects.

        :rtype: Group
        """
        for idx in range(len(self)):
            yield Group(self._get_ptr('GetClanByIndex', (self._ihandle(), idx)))
