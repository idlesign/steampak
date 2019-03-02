from datetime import datetime

from .base import _ApiResourceBase, _EnumBase


if False:  # pragma: nocover
    from ._wrapper import Utils as IUtils


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
        MAX: 'unsupported',
    }


class NotificationPosition:

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

    def __init__(self, *args, **kwargs):
        self._iface = self.get_client().utils
        super().__init__(*args, **kwargs)

    notification_positions = NotificationPosition

    @property
    def seconds_app_active(self):
        """Number seconds application is active.

        :rtype: int
        """
        return self._iface.get_seconds_app_active()

    @property
    def seconds_computer_active(self):
        """Number seconds computer is active.

        :rtype: int
        """
        return self._iface.get_seconds_computer_active()

    @property
    def server_time(self):
        """Date and time on server.

        :rtype: datetime
        """
        return datetime.utcfromtimestamp(self._iface.get_server_time())

    @property
    def country_code(self):
        """2 digit ISO 3166-1-alpha-2 format country code this client is running in
        (as looked up via an IP-to-location database)

        E.g: RU.

        :rtype: str
        """
        return self._iface.get_country_code()

    @property
    def battery_power(self):
        """The amount of battery power left in the current system in % [0..100].
        255 for being on AC power.

        :rtype: int
        """
        return self._iface.get_battery_power()

    @property
    def app_id(self):
        """Application ID of the current process.

        :rtype: int
        """
        return self._iface.get_app_id()

    def set_notification_position(self, position):
        """Sets the position where the overlay instance for the currently
        calling game should show notifications.

        This position is per-game and if this function is called from outside
        of a game context it will do nothing.

        :param int position: Position. See ``NotificationPosition``.
        """
        self._iface.set_notify_position(position)

    @property
    def overlay_enabled(self):
        """``True`` if the overlay is running & the user can access it.

        The overlay process could take a few seconds to start & hook the game process,
        so this function will initially return ``False`` while the overlay is loading.

        :rtype: bool
        """
        return self._iface.get_overlay_enabled()

    @property
    def vr_mode(self):
        """``True``  if Steam itself is running in VR mode.

        :rtype: bool
        """
        return self._iface.get_vr_mode()

    def get_universe(self, as_str=False):
        """Returns universe the client is connected to. See ``Universe``.

        :param bool as_str: Return human-friendly universe name instead of an ID.
        :rtype: int|str
        """
        result = self._iface.get_connected_universe()

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
        return self._iface.get_ipc_call_count()

    @property
    def ui_language(self):
        """The language the steam client is running in.

        E.g.: russian

        :rtype: str
        """
        return self._iface.get_ui_language()
