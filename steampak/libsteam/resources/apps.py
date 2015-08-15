import ctypes
from datetime import datetime

from .base import _ApiResourceBase, ResultArg
from .user import User
from .stats import CurrentApplicationAchievements


MAX_TITLE_LEN = 300
MAX_DIRECTORY_LEN = 500


class Application(_ApiResourceBase):
    """Exposes methods to get application data.

    Aliased as ``steampak.SteamApplication``.

    .. code-block:: python

        from steampak import SteamApplication

        # We use `Spacewar` app ID. (This game is provided with SDK).
        my_app = SteamApplication(480)

    """

    _res_name = 'ISteamApps'

    def __init__(self, app_id):
        """
        :param int|None app_id: Application (game) ID.
        """
        if app_id is not None:  # Might be None for current app.
            self.app_id = app_id

    @property
    def owned(self):
        """``True`` if user owns the current app.

        .. warning::

            Only use this member if you need to check ownership of a game related to yours, a demo for example.

        :rtype: bool
        """
        return self._get_bool('BIsSubscribedApp', (self._ihandle(), self.app_id))

    @property
    def installed(self):
        """``True`` if app is installed (not necessarily owned).

        :rtype: bool
        """
        return self._get_bool('BIsAppInstalled', (self._ihandle(), self.app_id))

    @property
    def name(self):
        """Application name, or None on error.

        .. warning::

            Restricted interface can only be used by approved apps.

        :rtype: str
        """
        max_len = MAX_TITLE_LEN
        result, name = self._call(
            'SteamAPI_ISteamAppList_GetAppName',
            [self._ihandle('SteamAppList'), self.app_id, ResultArg(ctypes.c_char * max_len), max_len], direct=True)

        if result == -1:
            return None

        return self._str_decode(name)

    @property
    def install_dir(self):
        """Returns application installation path.

        .. note::

            If fails this falls back to a restricted interface, which can only be used by approved apps.

        :rtype: str
        """
        max_len = MAX_DIRECTORY_LEN
        res_arg = ResultArg(ctypes.c_char * max_len)
        _, directory = self._call('GetAppInstallDir', [self._ihandle(), self.app_id, res_arg, max_len])

        if not directory:
            # Fallback to restricted interface (can only be used by approved apps).
            result, directory = self._call(
                'SteamAPI_ISteamAppList_GetAppInstallDir',
                [self._ihandle('SteamAppList'), self.app_id, res_arg, max_len], direct=True)

            if result == -1:
                return None

        return self._str_decode(directory)

    @property
    def purchase_time(self):
        """Date and time of app purchase.

        :rtype: datetime
        """
        # todo works?
        ts = self._call('GetEarliestPurchaseUnixTime', (self._ihandle(),))
        if not ts:
            return None
        return datetime.utcfromtimestamp(ts)

    @property
    def build_id(self):
        """Application Build ID.
        This may change at any time based on backend updates.

        .. warning::

            Restricted interface can only be used by approved apps.

        :rtype: int
        """
        return self._call(
            'SteamAPI_ISteamAppList_GetAppBuildId', (self._ihandle('SteamAppList'), self.app_id), direct=True)


class InstalledApplications(_ApiResourceBase):
    """Exposes methods to get data on installed applications.

    Interface can be accessed through ``api.apps.installed``.

    .. warning::

        Restricted interface can only be used by approved apps.

    """
    _res_name = 'ISteamAppList'

    def __len__(self):
        """Returns a number of currently installed applications.

        :rtype: int
        :return:
        """
        return self._call('GetNumInstalledApps', (self._ihandle(),))

    def __call__(self):
        """Generator. Returns Application objects, representing currently installed applications.

        :rtype: tuple(int, Application)
        :return:
        """
        max_count = len(self)
        _, apps_id = self._call(
            'GetInstalledApps', [self._ihandle(), ResultArg(ctypes.c_uint32 * max_count), max_count])

        for app_id in apps_id:
            yield app_id, Application(app_id)


class Dlc(Application):
    """Exposes methods to get downloadable content (DLC) data.

    Aliased as ``steampak.SteamDlc``.

    .. code-block:: python

        from steampak import SeamDlc

        # We use `Spacewar` DLC app ID. (Spacewar game is provided with SDK).
        my_dlc = SeamDlc(110902)


    Current application DLCs are available through ``CurrentApplication.dlcs``.

    """

    def __init__(self, app_id):
        super(Dlc, self).__init__(app_id)
        self._name = None
        self._available = None

    @property
    def installed(self):
        """``True`` if the user owns the DLC & if the DLC is installed.

        :rtype: bool
        """
        return self._get_bool('BIsDlcInstalled', (self._ihandle(), self.app_id))

    def install(self):
        """Installs DLC (for optional DLCs)."""
        self._call('InstallDLC', (self._ihandle(), self.app_id))

    def uninstall(self):
        """Uninstalls DLC (for optional DLCs)."""
        self._call('UninstallDLC', (self._ihandle(), self.app_id))

    def get_download_progress(self):
        """Returns tuple with download progress (for optional DLCs):

            (bytes_downloaded, bytes_total)

        :rtype: tuple
        """
        _, current, total = self._call(
            'GetDlcDownloadProgress',
            [self._ihandle(), self.app_id, ResultArg(ctypes.c_uint64), ResultArg(ctypes.c_uint64)])

        return current, total

    @property
    def name(self):
        """DLC name.

        :rtype: str
        """
        # Fallback to parent data if necessary.
        return self._name or super(Dlc, self).name

    @property
    def available(self):
        """True if DLC is available.

        :rtype: bool
        """
        return self._available


