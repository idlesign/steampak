from .base import _ApiResourceBase


class Screenshots(_ApiResourceBase):
    """Exposes methods to manipulate overlay.

    Interface can be accessed through ``api.screenshots``:

    .. code-block:: python

        api.screenshots.take()

    """

    def __init__(self, *args, **kwargs):
        self._iface = self.get_client().screenshots
        super().__init__(*args, **kwargs)

    @property
    def is_hooked(self):
        """Checks if the app is hooking screenshots,
        or if the Steam Overlay is handling them.

        :rtype: bool
        """
        return self._iface.get_is_hooked()

    def toggle_hook(self, use=True):
        """Toggles whether the overlay handles screenshots when the user presses
        the screenshot hotkey, or if the game handles them.

        Hooking is disabled by default, and only ever enabled if you do so with this function.

        :param bool use:
        """
        self._iface.toggle_hook(use)

    def take(self):
        """Either causes the Steam Overlay to take a screenshot,
        or tells your screenshot manager that a screenshot needs to be taken.

        """
        self._iface.take()
