import logging
from glob import glob
from os import path

import pytest

from steampak import SteamApi
from steampak.libsteam.resources.user import User


def set_log_level(lvl):
    logging.basicConfig(level=lvl, format="%(message)s")


APP_SPACEWAR = 480
APP_ID = APP_SPACEWAR

LOG_LEVEL = logging.DEBUG
# set_log_level(LOG_LEVEL)

libs = sorted(glob('libsteam_api*'))

if not libs:
    raise Exception('Unable to locate library .so')

LIBRARY_PATH = path.join(path.dirname(__file__), libs[-1])


@pytest.fixture(scope='module')
def api():
    api = SteamApi(LIBRARY_PATH, app_id=APP_ID)
    yield api
    api.shutdown()


def test_basic(api):
    assert api.steam_running
    assert api.app_id == APP_ID
    assert api.install_path


def test_utils(api):
    assert api.utils.ipc_call_count > 10
    assert api.utils.seconds_app_active >= 0
    assert api.utils.seconds_computer_active >= 0
    assert api.utils.server_time
    assert api.utils.country_code == 'RU'
    assert api.utils.battery_power == 255
    assert api.utils.app_id == APP_ID
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

    picked = None

    for friend in friends():
        name = friend.name
        assert name

        if name == 'hiter-fuma':
            picked = friend  # type: User

    assert picked
    # assert picked.level == 33  # todo
    assert picked.name_history == ['hiter-fuma']
    assert picked.state in {'online', 'away', 'offline'}
    assert picked.has_friends()
    picked.show_profile()

    tags = {tag.name: tag for tag in api.friends.tags()}

    assert tags
    assert 2 < len(tags['кореша']) < 10

    groups = {group.name: group for group in api.groups()}

    assert groups
    group = groups['Steam Universe']
    assert group.alias == 'Steam U'

    stats = group.stats
    assert stats
    assert 900000 > stats['online'] > 100000

