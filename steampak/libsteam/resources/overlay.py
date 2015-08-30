from .base import _ApiResourceBase


OVERLAY_PAGE_FRIENDS = 'Friends'
OVERLAY_PAGE_COMMUNITY = 'Community'
OVERLAY_PAGE_PLAYERS = 'Players'
OVERLAY_PAGE_SETTINGS = 'Settings'
OVERLAY_PAGE_GAME_GROUP = 'OfficialGameGroup'
OVERLAY_PAGE_STATS = 'Stats'
OVERLAY_PAGE_ACHIEVEMENTS = 'Achievements'


class Overlay(_ApiResourceBase):
    """Exposes methods to manipulate overlay.

    Overlay-related functions only work with OpenGL/D3D applications and only
    if Steam API is initialized before renderer device.

    Interface can be accessed through ``api.overlay``:

    .. code-block:: python

        api.overlay.activate()

    """
    _res_name = 'ISteamFriends'

    def activate(self, page=None):
        """Activates overlay with browser, optionally opened at a given page.

        :param str page: Overlay page alias (see OVERLAY_PAGE_*)
            or a custom URL.

        """
        page = page or ''

        if '://' in page:
            self._call('ActivateGameOverlayToWebPage', (self._ihandle(), page))
        else:
            self._call('ActivateGameOverlay', (self._ihandle(), page))
