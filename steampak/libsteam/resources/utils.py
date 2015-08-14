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
