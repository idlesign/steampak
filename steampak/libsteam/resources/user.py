from .base import _FriendsBase, FriendFilter
from libsteam.resources.base import _ApiResourceBase


class UserState(object):
    """User states enumeration."""

    OFFLINE = 0
    ONLINE = 1
    BUSY = 2
    AWAY = 3
    SNOOZE = 4
    READY_TO_TRADE = 5
    READY_TO_PLAY = 6

    STATES = {
        OFFLINE: 'offline',
        ONLINE: 'online',
        BUSY: 'busy',
        AWAY: 'away',
        SNOOZE: 'snooze',
        READY_TO_TRADE: 'trade',
        READY_TO_PLAY: 'play',
    }

    @classmethod
    def get_str(cls, state_id):
        return cls.STATES.get(state_id)


class User(_FriendsBase):
    """Exposes methods to get user-related data."""

    def __init__(self, user_id):
        self.user_id = user_id

    @property
    def name(self):
        """Returns user name (the same name as on the users community profile page).

        :return:
        """
        # GetPersonaName # todo local player
        return self._get_str('GetFriendPersonaName', [self._handle, self.user_id])

    @property
    def name_history(self):
        """A list of user names (as user can change those occasionally).

        :return:
        """
        history = []
        idx = 0
        while True:
            name = self._get_str('GetFriendPersonaNameHistory', [self._handle, self.user_id, idx])
            if not name:
                break
            idx += 1
            history.append(name)
        return history

    @property
    def nickname(self):
        """A nickname the current user has set for the user, or None if not set

        :return:
        """
        return self._get_str('GetPlayerNickname', [self._handle, self.user_id])

    def get_state(self, as_str=False):
        """Returns user state. See UserState.

        :param bool as_str: Return human-friendly state name instead of an ID.
        :return:
        """
        # GetPersonaState  # todo local player
        result = self._call('GetFriendPersonaState', [self._handle, self.user_id])

        if as_str:
            return UserState.get_str(result)

        return result

    @property
    def state(self):
        """User state. See .get_state().

        :rtype: str
        :return:
        """
        return self.get_state(as_str=True)

    @property
    def level(self):
        """User steam level.

        :rtype: int
        :return:
        """
        return self._call('GetFriendSteamLevel', [self._handle, self.user_id])

    def has_friends(self, flt=FriendFilter.ALL):
        """Indicated whether the user has friends, who meet the given criteria (filter).

        :param int flt: Filter value from FriendFilter. Filters can be combined with |.
        :rtype: bool
        :return:
        """
        return bool(self._call('HasFriend', [self._handle, self.user_id, flt]))


class CurrentUser(_ApiResourceBase):
    """Exposed methods related to a current Steam client user."""

    _res_name = 'ISteamUser'

    @property
    def user(self):
        """User object for current user.

        :rtype: User
        :return:
        """
        return User(self.steam_id())

    @property
    def is_logged_in(self):
        """Whether current user is logged in.

        :rtype: bool
        :return:
        """
        return self._get_bool('BLoggedOn', (self._handle,))

    @property
    def is_behind_nat(self):
        """Whether current user is behind NAT.

        :rtype: bool
        :return:
        """
        return self._get_bool('BIsBehindNAT', (self._handle,))

    @property
    def level(self):
        """Current user level.

        :rtype: int
        :return:
        """
        return self._call('GetPlayerSteamLevel', (self._handle,))

    @property
    def steam_id(self):
        return self._get_ptr('GetSteamID', (self._handle,))

    @property
    def steam_handle(self):
        return self._call('GetHSteamUser', (self._handle,))
