from .base import _ApiResourceBase


class Overlay(_ApiResourceBase):
    """Exposes methods to manipulate overlay.

    Overlay-related functions only work with OpenGL/D3D applications and only
    if Steam API is initialized before renderer device.

    Interface can be accessed through ``api.overlay``:

    .. code-block:: python

        api.overlay.activate()

    """

    PAGE_FRIENDS = 'Friends'
    PAGE_COMMUNITY = 'Community'
    PAGE_PLAYERS = 'Players'
    PAGE_SETTINGS = 'Settings'
    PAGE_GAME_GROUP = 'OfficialGameGroup'
    PAGE_STATS = 'Stats'
    PAGE_ACHIEVEMENTS = 'Achievements'

    def __init__(self, *args, **kwargs):
        self._iface = self.get_client().friends
        super().__init__(*args, **kwargs)

    def activate(self, page=None):
        """Activates overlay with browser, optionally opened at a given page.

        :param str page: Overlay page alias (see OVERLAY_PAGE_*)
            or a custom URL.

        """
        page = page or ''

        if '://' in page:
            self._iface.activate_overlay_url(page)

        else:
            self._iface.activate_overlay_game(page)
