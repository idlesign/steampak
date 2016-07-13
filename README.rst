steampak
========
https://github.com/idlesign/steampak

.. image:: https://img.shields.io/pypi/v/steampak.svg
    :target: https://pypi.python.org/pypi/steampak

.. image:: https://img.shields.io/pypi/dm/steampak.svg
    :target: https://pypi.python.org/pypi/steampak

.. image:: https://img.shields.io/pypi/l/steampak.svg
    :target: https://pypi.python.org/pypi/steampak


**This software is not affiliated with Valve, Steam, or any of their partners.**


Description
-----------

*Nicely packed tools to work with Steam APIs*

* Steam library bindings for Python programming language.

  It allows your game to interact with features offered by Steam client and Steam platform.

* Tools for querying Steam Web resources.

  Allowing access to applications and market data from within your Python application.

* Command line utility.

  To reach and analyse publicly available applications and market information.


Steam API bindings example
--------------------------

A short example of API provided by Steam library, just to give a taste of it:

.. code-block:: python

    from steampak import SteamApi

    # A path to steam library file. This library should be provided with your game.
    # Library for various OS is distributed with Steam SDK available for Steam partners
    # at https://partner.steamgames.com/
    LIBRARY_PATH = '/home/me/my_steam_game/libsteam_api.so'

    # Your application (game) identifier provided by Steam.
    # Pass it as a parameter or put `steam_appid.txt` file with that ID in your game folder.
    APP_ID = 480  # We use `Spacewar` ID. (This game is provided with SDK).

    api = SteamApi(LIBRARY_PATH, app_id=APP_ID)

    # Let's print some friend names:
    for user in api.friends():
        print(user.name)

    # Current app achievements progress:
    for ach_name, ach in api.apps.current.achievements():
        print('%s (%s): %s' % (ach.title, ach_name, ach.get_unlock_info()))

    # Do not forget to shutdown when done:
    api.shutdown()


Command line client example
---------------------------

.. code-block:: bash

    ; Get prices and simple analysis for Half-Life 2 cards.
    $ steampak app 220 get_card_prices --currency USD

    ; Get `Gordon Freeman` card price.
    $ steampak market item 220 "Gordon Freeman" get_price --currency GBP

    ; Get games owned by `idlesign`.
    $ steampak user idlesign get_games


Use ``--help`` command option to get more information on available commands.


Steam API bindings roadmap
--------------------------

**Work in progress. Callback-based functions support is not implemented.**

* **Implemented (may be partially)**

    * Applications
    * Installed applications (restricted interface)
    * Friends
    * Friend tags
    * Groups
    * Current user
    * Users
    * Utilities
    * Achievements

* **Not [yet]**

    * Controller
    * HTML Surface
    * HTTP
    * Inventory
    * Matchmaking
    * Music
    * Networking
    * Screenshots
    * Servers
    * Storage
    * UGC
    * Video


Documentation
-------------

http://steampak.readthedocs.org/