class CurrentApplicationDlcs(_ApiResourceBase):
    """Exposes methods to get downloadable content (DLC) data
    for current application.

    """
    _res_name = 'ISteamApps'

    def __len__(self):
        """Returns a number of current application .

        :rtype: int
        :return:
        """
        return self._call('GetDLCCount', (self._ihandle(),))

    def __call__(self):
        """Generator. Returns Dlc objects.

        :rtype: tuple(int, Dlc)
        :return:
        """
        max_len = MAX_TITLE_LEN
        for idx in range(len(self)):
            result, app_id, available, name = self._call(
                'BGetDLCDataByIndex', [
                    self._ihandle(), idx,
                    ResultArg(ctypes.c_int), ResultArg(ctypes.c_bool), ResultArg(ctypes.c_char * max_len), max_len])

            dlc = Dlc(app_id)
            # Populate data.
            dlc._name = name
            dlc._available = available

            yield app_id, dlc


class CurrentApplication(Application):
    """Exposes methods to get current application data.

    Interface can be accessed through ``api.apps.current``.

    .. code-block:: python

        from steampak import SteamApi

        api = SteamApi(LIBRARY_PATH, app_id=APP_ID)

        print(api.apps.current.language_current)

    """

    dlcs = CurrentApplicationDlcs()
    """Interface to DLCs of current application.

    .. code-block:: python

        for dlc_id, dlc in api.apps.current.dlcs():
            print('%s: %s' % (dlc_id, dlc.name))

    """

    achievements = CurrentApplicationAchievements()
    """Current application (game) achievements.

    .. code-block:: python

        for ach_name, ach in api.apps.current.achievements():
            print('%s: %s' % (ach_name, ach.title))

    """


    def __init__(self):
        super(CurrentApplication, self).__init__(None)

    @property
    def app_id(self):
        # Overrode to support parent class methods.
        return self._call('SteamAPI_ISteamUtils_GetAppID', (self._ihandle('SteamUtils'),), direct=True)

    @property
    def beta_name(self):
        """Current beta branch name, 'public' is the default branch.

        :rtype: str
        """
        # todo works?
        max_len = MAX_TITLE_LEN
        _, name = self._call('GetCurrentBetaName', [self._ihandle(), ResultArg(ctypes.c_char * max_len), max_len])
        return self._str_decode(name)

    @property
    def build_id(self):
        """Current application Build ID.
        This may change at any time based on backend updates.

        .. warning::

            Restricted interface can only be used by approved apps.

        :rtype: int
        """
        return self._call('GetAppBuildId', (self._ihandle(),))

    @property
    def language_current(self):
        """Current game language.

        E.g.: english

        :rtype: str
        """
        return self._get_str('GetCurrentGameLanguage', (self._ihandle(),))

    @property
    def language_available(self):
        """List of available game languages.

        E.g.: ['english', 'russian']

        :rtype: list[str]
        """
        return self._get_str('GetAvailableGameLanguages', (self._ihandle(),)).split(',')

    @property
    def vac_banned(self):
        """``True`` if the current app is banned by BIsVACBanned.

        :rtype: bool
        """
        return self._get_bool('BIsCybercafe', (self._ihandle(),))

    @property
    def mode_cybercafe(self):
        """``True`` if the current app supports Valve Cybercafe Program.

        :rtype: bool
        """
        return self._get_bool('BIsCybercafe', (self._ihandle(),))

    @property
    def mode_free_weekend(self):
        """``True`` if the user is subscribed to the current app through a free weekend.

        Will return ``False`` for users who have a retail or other type of license.

        .. note::

            Before using, please ask your Valve technical contact how to package and secure your free weekened.

        :rtype: bool
        """
        return self._get_bool('BIsCybercafe', (self._ihandle(),))

    @property
    def low_violence(self):
        """``True`` if the current app is low violence.

        :rtype: bool
        """
        return self._get_bool('BIsLowViolence', (self._ihandle(),))

    @property
    def owned(self):
        """``True`` if user owns the current app.

        :rtype: bool
        """
        return self._get_bool('BIsSubscribed', (self._ihandle(),))

    @property
    def owner(self):
        """Owner user. If different from current user, app is borrowed.

        :rtype: User
        """
        owner_id = self._get_ptr('GetAppOwner', (self._ihandle(),))
        return User(owner_id)

    def mark_corrupt(self, only_files_missing=False):
        """Signal Steam that game files seems corrupt or missing.

        :param bool only_files_missing: Set it to True if only files are missing.
        :rtype: bool
        """
        return self._get_bool('MarkContentCorrupt', (self._ihandle(), only_files_missing))


class Applications(_ApiResourceBase):
    """Exposes methods to get applications data."""

    _res_name = 'ISteamApps'

    installed = InstalledApplications()
    """Interface to installed applications.

    .. code-block:: python

        for app_id, app in api.apps.installed():
            print('%s: %s' % (app_id, app.name))

    """

    current = CurrentApplication()
    """Interface to current application.

    .. code-block:: python

        print(api.apps.current.language_current)

    """
