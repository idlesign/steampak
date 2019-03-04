#! /usr/bin/env python3
"""

Before you start:

* Demo application requires PyOpenGL (python3-opengl) and in some cases PyOpenGL-accelerate packages to be installed.
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

"""
from os import environ, path

from OpenGL.GL import *
from OpenGL.GLUT import *

from steampak import SteamApi

PATH_CURRENT = path.join(path.abspath(path.dirname(__file__)), 'libsteam_api.so')


class SteampakDemo:

    def __init__(self, fullscreen=False):

        glutInit()
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)

        if fullscreen:
            glutGameModeString('1920x1080:32@60')
            glutEnterGameMode()

        else:
            glutInitWindowPosition(100, 100)
            glutInitWindowSize(1024, 768)
            glutCreateWindow('steampak demo')

        glutDisplayFunc(self.redraw)
        glutIdleFunc(self.redraw)
        glutKeyboardFunc(self.keypress)

        api = SteamApi(
            environ.get('PATH_LIBSTEAM', PATH_CURRENT),
            app_id=environ.get('STEAM_APPID', 480),
        )
        self.api = api

    def redraw(self):
        self.api.run_callbacks()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glutSwapBuffers()

    def keypress(self, key, x, y):

        print('Key pressed: %s' % key)

        if key == b'q':
            self.api.shutdown()
            sys.exit()

        elif key == b'o':
            self.api.overlay.activate()

        elif key == b's':
            self.api.screenshots.take()

        elif key == b'p':
            self.api.overlay.activate('https://github.com/idlesign/steampak/')

    def run(self):
        glutMainLoop()


if __name__ == '__main__':

    demo = SteampakDemo()
    demo.run()
