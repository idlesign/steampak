import ctypes
from datetime import datetime

from .base import _ApiResourceBase, ResultArg


class _StatsBase(_ApiResourceBase):
    """Base class to consolidate functions under ISteamUserStats."""

    _res_name = 'ISteamUserStats'


class Achievement(_StatsBase):
    """Exposes methods to get achievement data."""

    def __init__(self, name):
        self._name = name
        self.name = self._str_decode(name)

    def _get_attr(self, attr_name):
        return self._get_str('GetAchievementDisplayAttribute', (self._ihandle(), self._name, attr_name))

    @property
    def title(self):
        """Achievement title.

        :rtype: str
        :return:
        """
        return self._get_attr('name')

    @property
    def description(self):
        """Achievement description.

        :rtype: str
        :return:
        """
        return self._get_attr('desc')

    def get_global_unlock_percent(self):
        result, percent = self._call(
            'GetAchievementAchievedPercent', [self._ihandle(), self._name, ResultArg(ctypes.c_float)])
        return percent

    @property
    def hidden(self):
        """True if achievement is hidden.

        :rtype: bool
        :return:
        """
        return self._get_attr('hidden') == '1'

    @property
    def unlocked(self):
        """True if achievement is unlocked.

        :rtype: bool
        :return:
        """
        result, unlocked = self._call(
            'GetAchievement', [self._ihandle(), self._name, ResultArg(ctypes.c_bool)])
        return unlocked

    def unlock(self):
        """Unlocks the achievement.

        :rtype: bool
        :return:
        """
        return self._get_bool('SetAchievement', (self._ihandle(), self._name))

    def clear(self):
        """Clears (locks) the achievement.

        :rtype: bool
        :return:
        """
        return self._get_bool('ClearAchievement', (self._ihandle(), self._name))

    def get_unlock_info(self):
        """Returns tuple of unlock data: (is_unlocked, unlocked_datetime).

        NOTE: unlocked_datetime wil be None if achievement if unlocked before 01.12.2009.

        :rtype: tuple[bool, datetime]
        :return:
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


class Achievements(_StatsBase):
    """Exposes methods to get to achievements."""

    def __len__(self):
        """Returns a number of current game achievements..

        :rtype: int
        :return:
        """
        return self._call('GetNumAchievements', (self._ihandle(),))

    def __call__(self):
        """Generator. Returns (name, Achievement) tuples.

        :rtype: tuple[str, Achievement]
        :return:
        """
        for idx in range(len(self)):
            name = self._get_str('GetAchievementName', (self._ihandle(), idx), decode=False)
            yield self._str_decode(name), Achievement(name)


class Stats(_StatsBase):
    """Exposes various statistics for current game."""

    # Current game achievements.
    achievements = Achievements()
