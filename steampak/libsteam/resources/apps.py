import ctypes

from .base import _ApiResourceBase, ResultArg


class Application(_ApiResourceBase):
    """Exposes methods to get application data."""

    _res_name = 'ISteamAppList'

    def __init__(self, app_id):
        self.app_id = app_id

    @property
    def owned(self):
        """True if user owns the current app.

        SDK Note: only use this member if you need to check ownership
        of a game related to yours, a demo for example.

        :rtype: bool
        :return:
        """
        return self._get_bool(
            'SteamAPI_ISteamApps_BIsSubscribedApp', (self._ihandle('SteamApps'), self.app_id), direct=True)

    @property
    def name(self):
        """Application name, or None on error.

        SDK Note: restricted interface can only be used by approved apps.

        :return:
        """
        max_len = 300
        result, name = self._call(
            'GetAppName', [self._handle, self.app_id, ResultArg(ctypes.c_char * max_len), max_len])

        if result == -1:
            return None

        return self._str_decode(name)

    @property
    def install_dir(self):
        """Returns application installation path, or None on error.

        SDK Note: restricted interface can only be used by approved apps.

        :return:
        """
        max_len = 500
        result, name = self._call(
            'GetAppInstallDir', [self._handle, self.app_id, ResultArg(ctypes.c_char * max_len), max_len])

        if result == -1:
            return None

        return self._str_decode(name)

    @property
    def build_id(self):
        """Returns an application Build ID.
        This may change at any time based on backend updates.

        Note: restricted interface can only be used by approved apps.

        :return:
        """
        return self._call('GetAppBuildId', (self._handle, self.app_id))


class InstalledApplications(_ApiResourceBase):
    """Exposes methods to get data on installed applications."""

    _res_name = 'ISteamAppList'

    def __len__(self):
        """Returns a number of currently installed applications.

        :rtype: int
        :return:
        """
        return self._call('GetNumInstalledApps', (self._handle,))

    def __call__(self):
        """Generator. Returns Application objects, representing currently installed applications.

        :rtype: Application
        :return:
        """
        max_count = len(self)
        _, apps_id = self._call(
            'GetInstalledApps', [self._handle, ResultArg(ctypes.c_uint32 * max_count), max_count])

        for app_id in apps_id:
            yield app_id, Application(app_id)


class CurrentApplication(_ApiResourceBase):
    """Exposes methods to get current application data."""

    _res_name = 'ISteamApps'

    @property
    def language_current(self):
        """Current game language.

        E.g.: english

        :rtype: str
        :return:
        """
        return self._get_str('GetCurrentGameLanguage', (self._handle,))

    @property
    def language_available(self):
        """List of available game languages.

        E.g.: ['english', 'russian']

        :rtype: list[str]
        :return:
        """
        return self._get_str('GetAvailableGameLanguages', (self._handle,)).split(',')

    @property
    def vac_banned(self):
        """True if the current app is banned by BIsVACBanned.

        :rtype: bool
        :return:
        """
        return self._get_bool('BIsCybercafe', (self._handle,))

    @property
    def mode_cybercafe(self):
        """True if the current app supports Valve Cybercafe Program.

        :rtype: bool
        :return:
        """
        return self._get_bool('BIsCybercafe', (self._handle,))

    @property
    def mode_free_weekend(self):
        """True if the user is subscribed to the current app through a free weekend.
        Will return False for users who have a retail or other type of license.
        Before using, please ask your Valve technical contact how to package and secure your free weekened.

        :rtype: bool
        :return:
        """
        return self._get_bool('BIsCybercafe', (self._handle,))

    @property
    def low_violence(self):
        """True if the current app is low violence.

        :rtype: bool
        :return:
        """
        return self._get_bool('BIsLowViolence', (self._handle,))

    @property
    def owned(self):
        """True if user owns the current app.

        :rtype: bool
        :return:
        """
        return self._get_bool('BIsSubscribed', (self._handle,))


class Applications(_ApiResourceBase):
    """Exposes methods to get applications data."""

    _res_name = 'ISteamApps'

    installed = InstalledApplications()
    current = CurrentApplication()
