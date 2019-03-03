from datetime import datetime

from ctyped.types import CRef
from .base import _ApiResourceBase
from .stats import CurrentApplicationAchievements
from .user import User


class Application(_ApiResourceBase):
    """Exposes methods to get application data.

    Aliased as ``steampak.SteamApplication``.

    .. code-block:: python

        from steampak import SteamApplication

        # We use `Spacewar` app ID. (This game is provided with SDK).
        my_app = SteamApplication(480)

    """

    def __init__(self, app_id, *args, **kwargs):
        """
        :param int|None app_id: Application (game) ID.
        """
        client = self.get_client()

        self._iface = client.apps
        self._iface_list = client.app_list

        super().__init__(*args, **kwargs)

        if app_id is not None:  # Might be None for current app.
            self.app_id = app_id

    def __str__(self):
        return self.name

    @property
    def owned(self):
        """``True`` if user owns the current app.

        .. warning::

            Only use this member if you need to check ownership of a game related to yours, a demo for example.

        :rtype: bool
        """
        return self._iface.get_is_subscribed(self.app_id)

    @property
    def installed(self):
        """``True`` if app is installed (not necessarily owned).

        :rtype: bool
        """
        return self._iface.get_is_installed(self.app_id)

    @property
    def name(self):
        """Application name, or None on error.

        .. warning::

            Restricted interface can only be used by approved apps.

        :rtype: str
        """
        return self._get_str(self._iface_list.get_name, [self.app_id])

    @property
    def install_dir(self):
        """Returns application installation path.

        .. note::

            If fails this falls back to a restricted interface, which can only be used by approved apps.

        :rtype: str
        """
        max_len = 500

        directory = self._get_str(self._iface.get_install_dir, [self.app_id], max_len=max_len)

        if not directory:
            # Fallback to restricted interface (can only be used by approved apps).
            directory = self._get_str(self._iface_list.get_install_dir, [self.app_id], max_len=max_len)

        return directory

    @property
    def purchase_time(self):
        """Date and time of app purchase.

        :rtype: datetime
        """
        ts = self._iface.get_purchase_time(self.app_id)
        return datetime.utcfromtimestamp(ts)

    @property
    def build_id(self):
        """Application Build ID.
        This may change at any time based on backend updates.

        .. warning::

            Restricted interface can only be used by approved apps.

        :rtype: int
        """
        return self._iface_list.get_build_id(self.app_id)


class InstalledApplications(_ApiResourceBase):
    """Exposes methods to get data on installed applications.

    Interface can be accessed through ``api.apps.installed``.

    .. warning::

        Restricted interface can only be used by approved apps.

    """

    def __init__(self, *args, **kwargs):
        self._iface = self.get_client().app_list
        super().__init__(*args, **kwargs)

    def __len__(self):
        """Returns a number of currently installed applications.

        :rtype: int
        """
        return self._iface.get_installed_count()

    def __call__(self):
        """Generator. Returns Application objects, representing currently installed applications.

        :rtype: tuple(int, Application)
        :return:
        """
        max_count = len(self)

        apps_ids = CRef.carray(int, size=max_count)

        total = self._iface.get_installed(apps_ids, max_count)

        for app_id in apps_ids:
            yield app_id, Application(app_id)

    def __iter__(self):
        return iter(self())


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
        self._iface = self.get_client().apps
        super(Dlc, self).__init__(app_id)
        self._name = None
        self._available = None

    @property
    def installed(self):
        """``True`` if the user owns the DLC & if the DLC is installed.

        :rtype: bool
        """
        return self._iface.get_is_dlc_installed(self.app_id)

    def install(self):
        """Installs DLC (for optional DLCs)."""
        self._iface.dlc_install(self.app_id)

    def uninstall(self):
        """Uninstalls DLC (for optional DLCs)."""
        self._iface.dlc_uninstall(self.app_id)

    def get_download_progress(self):
        """Returns tuple with download progress (for optional DLCs):

            (bytes_downloaded, bytes_total)

        :rtype: tuple
        """
        downloaded = CRef.cint()
        total = CRef.cint()

        result = self._iface.get_dlc_download_progress(self.app_id, downloaded, total)

        if not result:
            return 0, 0

        return int(downloaded), int(total)

    @property
    def name(self):
        """DLC name.

        :rtype: str
        """
        # Fallback to parent data if necessary.
        return self._name or super().name

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

    def __init__(self, *args, **kwargs):
        self._iface = self.get_client().apps
        super().__init__(*args, **kwargs)

    def __len__(self):
        """Returns a number of current application .

        :rtype: int
        :return:
        """
        return self._iface.get_dlc_count()

    def __call__(self):
        """Generator. Returns Dlc objects.

        :rtype: tuple(int, Dlc)
        :return:
        """
        max_len = 300

        for idx in range(len(self)):

            app_id = CRef.cint()
            available = CRef.cbool()
            name = CRef.carray(str, size=max_len)

            if not self._iface.get_dlc_by_index(idx, app_id, available, name, max_len):
                continue

            app_id = int(app_id)

            dlc = Dlc(app_id)
            # Populate data.
            dlc._name = str(name)
            dlc._available = bool(available)

            yield app_id, dlc

    def __iter__(self):
        return iter(self())


