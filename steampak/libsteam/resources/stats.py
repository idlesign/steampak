import ctypes
from datetime import datetime

from .base import _ApiResourceBase, ResultArg


class Achievement(_ApiResourceBase):
    """Exposes methods to get achievement data.

    Aliased as ``steampak.SteamAchievement``.

    .. code-block:: python

        from steampak import SteamAchievement

        print(SteamAchievement('some_achievement_name').title)


    Instances can be accessed through ``api.apps.current.achievements()``:

    .. code-block:: python

        for ach_name, ach in api.apps.current.achievements():
            print('%s (%s)' % (ach.title, ach_name))

    """

    _res_name = 'ISteamUserStats'

    def __init__(self, name):
        self._name = name
        self.name = self._str_decode(name)

    def _get_attr(self, attr_name):
        return self._get_str('GetAchievementDisplayAttribute', (self._ihandle(), self._name, attr_name))

    @property
    def title(self):
        """Achievement title.

        :rtype: str
        """
        return self._get_attr('name')

    @property
    def description(self):
        """Achievement description.

        :rtype: str
        """
        return self._get_attr('desc')

    @property
    def global_unlock_percent(self):
        """Global achievement unlock percent.

        :rtype: float
        """
        result, percent = self._call(
            'GetAchievementAchievedPercent', [self._ihandle(), self._name, ResultArg(ctypes.c_float)])
        return percent

    @property
    def hidden(self):
        """``True`` if achievement is hidden.

        :rtype: bool
        """
        return self._get_attr('hidden') == '1'

    @property
    def unlocked(self):
        """``True`` if achievement is unlocked.

        :rtype: bool
        """
        result, unlocked = self._call(
            'GetAchievement', [self._ihandle(), self._name, ResultArg(ctypes.c_bool)])
        return unlocked

    def unlock(self, store=True):
        """Unlocks the achievement.


        :param bool store: Whether to send data to server immediately (as to get overlay notification).
        :rtype: bool

        """
        result = self._get_bool('SetAchievement', (self._ihandle(), self._name))
        result and store and self._store()
        return result

    def clear(self, store=True):
        """Clears (locks) the achievement.

        :rtype: bool
        """
        result = self._get_bool('ClearAchievement', (self._ihandle(), self._name))
        result and store and self._store()
        return result

    def _store(self):
        """Stores the current achievement data on the server.

        The same as `api.apps.current.achievements.store_stats()`.

        Will get a callback when set and one callback for every new achievement.

        :rtype: bool
        """
        return self._call('StoreStats', (self._ihandle(),))

    def get_unlock_info(self):
        """Returns tuple of unlock data: (is_unlocked, unlocked_datetime).

        .. note::

            `unlocked_datetime` will be ``None`` if achievement if unlocked before 2009-12-01.

        :rtype: tuple[bool, datetime]
        """
        result, unlocked, unlocked_at = self._call(
            'GetAchievementAndUnlockTime',
            [self._ihandle(), self._name, ResultArg(ctypes.c_bool), ResultArg(ctypes.c_int)])

        if unlocked:
            if unlocked_at:
                unlocked_at = datetime.utcfromtimestamp(unlocked_at)
            else:
                unlocked_at = None
        else:
            unlocked_at = None

        return unlocked, unlocked_at


class CurrentApplicationAchievements(_ApiResourceBase):
    """Exposes methods to get to achievements."""

    _res_name = 'ISteamUserStats'

    def store_stats(self):
        """Stores the current data on the server.

        Will get a callback when set and one callback for every new achievement.

        :rtype: bool
        """
        return self._call('StoreStats', (self._ihandle(),))

    def __len__(self):
        """Returns a number of current game achievements..

        :rtype: int
        :return:
        """
        return self._call('GetNumAchievements', (self._ihandle(),))

    def __call__(self):
        """Generator. Returns (name, Achievement) tuples.

        :rtype: tuple(str, Achievement)
        :return:
        """
        for idx in range(len(self)):
            name = self._get_str('GetAchievementName', (self._ihandle(), idx), decode=False)
            yield self._str_decode(name), Achievement(name)
