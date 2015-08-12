from .base import _FriendsBase, FriendFilter
from .user import User


class FriendTag(_FriendsBase):
    """Exposes methods to get friend tag data."""

    def __init__(self, tag_id):
        self.tag_id = tag_id

    @property
    def name(self):
        """Name of a friend tag, or None on error.

        :return:
        """
        return self._get_str('GetFriendsGroupName', (self._handle, self.tag_id))

    def __len__(self):
        """Returns a number of members with friend tag.

        :rtype: int
        :return:
        """
        return self._call('GetFriendsGroupMembersCount', (self._handle, self.tag_id))


class FriendTags(_FriendsBase):
    """Exposes methods to get friend tags data."""

    def __len__(self):
        """Returns a number of current user friend tags.

        :rtype: int
        :return:
        """
        return self._call('GetFriendsGroupCount', (self._handle,))

    def __call__(self):
        """Generator. Returns FriendTag objects.

        :rtype: FriendTag
        :return:
        """
        for idx in range(len(self)):
            tag_id = self._call('GetFriendsGroupIDByIndex', (self._handle, idx))
            yield FriendTag(tag_id)


class Friends(_FriendsBase):
    """Exposes methods to get friends related data."""

    # Friends tags (categories).
    tags = FriendTags()

    def get_count(self, flt=FriendFilter.ALL):
        """Returns a number of current user friends, who meet a given criteria (filter).

        :rtype: int
        :return:
        """
        return self._call('GetFriendCount', (self._handle, flt))

    def __len__(self):
        return self.get_count()

    def __call__(self, flt=FriendFilter.ALL):
        """Generator. Returns User objects.

        :param int flt: Filter value from FriendFilter. Filters can be combined with |.
        :rtype: User
        :return:
        """
        for idx in range(self.get_count(flt)):
            user_id = self._get_ptr('GetFriendByIndex', (self._handle, idx, flt))
            yield User(user_id)
