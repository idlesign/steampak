from os import path, environ

from ..exceptions import SteamApiStartupError
from .base import _ApiResourceBase, get_library
from .user import CurrentUser
from .friends import Friends
from .groups import Groups
from .utils import Utils
from .apps import Applications
from .overlay import Overlay


class Api(_ApiResourceBase):
    """Main entry point of Steam API.

    It is aliased as ``steampak.SteamApi``.

    .. code-block:: python

        from steampak import SteamApi

        # Automatically initialize Steam API library if Steam client is running.
        api = SteamApi(LIBRARY_PATH, app_id=APP_ID)

        # Do not forget to shutdown when done:
        api.shutdown()

    """

    current_user = CurrentUser()
    """Interface to current user.

    .. code-block:: python

        print(api.current_user.name)

    """

    friends = Friends()
    """Interface to friends of current user.

    .. code-block:: python

        for user in api.friends():
            print(user.name)

    """

    groups = Groups()
    """Interface to user groups.

    .. code-block:: python

        for group in api.groups():
            print(group.name)

    """

    utils = Utils()
    """Interface to various utilities.

    .. code-block:: python

        print(api.utils.ui_language)

    """

    apps = Applications()
    """Interface to applications (games).

    .. code-block:: python

        for app_id, app in api.apps.installed():
            print('%s: %s' % (app_id, app.name))

    """

    overlay = Overlay()
    """Interface to Steam overlay.

    Overlay-related functions only work with OpenGL/D3D applications and only
    if Steam API is initialized before renderer device.

    .. code-block:: python

        api.overlay.activate()

    """

    _app_id = None

    def __init__(self, library_path, app_id=None):
        """
        :param str library_path: Full path to Steam library file.
            The library should be provided with your game.
            Library for various OS is distributed with Steam SDK available for Steam partners
            at https://partner.steamgames.com/

        :param str|int app_id: Application (game) identifier.
            Pass it as a parameter or put `steam_appid.txt` file with that ID in your game folder.
        """
        get_library(library_path)
        self._app_id = app_id

        if self.steam_running:
            self.init(app_id)

    def init(self, app_id=None):
        """Initializes Steam API library.

        :param str|int app_id: Application ID.
        :raises: SteamApiStartupError
        """
        self.set_app_id(app_id)
        if not self._call('Init'):
            raise SteamApiStartupError(
                'Unable to initialize. Check Steam client is running '
                'and Steam application ID is defined in steam_appid.txt or passed to Api.')

    @classmethod
    def set_app_id(cls, app_id):
        """Sets current application ID into environment.

        :param str|int app_id: Your application ID.
        """
        if app_id:
            environ['SteamAppId'] = str(app_id)  # SteamGameId

    @property
    def app_id(self):
        """Application ID of the current process."""
        return self.utils.app_id

    @property
    def steam_running(self):
        """``True`` if a local Steam client is running

        :rtype: bool
        """
        return bool(self._call('IsSteamRunning'))

    @property
    def install_path(self):
        """Returns library installation path.

        :rtype: str
        """
        return path.abspath(self._get_str('GetSteamInstallPath'))

    def start_app(self):
        """
        Detects if your executable was launched through the Steam client, and restarts your game through
        the client if necessary. The Steam client will be started if it is not running.

        SDK Note: This function should be used only if you are using CEG or not using Steam's DRM. Once applied
        to your executable, Steam's DRM will handle restarting through Steam if necessary.

        :rtype: bool
        :return: True if your executable was NOT launched through the Steam client. This function will
                then start your application through the client. Your current process should exit.

                False if your executable was started through the Steam client or a steam_appid.txt file
                is present in your game's directory (for development). Your current process should continue.
        """
        args = None
        if self._app_id is not None:
            args = (self._app_id,)
        return bool(self._call('RestartAppIfNecessary', args))

    def run_callbacks(self):
        # Heavy duty method. Call library function as directly as possible.
        get_library().SteamAPI_RunCallbacks()

    def register_callback(self, callback, i_callback):
        self._call('RegisterCallback', (callback, i_callback))

    def unregister_callback(self, callback):
        self._call('RegisterCallback', (callback,))

    def register_call_result(self, callback, result):
        self._call('RegisterCallResult', (callback, result))

    def unregister_call_result(self, callback, result):
        self._call('UnregisterCallResult', (callback, result))

    def shutdown(self):
        """Shutdowns API."""
        self._call('Shutdown')
