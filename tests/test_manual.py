import logging
from glob import glob
from os import path

import pytest

from steampak import SteamApi
from steampak.libsteam.resources.apps import Application
from steampak.libsteam.resources.stats import Achievement
from steampak.libsteam.resources.user import User


def set_log_level(lvl):
    logging.basicConfig(level=lvl, format="%(message)s")


APP_SPACEWAR = 480
APP_DLC_SPACEWAR = 110902
APP_AMNESIA = 57300
APP_TIMBERMAN = 398710


LOG_LEVEL = logging.DEBUG
# set_log_level(LOG_LEVEL)

libs = sorted(glob('libsteam_api*'))

if not libs:
    raise Exception('Unable to locate library .so')

LIBRARY_PATH = path.join(path.dirname(__file__), libs[-1])


@pytest.fixture()
def api():
    api = SteamApi(LIBRARY_PATH, app_id=APP_SPACEWAR)
    yield api
    api.shutdown()


@pytest.fixture()
def set_app_id():

    def set_app_id_(app_id):
        return SteamApi(LIBRARY_PATH, app_id=app_id)

    return set_app_id_


def test_basic(api):
    assert api.steam_running
    assert api.app_id == APP_SPACEWAR
    assert api.install_path


def test_utils(api):
    assert api.utils.ipc_call_count > 10
    assert api.utils.seconds_app_active >= 0
    assert api.utils.seconds_computer_active >= 0
    assert api.utils.server_time
    assert api.utils.country_code == 'RU'
    assert api.utils.battery_power == 255
    assert api.utils.app_id == APP_SPACEWAR
    assert api.utils.overlay_enabled is False
    assert api.utils.vr_mode is False
    assert api.utils.ui_language in {'russian', 'english'}
    assert api.utils.universe == 'public'

    api.utils.set_notification_position(api.utils.notification_positions.TOP_LEFT)


def test_current_user(api):
    user = api.current_user
    assert user.steam_id
    assert user.steam_handle
    assert 10 < user.level < 60
    assert user.behind_nat
    assert user.logged_in

    user_obj = user.user
    assert user_obj.name == 'idle sign'
    assert user_obj.state == 'online'


def test_friends(api):

    friends = api.friends

    assert 10 < friends.get_count() < 20

    friends = {friend.name:  friend for friend in friends}
    picked = friends['hiter-fuma']

    assert picked
    # assert picked.level == 33  # todo
    assert picked.name_history == ['hiter-fuma']
    assert picked.state in {'online', 'away', 'offline'}
    assert picked.has_friends()
    picked.show_profile()

    tags = {tag.name: tag for tag in api.friends.tags}

    assert tags
    assert 2 < len(tags['кореша']) < 10


def test_groups(api):

    groups = {group.name: group for group in api.groups}

    assert groups
    group = groups['Steam Universe']
    assert group.alias == 'Steam U'

    stats = group.stats
    assert stats
    assert 900000 > stats['online'] > 100000


def test_apps(api):

    apps = api.apps
    installed = apps.installed

    apps_installed = dict(installed)
    assert apps_installed

    app_current = apps.current
    assert app_current.name == 'Spacewar'
    assert app_current.build_id == 0
    assert app_current.language_current == ''
    assert app_current.language_available == ['english']
    assert app_current.vac_banned is False
    assert app_current.mode_cybercafe is False
    assert app_current.mode_free_weekend is False
    assert app_current.low_violence is False
    assert app_current.owned is True
    assert app_current.owner.name == 'idle sign'
    assert not app_current.mark_corrupt(only_files_missing=True)
    assert app_current.beta_name == ''

    dlcs = dict(app_current.dlcs)
    assert dlcs

    dlc = dlcs[APP_DLC_SPACEWAR]
    assert not dlc.available
    assert dlc.install_dir == ''
    assert dlc.name == 'pieterw test DLC'
    assert not dlc.owned
    assert not dlc.installed
    dlc.install()
    assert dlc.get_download_progress() == (0, 0)
    dlc.uninstall()

    app: Application = Application(APP_AMNESIA)
    assert app.name == 'Amnesia: The Dark Descent'
    assert 'SteamApps/common/Amnesia' in app.install_dir
    assert app.build_id >= 3192428
    assert app.owned
    assert app.installed
    assert app.purchase_time.year == 2011


def test_ach(set_app_id):

    api = set_app_id(APP_TIMBERMAN)
    achs = api.apps.current.achievements

    achs_dict = dict(achs)
    assert len(achs_dict) >= 20

    ach_angel = achs_dict['NEW_ACHIEVEMENT_1_1']  # type: Achievement
    assert ach_angel.title == 'Angel of Axe'
    assert not ach_angel.hidden
    assert 'Score 150' in ach_angel.description
    assert ach_angel.unlocked

    unlocked, unlocked_at = ach_angel.get_unlock_info()
    assert unlocked_at
    assert unlocked_at.year == 2015

    ach_streamer = achs_dict['NEW_ACHIEVEMENT_1_11']  # type: Achievement
    assert not ach_streamer.unlocked
    assert 2 < ach_streamer.global_unlock_percent < 5

    unlocked, unlocked_at = ach_streamer.get_unlock_info()
    assert unlocked is False
    assert unlocked_at is None

    assert ach_streamer.unlock(store=False)
    assert ach_streamer.clear()

    assert achs.store_stats()


def test_overlay(api):
    overlay = api.overlay

    overlay.activate('https://pythonz.net')
    overlay.activate(overlay.PAGE_ACHIEVEMENTS)


def test_screenshots(api):
    screenshots = api.screenshots

    assert not screenshots.is_hooked
    screenshots.toggle_hook()
    screenshots.take()
