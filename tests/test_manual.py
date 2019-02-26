import logging
from glob import glob
from os import path

import pytest

from steampak import SteamApi


def set_log_level(lvl):
    logging.basicConfig(level=lvl, format="%(message)s")


APP_SPACEWAR = 480
APP_ID = APP_SPACEWAR

LOG_LEVEL = logging.DEBUG
set_log_level(LOG_LEVEL)

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
    assert api.utils.ipc_call_count == 30  # may vary probably
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

