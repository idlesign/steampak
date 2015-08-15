from datetime import datetime

from .base import _ApiResourceBase, _EnumBase


class Universe(_EnumBase):

    INVALID = 0
    PUBLIC = 1
    BETA = 2
    INTERNAL = 3
    DEV = 4
    MAX = 5

    aliases = {
        INVALID: 'invalid',
        PUBLIC: 'public',
        BETA: 'beta',
        INTERNAL: 'internal',
        DEV: 'dev',
        MAX: 'max',
    }


class NotificationPosition(object):

    TOP_LEFT = 0
    TOP_RIGHT = 1
    BOTTOM_LEFT = 2
    BOTTOM_RIGHT = 3


class Utils(_ApiResourceBase):
    """Exposes various utility methods.

    Interface can be accessed through ``api.utils``:

    .. code-block:: python

        print(api.utils.ui_language)

    """

    _res_name = 'ISteamUtils'

    @property
    def seconds_app_active(self):
        """Number seconds application is active.

        :rtype: int
        """
        # todo works?
        return self._call('GetSecondsSinceAppActive', (self._ihandle(),))

    @property
    def seconds_computer_active(self):
        """Number seconds computer is active.

        :rtype: int
        """
        # todo works?
        return self._call('GetSecondsSinceComputerActive', (self._ihandle(),))

    @property
    def server_time(self):
        """Date and time on server.

        :rtype: datetime
        """
        return datetime.utcfromtimestamp(self._call('GetServerRealTime', (self._ihandle(),)))

    @property
    def country_code(self):
        """2 digit ISO 3166-1-alpha-2 format country code this client is running in
        (as looked up via an IP-to-location database)

        E.g: RU.

        :rtype: str
        """
        return self._get_str('GetIPCountry', (self._ihandle(),))

    @property
    def battery_power(self):
        """The amount of battery power left in the current system in % [0..100].
        255 for being on AC power.

        :rtype: int
        """
        return self._call('GetCurrentBatteryPower', (self._ihandle(),))

    @property
    def app_id(self):
        """Application ID of the current process.

        :rtype: int
        """
        return self._call('GetAppID', (self._ihandle(),))

    def set_notification_position(self, position):
        """Sets the position where the overlay instance for the currently
        calling game should show notifications.

        This position is per-game and if this function is called from outside
        of a game context it will do nothing.

        :param int position: Position. See ``NotificationPosition``.
        """
        return self._call('SetOverlayNotificationPosition', (self._ihandle(), position))

    @property
    def overlay_enabled(self):
        """``True`` if the overlay is running & the user can access it.

        The overlay process could take a few seconds to start & hook the game process,
        so this function will initially return ``False`` while the overlay is loading.

        :rtype: bool
        """
        return self._get_bool('IsOverlayEnabled', (self._ihandle(),))

    @property
    def vr_mode(self):
        """``True``  if Steam itself is running in VR mode.

        :rtype: bool
        """
        return self._get_bool('IsSteamRunningInVR', (self._ihandle(),))

    def get_universe(self, as_str=False):
        """Returns universe the client is connected to. See ``Universe``.

        :param bool as_str: Return human-friendly universe name instead of an ID.
        :rtype: int|str
        """
        result = self._call('GetConnectedUniverse', (self._ihandle(),))

        if as_str:
            return Universe.get_alias(result)

        return result

    @property
    def universe(self):
        """Universe the client is connected to.

        :rtype: str
        """
        return self.get_universe(as_str=True)

    @property
    def ipc_call_count(self):
        """The number of IPC calls made since the last time this function was called.
        Used for perf debugging so you can understand how many IPC calls your game makes per frame.
        Every IPC call is at minimum a thread context switch if not a process one
        so you want to rate control how often you do them.

        :rtype: int
        """
        return self._call('GetIPCCallCount', (self._ihandle(),))

    @property
    def ui_language(self):
        """The language the steam client is running in.

        E.g.: russian

        :rtype: str
        """
        return self._get_str('GetSteamUILanguage', (self._ihandle(),))
