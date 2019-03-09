#! /usr/bin/env python3
"""

Before you start:

* Demo application requires ``arcade`` packages to be installed: http://arcade.academy/installation_linux.html.
* Make sure `steampak` is available to your Python 3.

1. Set PATH_LIBSTEAM environment variable to a proper path or put `libsteam_api.so` into `demo` directory
   near this very file.

2. Add `steampak_demo.py` into your game library:
   Steam -> Library -> + ADD A GAME -> Add a Non-Steam Game ... -> BROWSE, ADD SELECTED PROGRAMS

3. Launch demo from Steam Library.

Controls:
    * q - quit
    * o - show overlay
    * p - show overlay with browser launched


Steam debug hint:

* Launch Steam with -console -debug_steamapi -dev
* Open Steam -> Console, run ``log_ipc 1``, ``log_callbacks``
* IPC log: tail-f ~/.steam/logs/ipc_SteamClient.log

"""
from os import environ, path

import arcade


class SteampakDemo(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        self._log = ''

        try:
            from steampak import SteamApi

            steam = SteamApi(
                environ.get('PATH_LIBSTEAM', path.join(path.abspath(path.dirname(__file__)), 'libsteam_api.so')),
                app_id=environ.get('STEAM_APPID', 480),
            )

            steam_run_callbacks = steam.run_callbacks

        except Exception as e:
            self.log_add('exception: %s' % e)
            steam = None
            steam_run_callbacks = lambda: None

        self.steam = steam
        self.steam_run_callbacks = steam_run_callbacks

    def on_draw(self):
        arcade.start_render()
        self.steam_run_callbacks()
        arcade.draw_text(self._log, 10, 10, arcade.color.WHITE, anchor_y='bottom')

    def log_add(self, val):
        self._log += '\n%s' % val

    def on_key_press(self, key, key_modifiers):
        log_add = self.log_add

        log_add('key: %s' % key)

        if key == 113:  # q
            log_add('closing')
            self.close()

        else:

            try:

                if key == 111:  # o
                    log_add('overlay activate')
                    self.steam.overlay.activate()

                elif key == 115:  # s
                    log_add('take screenshot')
                    self.steam.screenshots.take()

                elif key == 112:
                    log_add('overlay link')  # p
                    self.steam.overlay.activate('https://github.com/idlesign/steampak/')

            except Exception as e:
                log_add('exception: %s' % e)


if __name__ == '__main__':

    SteampakDemo(800, 600, 'steampak demo')
    arcade.run()
