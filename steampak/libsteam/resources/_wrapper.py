import faulthandler
from os import environ

from ctyped.toolbox import Library
from ctyped.types import CObject, CPointer, CInt16, CRef
from ._versions import *

faulthandler.enable()


lib = Library(environ.get('STEAM_API_LIB', 'libsteam_api'), int_bits=32)


########################################################################


with lib.s('SteamAPI_'):

    @lib.f('Init')
    def steam_init() -> bool:
        ...

    @lib.f('Shutdown')
    def steam_shutdown():
        ...

    @lib.f('RunCallbacks')
    def steam_run_callbacks():
        ...

    @lib.f('IsSteamRunning')
    def steam_is_running() -> bool:
        ...

    @lib.f('RestartAppIfNecessary')
    def steam_restart_if_necessary(app_id: int) -> bool:
        ...

    @lib.f('GetHSteamUser')
    def get_h_user() -> int:
        ...

    @lib.f('GetHSteamPipe')
    def get_h_pipe() -> int:
        ...

    @lib.f('GetSteamInstallPath')
    def get_install_path() -> str:
        ...

    @lib.cls(prefix='ISteamUser_')
    class User(CObject):

        @lib.m('GetSteamID', int_bits=64)
        def get_id(self) -> int:
            ...

        @lib.m('GetPlayerSteamLevel')
        def get_level(self) -> int:
            ...

        @lib.m('BIsBehindNAT')
        def get_is_behind_nat(self) -> bool:
            ...

        @lib.m('BLoggedOn')
        def get_is_logged_on(self) -> bool:
            ...

    @lib.cls(prefix='ISteamFriends_', int_bits=64, int_sign=False)
    class Friends(CObject):

        @lib.m('GetFriendCount',)
        def get_count(self, flt: int) -> int:
            ...

        @lib.m('GetPersonaName')
        def get_my_name(self) -> str:
            ...

        @lib.m('GetPersonaState')
        def get_my_state(self) -> int:
            ...

        @lib.m('GetPlayerNickname')
        def get_nickname(self, uid: int) -> str:
            ...

        @lib.m('HasFriend')
        def get_has_friend(self, uid: int, flt: int) -> bool:
            ...

        @lib.m('GetFriendByIndex')
        def get_by_index(self, idx: int, flt: int) -> int:
            ...

        @lib.m('GetFriendPersonaName')
        def get_name(self, uid: int) -> str:
            ...

        @lib.m('GetFriendPersonaState')
        def get_state(self, uid: int) -> int:
            ...

        @lib.m('GetClanCount')
        def get_clan_count(self) -> int:
            ...

        @lib.m('GetClanByIndex')
        def get_clan(self, idx: int) -> int:
            ...

        @lib.m('GetClanName')
        def get_clan_name(self, cid: int) -> str:
            ...

        @lib.m('GetClanTag')
        def get_clan_alias(self, cid: int) -> str:
            ...

        @lib.m('GetClanActivityCounts')
        def get_clan_stats(self, cid: int, online: CRef, ingame: CRef, chatting: CRef) -> bool:
            ...

        @lib.m('GetFriendsGroupCount')
        def get_group_count(self) -> int:
            ...

        @lib.m('GetFriendsGroupName')
        def get_group_name(self, gid: int) -> str:
            ...

        @lib.m('GetFriendsGroupMembersCount')
        def get_group_members_count(self, gid: int) -> int:
            ...

        @lib.m('GetFriendsGroupIDByIndex')
        def get_group(self, idx: int) -> CInt16:
            ...

        @lib.m('GetFriendPersonaNameHistory')
        def get_name_history(self, uid: int, idx: int) -> str:
            ...

        @lib.m('GetFriendSteamLevel')
        def get_level(self, uid: int) -> int:
            ...

        @lib.m('ActivateGameOverlayToUser')
        def activate_overlay(self, realm: str, uid: int) -> int:
            ...

        @lib.m('ActivateGameOverlayToWebPage')
        def activate_overlay_url(self, url: str) -> None:
            ...

        @lib.m('ActivateGameOverlay')
        def activate_overlay_game(self, page: str) -> None:
            ...

    @lib.cls(prefix='ISteamMatchmaking_')
    class Matchmaking(CObject):
        """"""

    @lib.cls(prefix='ISteamMatchmakingServers_')
    class MatchmakingServers(CObject):
        """"""

    @lib.cls(prefix='ISteamUserStats_', int_sign=False)
    class UserStats(CObject):

        @lib.m('GetNumAchievements')
        def get_ach_count(self) -> int:
            ...

        @lib.m('GetAchievementName')
        def get_ach_name(self, idx: int) -> str:
            ...

        @lib.m('GetAchievementDisplayAttribute')
        def get_ach_attrib(self, aname: str, attr: str) -> str:
            ...

        @lib.m('GetAchievement')
        def get_ach(self, aname: str, achieved: CRef) -> bool:
            ...

        @lib.m('GetAchievementAchievedPercent')
        def get_ach_progress(self, aname: str, percent: CRef) -> bool:
            ...

        @lib.m('GetAchievementAndUnlockTime')
        def get_ach_unlock_info(self, aname: str, achieved: CRef, achieved_at: CRef) -> bool:
            ...

        @lib.m('StoreStats')
        def store_stats(self) -> bool:
            ...

        @lib.m('SetAchievement')
        def ach_unlock(self, aname: str) -> bool:
            ...

        @lib.m('ClearAchievement')
        def ach_lock(self, aname: str) -> bool:
            ...


    @lib.cls(prefix='ISteamApps_', int_sign=False)
    class Apps(CObject):

        @lib.m('GetAppInstallDir', int_sign=True)
        def get_install_dir(self, aid: int, result: CRef, max_len: int) -> int:
            ...

        @lib.m('BIsSubscribedApp')
        def get_is_subscribed(self, aid: int) -> bool:
            ...

        @lib.m('BIsAppInstalled')
        def get_is_installed(self, aid: int) -> bool:
            ...

        @lib.m('BIsDlcInstalled')
        def get_is_dlc_installed(self, aid: int) -> bool:
            ...

        @lib.m('InstallDLC')
        def dlc_install(self, aid: int):
            ...

        @lib.m('UninstallDLC')
        def dlc_uninstall(self, aid: int):
            ...

        @lib.m('GetDlcDownloadProgress')
        def get_dlc_download_progress(self, aid: int, downloaded: CRef, total: CRef) -> bool:
            ...

        @lib.m('GetEarliestPurchaseUnixTime')
        def get_purchase_time(self, aid: int) -> int:
            ...

        @lib.m('GetAppBuildId')
        def get_current_build_id(self) -> int:
            ...

        @lib.m('GetCurrentGameLanguage')
        def get_current_language(self) -> str:
            ...

        @lib.m('GetAvailableGameLanguages')
        def get_available_languages(self) -> str:
            ...

        @lib.m('BIsVACBanned')
        def get_is_vac_banned(self) -> bool:
            ...

        @lib.m('BIsCybercafe')
        def get_is_cybercafe(self) -> bool:
            ...

        @lib.m('BIsSubscribedFromFreeWeekend')
        def get_is_free_weekend(self) -> bool:
            ...

        @lib.m('BIsLowViolence')
        def get_is_low_violence(self) -> bool:
            ...

        @lib.m('BIsSubscribed')
        def get_is_owned(self) -> bool:
            ...

        @lib.m('GetAppOwner', int_bits=64)
        def get_owner(self) -> int:
            ...

        @lib.m('MarkContentCorrupt')
        def mark_corrupt(self, files_missing: bool) -> bool:
            ...

        @lib.m('GetCurrentBetaName', int_sign=True)
        def get_name_beta(self, result: CRef, max_len: int) -> bool:
            ...

        @lib.m('GetDLCCount')
        def get_dlc_count(self) -> int:
            ...

        @lib.m('BGetDLCDataByIndex')
        def get_dlc_by_index(self, idx: int, aid: CRef, available: CRef, name: CRef, max_len: int) -> bool:
            ...


    @lib.cls(prefix='ISteamNetworking_')
    class Networking(CObject):
        """"""

    @lib.cls(prefix='ISteamRemoteStorage_')
    class RemoteStorage(CObject):
        """"""

    @lib.cls(prefix='ISteamScreenshots_')
    class Screenshots(CObject):

        @lib.m('TriggerScreenshot')
        def take(self) -> None:
            ...

        @lib.m('HookScreenshots')
        def toggle_hook(self, flag: bool) -> None:
            ...

        @lib.m('IsScreenshotsHooked')
        def get_is_hooked(self) -> bool:
            ...

    @lib.cls(prefix='ISteamHTTP_')
    class Http(CObject):
        """"""

    @lib.cls(prefix='ISteamController_')
    class Controller(CObject):
        """"""

    @lib.cls(prefix='ISteamUGC_')
    class Ugc(CObject):
        """"""

    @lib.cls(prefix='ISteamAppList_', int_bits=32, int_sign=False)
    class AppList(CObject):

        @lib.m('GetNumInstalledApps')
        def get_installed_count(self) -> int:
            ...

        @lib.m('GetInstalledApps')
        def get_installed(self, result: CRef, max_count: int) -> int:
            ...

        @lib.m('GetAppName', int_sign=True)
        def get_name(self, aid: int, result: CRef, max_len: int) -> int:
            ...

        @lib.m('GetAppInstallDir', int_sign=True)
        def get_install_dir(self, aid: int, result: CRef, max_len: int) -> int:
            ...

        @lib.m('GetAppBuildId')
        def get_build_id(self, aid: int) -> int:
            ...

    @lib.cls(prefix='ISteamMusic_')
    class Music(CObject):
        """"""

    @lib.cls(prefix='ISteamMusicRemote_')
    class MusicRemote(CObject):
        """"""

    @lib.cls(prefix='ISteamHTMLSurface_')
    class HtmlSurface(CObject):
        """"""

    @lib.cls(prefix='ISteamInventory_')
    class Inventory(CObject):
        """"""

    @lib.cls(prefix='ISteamVideo_')
    class Video(CObject):
        """"""

    @lib.cls(prefix='ISteamParentalSettings_')
    class ParentalSettings(CObject):
        """"""

    @lib.cls(prefix='ISteamGameServer_')
    class GameServer(CObject):
        """"""

    @lib.cls(prefix='ISteamGameServerStats_')
    class GameServerStats(CObject):
        """"""

    @lib.cls(prefix='ISteamUtils_')
    class Utils(CObject):

        @lib.m('GetAppID')
        def get_app_id(self) -> int:
            ...

        @lib.m('GetSteamUILanguage')
        def get_ui_language(self) -> str:
            ...

        @lib.m('GetIPCountry')
        def get_country_code(self) -> str:
            ...

        @lib.m('GetCurrentBatteryPower')
        def get_battery_power(self) -> int:
            ...

        @lib.m('GetServerRealTime')
        def get_server_time(self) -> int:
            ...

        @lib.m('GetSecondsSinceComputerActive')
        def get_seconds_computer_active(self) -> int:
            ...

        @lib.m('GetSecondsSinceAppActive')
        def get_seconds_app_active(self) -> int:
            ...

        @lib.m('GetIPCCallCount')
        def get_ipc_call_count(self) -> int:
            ...

        @lib.m('GetConnectedUniverse')
        def get_connected_universe(self) -> int:
            ...

        @lib.m('IsOverlayEnabled')
        def get_overlay_enabled(self) -> bool:
            ...

        @lib.m('IsSteamRunningInVR')
        def get_vr_mode(self) -> bool:
            ...

        @lib.m('SetOverlayNotificationPosition')
        def set_notify_position(self, position: int) -> int:
            ...

    @lib.cls(prefix='ISteamClient_')
    class Client(CObject):

        def __init__(self, *args, **kwargs):
            super().__init__()

            self.value = get_client(VERSION_CLIENT)

            h_user = get_h_user()
            self.h_user = h_user

            h_pipe = get_h_pipe()

            self.utils = self._cget_utils(h_pipe, VERSION_UTILS)
            self.user = self._cget_user(h_user, h_pipe, VERSION_USER)
            self.friends = self._cget_friends(h_user, h_pipe, VERSION_FRIENDS)
            self.matchmaking = self._cget_matchmaking(h_user, h_pipe, VERSION_MATCHMAKING)
            self.matchmaking_servers = self._cget_matchmaking_servers(h_user, h_pipe, VERSION_MATCHMAKING_SERVERS)
            self.user_stats = self._cget_user_stats(h_user, h_pipe, VERSION_USER_STATS)
            self.apps = self._cget_apps(h_user, h_pipe, VERSION_APPS)
            self.networking = self._cget_networking(h_user, h_pipe, VERSION_NETWORKING)
            self.remote_storage = self._cget_remote_storage(h_user, h_pipe, VERSION_REMOTE_STORAGE)
            self.screenshots = self._cget_screenshots(h_user, h_pipe, VERSION_SCREENSHOTS)
            self.http = self._cget_http(h_user, h_pipe, VERSION_HTTP)
            self.controller = self._cget_controller(h_user, h_pipe, VERSION_CONTROLLER)
            self.ugc = self._cget_ugc(h_user, h_pipe, VERSION_UGC)
            self.app_list = self._cget_app_list(h_user, h_pipe, VERSION_APP_LIST)
            self.music = self._cget_music(h_user, h_pipe, VERSION_MUSIC)
            self.music_remote = self._cget_music_remote(h_user, h_pipe, VERSION_MUSIC_REMOTE)
            self.html_surface = self._cget_html_surface(h_user, h_pipe, VERSION_HTML_SURFACE)
            self.inventory = self._cget_inventory(h_user, h_pipe, VERSION_INVENTORY)
            self.video = self._cget_video(h_user, h_pipe, VERSION_VIDEO)
            self.parental_settings = self._cget_parental_settings(h_user, h_pipe, VERSION_PARENTAL_SETTINGS)
            self.game_server = self._cget_game_server(h_user, h_pipe, VERSION_GAME_SERVER)
            self.game_server_stats = self._cget_game_server_stats(h_user, h_pipe, VERSION_GAME_SERVER_STATS)

        def __setattr__(self, name, value):

            if not value:

                if name == '_ct_val':
                    name = 'Steam Client. Please make sure Steam is running.'

                raise Exception(f'Unable to initialize {name} interface.')

            super().__setattr__(name, value)

        @lib.m('GetISteamUtils')
        def _cget_utils(self, pipe_h: int, version: str) -> Utils:
            ...

        @lib.m('GetISteamGameServer')
        def _cget_game_server(self, user_h: int, pipe_h: int, version: str) -> GameServer:
            ...

        @lib.m('GetISteamGameServerStats')
        def _cget_game_server_stats(self, user_h: int, pipe_h: int, version: str) -> GameServerStats:
            ...

        @lib.m('GetISteamUser')
        def _cget_user(self, user_h: int, pipe_h: int, version: str) -> User:
            ...

        @lib.m('GetISteamFriends')
        def _cget_friends(self, user_h: int, pipe_h: int, version: str) -> Friends:
            ...

        @lib.m('GetISteamApps')
        def _cget_apps(self, user_h: int, pipe_h: int, version: str) -> Apps:
            ...

        @lib.m('GetISteamAppList')
        def _cget_app_list(self, user_h: int, pipe_h: int, version: str) -> AppList:
            ...

        @lib.m('GetISteamHTTP')
        def _cget_http(self, user_h: int, pipe_h: int, version: str) -> Http:
            ...

        @lib.m('GetISteamUGC')
        def _cget_ugc(self, user_h: int, pipe_h: int, version: str) -> Ugc:
            ...

        @lib.m('GetISteamHTMLSurface')
        def _cget_html_surface(self, user_h: int, pipe_h: int, version: str) -> HtmlSurface:
            ...

        @lib.m('GetISteamMusic')
        def _cget_music(self, user_h: int, pipe_h: int, version: str) -> Music:
            ...

        @lib.m('GetISteamInventory')
        def _cget_inventory(self, user_h: int, pipe_h: int, version: str) -> Inventory:
            ...

        @lib.m('GetISteamMusicRemote')
        def _cget_music_remote(self, user_h: int, pipe_h: int, version: str) -> MusicRemote:
            ...

        @lib.m('GetISteamController')
        def _cget_controller(self, user_h: int, pipe_h: int, version: str) -> Controller:
            ...

        @lib.m('GetISteamScreenshots')
        def _cget_screenshots(self, user_h: int, pipe_h: int, version: str) -> Screenshots:
            ...

        @lib.m('GetISteamVideo')
        def _cget_video(self, user_h: int, pipe_h: int, version: str) -> Video:
            ...

        @lib.m('GetISteamRemoteStorage')
        def _cget_remote_storage(self, user_h: int, pipe_h: int, version: str) -> RemoteStorage:
            ...

        @lib.m('GetISteamNetworking')
        def _cget_networking(self, user_h: int, pipe_h: int, version: str) -> Networking:
            ...

        @lib.m('GetISteamUserStats')
        def _cget_user_stats(self, user_h: int, pipe_h: int, version: str) -> UserStats:
            ...

        @lib.m('GetISteamMatchmaking')
        def _cget_matchmaking(self, user_h: int, pipe_h: int, version: str) -> Matchmaking:
            ...

        @lib.m('GetISteamMatchmakingServers')
        def _cget_matchmaking_servers(self, user_h: int, pipe_h: int, version: str) -> MatchmakingServers:
            ...

        @lib.m('GetISteamParentalSettings')
        def _cget_parental_settings(self, user_h: int, pipe_h: int, version: str) -> ParentalSettings:
            ...


@lib.function('SteamInternal_CreateInterface')
def get_client(version: str) -> CPointer:
    ...


lib.bind_types()


def print_known_functions():
    print('==' * 30)

    for n in lib.funcs.keys():
        print(n)


# print_known_functions()
