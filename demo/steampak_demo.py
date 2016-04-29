#! /usr/bin/env python
"""
Demo application requires `PyOpenGL` and `PyOpenGL-accelerate` packages to be installed.

1. Change LIBRARY_PATH (see below) to a proper path or put `libsteam_api.so` into `demo` directory
   near this very file.

2. Change `Exec` param in `steampak_demo.desktop` file to a proper path.

3. Add `steampak_demo.desktop` into your game library:
   Steam -> Library -> Add a game... -> Add a non-Steam game ...

4. Launch demo from Steam.


Controls:
q - quit
o - show overlay
p - show overlay with browser launched

"""
import sys

import OpenGL.GLUT as glut

from steampak import SteamApi
from steampak.libsteam.resources.apps import Application


LIBRARY_PATH = '/home/shared/idle/code/i/steampak/libsteam_api.so'


class SteampakDemo(object):

    def __init__(self, app_id, fullscreen=False):
        glut.glutInit()
        glut.glutInitDisplayMode(glut.GLUT_DOUBLE | glut.GLUT_RGBA)

        if fullscreen:
            glut.glutGameModeString('1920x1080:32@60')
            glut.glutEnterGameMode()
        else:
            glut.glutInitWindowPosition(100, 100)
            glut.glutInitWindowSize(1024, 768)
            glut.glutCreateWindow('steampak demo')

        glut.glutDisplayFunc(self.redraw)
        glut.glutIdleFunc(self.redraw)
        glut.glutKeyboardFunc(self.keypress)

        self.api = SteamApi(LIBRARY_PATH, app_id=app_id)

    def redraw(self):
        glut.glutSwapBuffers()
        self.api.run_callbacks()

    def keypress(self, key, x, y):

        if key == 'q':
            self.api.shutdown()
            sys.exit()

        elif key == 'o':
            self.api.overlay.activate()

        elif key == 'p':
            self.api.overlay.activate('https://github.com/idlesign/steampak/')

    def run(self):
        glut.glutMainLoop()


if __name__ == '__main__':

    APP_ID = 480
    demo = SteampakDemo(APP_ID)
    demo.run()
