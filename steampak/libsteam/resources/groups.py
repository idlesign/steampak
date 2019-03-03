from ctyped.types import CRef

from .base import _ApiResourceBase


class Group(_ApiResourceBase):
    """Exposes methods to get user groups (clans) data.

    Instances can be accessed through ``api.groups()``:

    .. code-block:: python

        for group in api.groups():
            print(group.name)

    """

    def __init__(self, group_id, *args, **kwargs):
        self._iface = self.get_client().friends
        super().__init__(*args, **kwargs)
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
        stats_online = CRef.cint()
        stats_ingame = CRef.cint()
        stats_chatting = CRef.cint()

        self._iface.get_clan_stats(
            self.group_id,
            stats_online,
            stats_ingame,
            stats_chatting,
        )

        return {
            'online': int(stats_online),
            'ingame': int(stats_ingame),
            'chatting': int(stats_chatting),
        }

    @property
    def name(self):
        """Name of a group.

        :rtype: str
        """
        return self._iface.get_clan_name(self.group_id)

    @property
    def alias(self):
        """Alias (short name) of a group.

        :rtype: str
        """
        return self._iface.get_clan_alias(self.group_id)

    def show_page(self):
        """Shows overlay with group page."""
        self._iface.activate_overlay('steamid', self.group_id)

    def open_chat(self):
        """Shows overlay with group chat window."""
        self._iface.activate_overlay('chat', self.group_id)


class Groups(_ApiResourceBase):
    """Exposes methods to get user groups data. Groups are also known as clans.

    Interface can be accessed through ``api.groups()``:

    .. code-block:: python

        for group in api.groups():
            print(group.name)

    """

    def __init__(self, *args, **kwargs):
        self._iface = self.get_client().friends
        super().__init__(*args, **kwargs)

    def __len__(self):
        """Returns a number of current user groups (clans).

        :rtype: int
        """
        return self._iface.get_clan_count()

    def __call__(self):
        """Generator. Returns Group objects.

        :rtype: Group
        """
        get_clan = self._iface.get_clan

        for idx in range(len(self)):
            yield Group(get_clan(idx))

    def __iter__(self):
        return iter(self())
