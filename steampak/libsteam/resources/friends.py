from .base import _ApiResourceBase, FriendFilter
from .user import User


class FriendTag(_ApiResourceBase):
    """Exposes methods to get friend tag data.

    Interface can be accessed through ``api.friends.tags()``:

    .. code-block:: python

        for tag in api.friends.tags():
            print(tag.name)

    """

    _res_name = 'ISteamFriends'

    def __init__(self, tag_id):
        self.tag_id = tag_id

    @property
    def name(self):
        """Name of a friend tag, or None on error.

        :rtype: str
        """
        return self._get_str('GetFriendsGroupName', (self._ihandle(), self.tag_id))

    def __len__(self):
        """Returns a number of members with friend tag.

        :rtype: int
        :return:
        """
        return self._call('GetFriendsGroupMembersCount', (self._ihandle(), self.tag_id))


class FriendTags(_ApiResourceBase):
    """Exposes methods to get friend tags data."""

    _res_name = 'ISteamFriends'

    def __len__(self):
        """Returns a number of current user friend tags.

        :rtype: int
        :return:
        """
        return self._call('GetFriendsGroupCount', (self._ihandle(),))

    def __call__(self):
        """Generator. Returns FriendTag objects.

        :rtype: FriendTag
        :return:
        """
        for idx in range(len(self)):
            tag_id = self._call('GetFriendsGroupIDByIndex', (self._ihandle(), idx))
            yield FriendTag(tag_id)


class Friends(_ApiResourceBase):
    """Exposes methods to get friends related data.

    Interface can be accessed through ``api.friends()``:

    .. code-block:: python

        for user in api.friends():
            print(user.name)

    """
    _res_name = 'ISteamFriends'

    tags = FriendTags()
    """Interface to friend tags (categories).

    .. code-block:: python

        for tag in api.friends.tags():
            print(tag.name)

    """

    def get_count(self, flt=FriendFilter.ALL):
        """Returns a number of current user friends, who meet a given criteria (filter).

        :param int flt: Filter value from FriendFilter. Filters can be combined with `|`.
            Defaults to ``FriendFilter.ALL``.

        :rtype: int
        """
        return self._call('GetFriendCount', (self._ihandle(), flt))

    def __len__(self):
        return self.get_count()

    def __call__(self, flt=FriendFilter.ALL):
        """Generator. Returns User objects.

        :param int flt: Filter value from FriendFilter. Filters can be combined with |.
        :rtype: User
        """
        for idx in range(self.get_count(flt)):
            user_id = self._get_ptr('GetFriendByIndex', (self._ihandle(), idx, flt))
            yield User(user_id)
