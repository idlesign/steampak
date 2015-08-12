import ctypes

from .base import _ApiResourceBase, ResultArg


class Application(_ApiResourceBase):
    """Exposes methods to get application data."""

    _res_name = 'ISteamAppList'

    def __init__(self, app_id):
        self.app_id = app_id

    @property
    def name(self):
        """Application name, or None on error.

        Note: restricted interface can only be used by approved apps.

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

        Note: restricted interface can only be used by approved apps.

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


class Applications(_ApiResourceBase):
    """Exposes methods to get applications data."""

    _res_name = 'ISteamApps'

    installed = InstalledApplications()
