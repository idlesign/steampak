steampak documentation
======================
https://github.com/idlesign/steampak

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


Requirements
------------

* Python 3.6+
* Steam API library from Steamworks SDK (e.g. ``libsteam_api.so``).

    .. note:: Tested version - 1.42: https://partner.steamgames.com/downloads/steamworks_sdk_142.zip (login required)

* Linux (not tested with libraries for OSX or Windows)

Optional dependencies
---------------------

To install all dependencies for `steampak`::

  > pip install steampak[extra]

* `requests`, `BeautifulSoup` (for Web API related stuff)
* `click` (for CLI)


Table of Contents
-----------------

.. toctree::
    :maxdepth: 2

    quickstart
    libsteam_api
    libsteam_apps
    libsteam_friends
    libsteam_groups
    libsteam_stats
    libsteam_user
    libsteam_utils
    libsteam_overlay
    libsteam_screenshots

