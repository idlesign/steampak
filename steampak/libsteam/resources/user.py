from .base import FriendFilter, _ApiResourceBase, _EnumBase


class UserState(_EnumBase):
    """User states enumeration."""

    OFFLINE = 0
    ONLINE = 1
    BUSY = 2
    AWAY = 3
    SNOOZE = 4
    READY_TO_TRADE = 5
    READY_TO_PLAY = 6
    MAX = 7

    aliases = {
        OFFLINE: 'offline',
        ONLINE: 'online',
        BUSY: 'busy',
        AWAY: 'away',
        SNOOZE: 'snooze',
        READY_TO_TRADE: 'trade',
        READY_TO_PLAY: 'play',
        MAX: 'unsupported',
    }


class User(_ApiResourceBase):
    """Exposes methods to get user-related data.

    Instance access example:

    .. code-block:: python

        for user in api.friends():
            print(user.name)

    """

    def __init__(self, user_id, *args, **kwargs):
        client = self.get_client()
        self._iface = client.friends
        self._iface_user = client.user

        super().__init__(*args, **kwargs)
        self.user_id = user_id

    def __str__(self):
        return '%s [%s]' % (self.user_id, self.name)

    @property
    def name(self):
        """User name (the same name as on the users community profile page).

        :rtype: str
        """
        uid = self.user_id

        if self._iface_user.get_id() == uid:
            return self._iface.get_my_name()

        return self._iface.get_name(uid)

    @property
    def name_history(self):
        """A list of user names (as user can change those occasionally).

        :rtype: list
        """
        history = []
        idx = 0

        get_history = self._iface.get_name_history
        uid = self.user_id

        while True:
            name = get_history(uid, idx)

            if not name:
                break

            idx += 1
            history.append(name)

        return history

    @property
    def nickname(self):
        """A nickname the current user has set for the user, or ``None`` if not set.

        :rtype: str
        """
        return self._iface.get_nickname(self.user_id)

    def get_state(self, as_str=False):
        """Returns user state. See ``UserState``.

        :param bool as_str: Return human-friendly state name instead of an ID.
        :rtype: int|str
        """

        uid = self.user_id

        if self._iface_user.get_id() == uid:
            result = self._iface.get_my_state()

        else:
            result = self._iface.get_state(uid)

        if as_str:
            return UserState.get_alias(result)

        return result

    @property
    def state(self):
        """User state. See .get_state().

        :rtype: str
        """
        return self.get_state(as_str=True)

    @property
    def level(self):
        """User level (as shown on profile).

        :rtype: int
        """
        return self._iface.get_level(self.user_id)

    def has_friends(self, flt=FriendFilter.ALL):
        """Indicated whether the user has friends, who meet the given criteria (filter).

        :param int flt: Filter value from FriendFilter. Filters can be combined with `|`.
        :rtype: bool
        """
        return self._iface.get_has_friend(self.user_id, flt)

    def show_profile(self):
        """Shows overlay with user profile."""
        self._iface.activate_overlay('steamid', self.user_id)

    def show_stats(self):
        """Shows overlay with user stats."""
        self._iface.activate_overlay('stats', self.user_id)

    def show_achievements(self):
        """Shows overlay with user achievements."""
        self._iface.activate_overlay('achievements', self.user_id)

    def add_to_friends(self):
        """Shows a dialog to add user as a friend."""
        self._iface.activate_overlay('friendadd', self.user_id)

    def remove_from_friends(self):
        """Shows a dialog to remove user from friends."""
        self._iface.activate_overlay('friendremove', self.user_id)

    def accept_friend_invite(self):
        """Shows a dialog to accept an incoming friend invite."""
        self._iface.activate_overlay('friendrequestaccept', self.user_id)

    def ignore_friend_invite(self):
        """Shows a dialog to ignore an incoming friend invite."""
        self._iface.activate_overlay('friendrequestignore', self.user_id)

    def open_chat(self):
        """Shows overlay with chat window."""
        self._iface.activate_overlay('chat', self.user_id)

    def open_trade(self):
        """Shows overlay with Steam Trading session that was started
        with the ISteamEconomy/StartTrade Web API.

        """
        self._iface.activate_overlay('jointrade', self.user_id)


class CurrentUser(_ApiResourceBase):
    """Exposed methods related to a current Steam client user.

    Can be accessed through ``api.current_user``:

    .. code-block:: python

        user = api.current_user

    """

    def __init__(self, *args, **kwargs):
        self._iface = self.get_client().user
        super().__init__(*args, **kwargs)

    def __str__(self):
        return str(self.steam_id)

    @property
    def user(self):
        # User object for current user.
        return User(self.steam_id)

    @property
    def logged_in(self):
        """``True`` if the Steam client current has a live connection to the Steam servers.

        If ``False``, it means there is no active connection due to either a networking issue
        on the local machine, or the Steam server is down/busy.

        The Steam client will automatically be trying to recreate the connection as often as possible.

        :rtype: bool
        """
        return self._iface.get_is_logged_on()

    @property
    def behind_nat(self):
        """``True`` if this users looks like they are behind a NAT device.
        Only valid once the user has connected to steam (i.e a SteamServersConnected_t has been issued)
        and may not catch all forms of NAT.

        :rtype: bool
        """
        return self._iface.get_is_behind_nat()

    @property
    def level(self):
        """Current user level (as shown on their profile).

        :rtype: int
        """
        return self._iface.get_level()

    @property
    def steam_id(self):
        # Returns the CSteamID of the account currently logged into the Steam client.
        # A CSteamID is a unique identifier for an account, and used to differentiate users
        # in all parts of the Steamworks API
        return self._iface.get_id()

    @property
    def steam_handle(self):
        # Returns the HSteamUser this interface represents.
        # This is only used internally by the API, and by a few select interfaces
        # that support multi-user.
        return self.get_client().h_user
