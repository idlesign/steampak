Quickstart
==========

Steam API example
-----------------

* First a path to steam library file. This library should be provided with your game.
  Library for various OS (`libsteam_api.so` or `steam_api.dll` or `libsteam_api.dylib`) is distributed
  with Steam SDK available for Steam partners at https://partner.steamgames.com/

* Second. Your need to know application (game) identifier provided by Steam.
  Pass it as a parameter or put `steam_appid.txt` file with that ID in your game folder.


Now you're ready to begin. API initialization is easy:

.. code-block:: python

    from steampak import SteamApi  # Main API entry point.

    LIBRARY_PATH = '/home/me/my_steam_game/libsteam_api.so'
    APP_ID = 480  # We use `Spacewar` ID. (This game is provided with SDK).

    api = SteamApi(LIBRARY_PATH, app_id=APP_ID)


After that you can access various API parts as `api` object attributes:

.. code-block:: python

    # Let's print some friend names:
    for user in api.friends():
        print(user.name)

    # Print out some info from utils:
    print(api.utils.country_code)
    print(api.utils.ui_language)

    # Achievements progress:
    for ach_name, ach in api.apps.current.achievements():
        print('%s (%s): %s' % (ach.title, ach_name, ach.get_unlock_info()))

    # Installed applications titles:
    for app_id, app in api.apps.installed():
        print('%s: %s' % (app_id, app.name))


When you're done, do not forget to shutdown API:

.. code-block:: python

    # Do not forget to shutdown when done:
    api.shutdown()


Command line interface example
------------------------------

.. code-block:: bash

    ; Get prices and simple analysis for Half-Life 2 cards.
    $ steampak app 220 get_card_prices --currency USD

    ; Get `Gordon Freeman` card price.
    $ steampak market item 220 "Gordon Freeman" get_price --currency GBP

    ; Get games owned by `idlesign`.
    $ steampak user idlesign get_games


Use ``--help`` command option to get more information on available commands.
