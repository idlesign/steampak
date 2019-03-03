from .base import _ApiResourceBase, FriendFilter
from .user import User


class FriendTag(_ApiResourceBase):
    """Exposes methods to get friend tag data.

    Interface can be accessed through ``api.friends.tags()``:

    .. code-block:: python

        for tag in api.friends.tags():
            print(tag.name)

    """

    def __init__(self, tag_id, *args, **kwargs):
        self._iface = self.get_client().friends
        super().__init__(*args, **kwargs)
        self.tag_id = tag_id

    def __str__(self):
        return self.name

    @property
    def name(self):
        """Name of a friend tag, or None on error.

        :rtype: str
        """
        return self._iface.get_group_name(self.tag_id)

    def __len__(self):
        """Returns a number of members with friend tag.

        :rtype: int
        """
        return self._iface.get_group_members_count(self.tag_id)


class FriendTags(_ApiResourceBase):
    """Exposes methods to get friend tags data."""

    def __init__(self, *args, **kwargs):
        self._iface = self.get_client().friends
        super().__init__(*args, **kwargs)

    def __len__(self):
        """Returns a number of current user friend tags.

        :rtype: int
        """
        return self._iface.get_group_count()

    def __call__(self):
        """Generator. Returns FriendTag objects.

        :rtype: FriendTag
        """
        get_group = self._iface.get_group

        for idx in range(len(self)):
            yield FriendTag(get_group(idx))

    def __iter__(self):
        return iter(self())


class Friends(_ApiResourceBase):
    """Exposes methods to get friends related data.

    Interface can be accessed through ``api.friends()``:

    .. code-block:: python

        for user in api.friends():
            print(user.name)

    """

    tags: FriendTags = None
    """Interface to friend tags (categories).

    .. code-block:: python

        for tag in api.friends.tags():
            print(tag.name)

    """

    def __init__(self, *args, **kwargs):
        self._iface = self.get_client().friends
        super().__init__(*args, **kwargs)

        self.tags = FriendTags()

    def get_count(self, flt=FriendFilter.ALL):
        """Returns a number of current user friends, who meet a given criteria (filter).

        :param int flt: Filter value from FriendFilter. Filters can be combined with `|`.
            Defaults to ``FriendFilter.ALL``.

        :rtype: int
        """
        return self._iface.get_count(flt)

    def __len__(self):
        return self.get_count()

    def __call__(self, flt=FriendFilter.ALL):
        """Generator. Returns User objects.

        :param int flt: Filter value from FriendFilter. Filters can be combined with |.
        :rtype: User
        """
        get_by_index = self._iface.get_by_index

        for idx in range(self.get_count(flt)):
            user_id = get_by_index(idx, flt)
            yield User(user_id)

    def __iter__(self):
        return iter(self())