class CurrentApplication(Application):
    """Exposes methods to get current application data.

    Interface can be accessed through ``api.apps.current``.

    .. code-block:: python

        from steampak import SteamApi

        api = SteamApi(LIBRARY_PATH, app_id=APP_ID)

        print(api.apps.current.language_current)

    """

    dlcs: CurrentApplicationDlcs = None
    """Interface to DLCs of current application.

    .. code-block:: python

        for dlc_id, dlc in api.apps.current.dlcs():
            print('%s: %s' % (dlc_id, dlc.name))

    """

    achievements: CurrentApplicationAchievements = None
    """Current application (game) achievements.

    .. code-block:: python

        for ach_name, ach in api.apps.current.achievements():
            print('%s: %s' % (ach_name, ach.title))

    """

    def __init__(self, *args, **kwargs):
        self._iface = self.get_client().apps
        self._iface_utils = self.get_client().utils
        super().__init__(None, *args, **kwargs)

        self.dlcs = CurrentApplicationDlcs()
        self.achievements = CurrentApplicationAchievements()

    @property
    def app_id(self):
        # Overrode to support parent class methods.
        return self._iface_utils.get_app_id()

    @property
    def beta_name(self):
        """Current beta branch name, 'public' is the default branch.

        :rtype: str
        """
        return self._get_str(self._iface.get_name_beta, [])

    @property
    def build_id(self):
        """Current application Build ID.
        This may change at any time based on backend updates.

        .. warning::

            Restricted interface can only be used by approved apps.

        :rtype: int
        """
        return self._iface.get_current_build_id()

    @property
    def language_current(self):
        """Current game language.

        E.g.: english

        :rtype: str
        """
        return self._iface.get_current_language()

    @property
    def language_available(self):
        """List of available game languages.

        E.g.: ['english', 'russian']

        :rtype: list[str]
        """
        return self._iface.get_available_languages().split(',')

    @property
    def vac_banned(self):
        """``True`` if the current app is banned by BIsVACBanned.

        :rtype: bool
        """
        return self._iface.get_is_vac_banned()

    @property
    def mode_cybercafe(self):
        """``True`` if the current app supports Valve Cybercafe Program.

        :rtype: bool
        """
        return self._iface.get_is_cybercafe()

    @property
    def mode_free_weekend(self):
        """``True`` if the user is subscribed to the current app through a free weekend.

        Will return ``False`` for users who have a retail or other type of license.

        .. note::

            Before using, please ask your Valve technical contact how to package and secure your free weekened.

        :rtype: bool
        """
        return self._iface.get_is_free_weekend()

    @property
    def low_violence(self):
        """``True`` if the current app is low violence.

        :rtype: bool
        """
        return self._iface.get_is_low_violence()

    @property
    def owned(self):
        """``True`` if user owns the current app.

        :rtype: bool
        """
        return self._iface.get_is_owned()

    @property
    def owner(self):
        """Owner user. If different from current user, app is borrowed.

        :rtype: User
        """
        return User(self._iface.get_owner())

    def mark_corrupt(self, only_files_missing=False):
        """Signal Steam that game files seems corrupt or missing.

        :param bool only_files_missing: Set it to True if only files are missing.
        :rtype: bool
        """
        return self._iface.mark_corrupt(only_files_missing)


class Applications(_ApiResourceBase):
    """Exposes methods to get applications data."""

    installed: InstalledApplications = None
    """Interface to installed applications.

    .. code-block:: python

        for app_id, app in api.apps.installed:
            print('%s: %s' % (app_id, app.name))

    """

    current: CurrentApplication = None
    """Interface to current application.

    .. code-block:: python

        print(api.apps.current.language_current)

    """

    def __init__(self, *args, **kwargs):
        self._iface = self.get_client().apps
        super().__init__(*args, **kwargs)

        self.installed = InstalledApplications()
        self.current = CurrentApplication()
