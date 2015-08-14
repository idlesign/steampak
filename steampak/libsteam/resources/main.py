from os import path

from ..exceptions import SteamApiStartupError
from .base import _ApiResourceBase, API_THREAD_LOCAL, get_library
from .user import CurrentUser
from .friends import Friends
from .groups import Groups
from .utils import Utils
from .apps import Applications
from .stats import Stats


class Api(_ApiResourceBase):
    """Main entry point of Steam API."""

    player = CurrentUser()
    friends = Friends()
    groups = Groups()
    stats = Stats()
    utils = Utils()
    apps = Applications()

    _app_id = None

    def __init__(self, library_path, app_id=None):
        """
        :param str library_path: Full path to Steam library file.
            The library should be provided with your game.
            Library for various OS is distributed with Steam SDK available for Steam partners
            at https://partner.steamgames.com/

        :param str|int app_id: Application (game) identifier.
            Pass it as a parameter or place `steam_appid.txt` file with that ID in your game folder.

        :return:
        """
        get_library(library_path)
        self._app_id = app_id

        if self.is_steam_running():
            self.init(app_id)

    def init(self, app_id=None):
        """Initializes Steam API library.

        :param app_id:
        :return:
        """
        self.set_app_id(app_id)
        if not self._call('Init'):
            raise SteamApiStartupError(
                'Unable to initialize. Check Steam client is running '
                'and Steam application ID is defined in steam_appid.txt or passed to Api.')

    @property
    def app_id(self):
        """Application ID of the current process.

        :return:
        """
        return self.utils.app_id

    def is_steam_running(self):
        """Returns boolean whether a local Steam client is running

        :return:
        """
        return bool(self._call('IsSteamRunning'))

    def get_install_path(self):
        """Returns library installation path.

        :return:
        """
        return path.abspath(self._get_str('GetSteamInstallPath'))

    def start_app(self):
        """
        Detects if your executable was launched through the Steam client, and restarts your game through
        the client if necessary. The Steam client will be started if it is not running.

        Returns: true if your executable was NOT launched through the Steam client. This function will
                  then start your application through the client. Your current process should exit.

                 false if your executable was started through the Steam client or a steam_appid.txt file
                 is present in your game's directory (for development). Your current process should continue.

        NOTE: This function should be used only if you are using CEG or not using Steam's DRM. Once applied
              to your executable, Steam's DRM will handle restarting through Steam if necessary.

        :return:
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
        """Shutdowns API.

        :return:
        """
        self._call('Shutdown')
