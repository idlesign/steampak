import ctypes
from datetime import datetime

from .base import _ApiResourceBase, ResultArg
from .user import User


MAX_TITLE_LEN = 300
MAX_DIRECTORY_LEN = 500


class Application(_ApiResourceBase):
    """Exposes methods to get application data."""

    _res_name = 'ISteamApps'

    def __init__(self, app_id):
        if app_id is not None:  # Might be None for current app.
            self.app_id = app_id

    @property
    def owned(self):
        """True if user owns the current app.

        SDK Note: only use this member if you need to check ownership
        of a game related to yours, a demo for example.

        :rtype: bool
        :return:
        """
        return self._get_bool('BIsSubscribedApp', (self._ihandle(), self.app_id))

    @property
    def installed(self):
        """True if app is installed (not necessarily owned).

        :rtype: bool
        :return:
        """
        return self._get_bool('BIsAppInstalled', (self._ihandle(), self.app_id))

    @property
    def name(self):
        """Application name, or None on error.

        SDK Note: restricted interface can only be used by approved apps.

        :return:
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

        :rtype: str
        :return:
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
        :return:
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

        SDK Note: restricted interface can only be used by approved apps.

        :return:
        """
        return self._call(
            'SteamAPI_ISteamAppList_GetAppBuildId', (self._ihandle('SteamAppList'), self.app_id), direct=True)


class InstalledApplications(_ApiResourceBase):
    """Exposes methods to get data on installed applications."""

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
    """Exposes methods to get downloadable content (DLC) data."""

    def __init__(self, app_id):
        super(Dlc, self).__init__(app_id)
        self._name = None
        self._available = None

    @property
    def installed(self):
        """True if the user owns the DLC & if the DLC is installed

        :rtype: bool
        :return:
        """
        return self._get_bool('BIsDlcInstalled', (self._ihandle(), self.app_id))

    def install(self):
        """Installs DLC (for optional DLCs).

        :return:
        """
        self._call('InstallDLC', (self._ihandle(), self.app_id))

    def uninstall(self):
        """Uninstalls DLC (for optional DLCs).

        :return:
        """
        self._call('UninstallDLC', (self._ihandle(), self.app_id))

    def get_download_progress(self):
        """Returns tuple with download progress (for optional DLCs):
        (bytes_downloaded, bytes_total)

        :rtype: tuple
        :return:
        """
        _, current, total = self._call(
            'GetDlcDownloadProgress',
            [self._ihandle(), self.app_id, ResultArg(ctypes.c_uint64), ResultArg(ctypes.c_uint64)])

        return current, total

    @property
    def name(self):
        """DLC name.

        :rtype: str
        :return:
        """
        # Fallback to parent data if necessary.
        return self._name or super(Dlc, self).name

    @property
    def available(self):
        """True if DLC is available.

        :rtype: bool
        :return:
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
    """Exposes methods to get current application data."""

    dlcs = CurrentApplicationDlcs()

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
        :return:
        """
        # todo works?
        max_len = MAX_TITLE_LEN
        _, name = self._call('GetCurrentBetaName', [self._ihandle(), ResultArg(ctypes.c_char * max_len), max_len])
        return self._str_decode(name)

    @property
    def build_id(self):
        """Current application Build ID.
        This may change at any time based on backend updates.

        SDK Note: restricted interface can only be used by approved apps.

        :return:
        """
        return self._call('GetAppBuildId', (self._ihandle(),))

    @property
    def language_current(self):
        """Current game language.

        E.g.: english

        :rtype: str
        :return:
        """
        return self._get_str('GetCurrentGameLanguage', (self._ihandle(),))

    @property
    def language_available(self):
        """List of available game languages.

        E.g.: ['english', 'russian']

        :rtype: list[str]
        :return:
        """
        return self._get_str('GetAvailableGameLanguages', (self._ihandle(),)).split(',')

    @property
    def vac_banned(self):
        """True if the current app is banned by BIsVACBanned.

        :rtype: bool
        :return:
        """
        return self._get_bool('BIsCybercafe', (self._ihandle(),))

    @property
    def mode_cybercafe(self):
        """True if the current app supports Valve Cybercafe Program.

        :rtype: bool
        :return:
        """
        return self._get_bool('BIsCybercafe', (self._ihandle(),))

    @property
    def mode_free_weekend(self):
        """True if the user is subscribed to the current app through a free weekend.
        Will return False for users who have a retail or other type of license.
        Before using, please ask your Valve technical contact how to package and secure your free weekened.

        :rtype: bool
        :return:
        """
        return self._get_bool('BIsCybercafe', (self._ihandle(),))

    @property
    def low_violence(self):
        """True if the current app is low violence.

        :rtype: bool
        :return:
        """
        return self._get_bool('BIsLowViolence', (self._ihandle(),))

    @property
    def owned(self):
        """True if user owns the current app.

        :rtype: bool
        :return:
        """
        return self._get_bool('BIsSubscribed', (self._ihandle(),))

    @property
    def owner(self):
        """Owner user. If different from current user, app is borrowed.

        :rtype: User
        :return:
        """
        owner_id = self._get_ptr('GetAppOwner', (self._ihandle(),))
        return User(owner_id)

    def mark_corrupt(self, only_files_missing=False):
        """Signal Steam that game files seems corrupt or missing.

        :param bool only_files_missing: Set to True if only files are missing.
        :rtype: bool
        :return:
        """
        return self._get_bool('MarkContentCorrupt', (self._ihandle(), only_files_missing))


class Applications(_ApiResourceBase):
    """Exposes methods to get applications data."""

    _res_name = 'ISteamApps'

    installed = InstalledApplications()
    current = CurrentApplication()
