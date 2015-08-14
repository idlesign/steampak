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


class NotificationPosition(_EnumBase):

    TOP_LEFT = 0
    TOP_RIGHT = 1
    BOTTOM_LEFT = 2
    BOTTOM_RIGHT = 3


class Utils(_ApiResourceBase):
    """Exposes various utility methods."""

    _res_name = 'ISteamUtils'

    @property
    def seconds_app_active(self):
        """Number seconds application is active.

        :rtype: int
        :return:
        """
        # todo is it working at all?
        return self._call('GetSecondsSinceAppActive', (self._handle,))

    @property
    def seconds_computer_active(self):
        """Number seconds computer is active.

        :rtype: int
        :return:
        """
        # todo is it working at all?
        return self._call('GetSecondsSinceComputerActive', (self._handle,))

    @property
    def server_time(self):
        """Date and time on server.

        :rtype: datetime
        :return:
        """
        return datetime.utcfromtimestamp(self._call('GetServerRealTime', (self._handle,)))

    @property
    def country_code(self):
        """2 digit ISO 3166-1-alpha-2 format country code this client is running in
        (as looked up via an IP-to-location database) e.g "RU".

        :rtype: str
        :return:
        """
        return self._get_str('GetIPCountry', (self._handle,))

    @property
    def battery_power(self):
        """The amount of battery power left in the current system in % [0..100].
        255 for being on AC power.

        :rtype: int
        :return:
        """
        return self._call('GetCurrentBatteryPower', (self._handle,))

    @property
    def app_id(self):
        """Application ID of the current process.

        :return:
        """
        return self._call('GetAppID', (self._handle,))

    def set_notification_position(self, position):
        """Sets the position where the overlay instance for the currently
        calling game should show notifications.

        This position is per-game and if this function is called from outside
        of a game context it will do nothing.

        :param int position: Position. See NotificationPosition.
        :return:
        """
        return self._call('SetOverlayNotificationPosition', (self._handle, position))

    def get_universe(self, as_str=False):
        """Returns universe the client is connected to. See Universe.

        :param bool as_str: Return human-friendly universe name instead of an ID.
        :return:
        """
        result = self._call('GetConnectedUniverse', (self._handle,))

        if as_str:
            return Universe.get_alias(result)

        return result

    @property
    def universe(self):
        """Universe the client is connected to.

        :rtype:
        :return:
        """
        return self.get_universe(as_str=True)

    @property
    def ipc_call_count(self):
        """The number of IPC calls made since the last time this function was called.
        Used for perf debugging so you can understand how many IPC calls your game makes per frame.
        Every IPC call is at minimum a thread context switch if not a process one
        so you want to rate control how often you do them.

        :rtype: int
        :return:
        """
        return self._call('GetIPCCallCount', (self._handle,))
