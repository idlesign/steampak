from datetime import datetime

from ctyped.types import CRef
from .base import _ApiResourceBase


class Achievement(_ApiResourceBase):
    """Exposes methods to get achievement data.

    Aliased as ``steampak.SteamAchievement``.

    .. code-block:: python

        from steampak import SteamAchievement

        print(SteamAchievement('some_achievement_name').title)


    Instances can be accessed through ``api.apps.current.achievements``:

    .. code-block:: python

        for ach_name, ach in api.apps.current.achievements:
            print('%s (%s)' % (ach.title, ach_name))

    """

    def __init__(self, name, *args, **kwargs):
        self._iface = self.get_client().user_stats
        super().__init__(*args, **kwargs)
        self.name = name

    def __str__(self):
        return self.name

    def _get_attr(self, attr_name):
        return self._iface.get_ach_attrib(self.name, attr_name)

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
        percent = CRef.cfloat()
        result = self._iface.get_ach_progress(self.name, percent)

        if not result:
            return 0.0

        return float(percent)

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
        achieved = CRef.cbool()
        result = self._iface.get_ach(self.name, achieved)

        if not result:
            return False

        return bool(achieved)

    def unlock(self, store=True):
        """Unlocks the achievement.


        :param bool store: Whether to send data to server immediately (as to get overlay notification).
        :rtype: bool

        """
        result = self._iface.ach_unlock(self.name)
        result and store and self._store()
        return result

    def clear(self, store=True):
        """Clears (locks) the achievement.

        :rtype: bool
        """
        result = self._iface.ach_lock(self.name)
        result and store and self._store()
        return result

    def _store(self):
        """Stores the current achievement data on the server.

        The same as `api.apps.current.achievements.store_stats()`.

        Will get a callback when set and one callback for every new achievement.

        :rtype: bool
        """
        return self._iface.store_stats()

    def get_unlock_info(self):
        """Returns tuple of unlock data: (is_unlocked, unlocked_datetime).

        .. note::

            `unlocked_datetime` will be ``None`` if achievement if unlocked before 2009-12-01.

        :rtype: tuple[bool, datetime]
        """
        unlocked = CRef.cbool()
        unlocked_at = CRef.cint()

        result = self._iface.get_ach_unlock_info(self.name, unlocked, unlocked_at)

        if not result:
            return None, None

        unlocked = bool(unlocked)
        unlocked_at = int(unlocked_at)

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

    def __init__(self, *args, **kwargs):
        self._iface = self.get_client().user_stats
        super().__init__(*args, **kwargs)

    def store_stats(self):
        """Stores the current data on the server.

        Will get a callback when set and one callback for every new achievement.

        :rtype: bool
        """
        return self._iface.store_stats()

    def __len__(self):
        """Returns a number of current game achievements..

        :rtype: int
        """
        return self._iface.get_ach_count()

    def __call__(self):
        """Generator. Returns (name, Achievement) tuples.

        :rtype: tuple(str, Achievement)
        """
        for idx in range(len(self)):
            name = self._iface.get_ach_name(idx)
            yield name, Achievement(name)

    def __iter__(self):
        return iter(self())
