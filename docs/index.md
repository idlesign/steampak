# steampak

<https://github.com/idlesign/steampak>

**This software is not affiliated with Valve, Steam, or any of their partners.**

## Description

*Nicely packed tools to work with Steam APIs*

* Steam library bindings for Python programming language.

  It allows your game to interact with features offered by Steam client and Steam platform.

* Tools for querying Steam Web resources.

  Allowing access to applications and market data from within your Python application.

* Command line utility.

  To reach and analyse publicly available applications and market information.

## Requirements

* Python 3.10+
* Steam API library from Steamworks SDK (e.g. `libsteam_api.so`).

    !!! note

        Tested version — 1.42: <https://partner.steamgames.com/downloads/steamworks_sdk_142.zip> (login required)

* Linux (not tested with libraries for OSX or Windows)

## Optional dependencies

To install all dependencies for `steampak`:

```shell
$ pip install steampak[extra]
```

* `requests`, `BeautifulSoup` (for Web API related stuff)
* `click` (for CLI)

## Get involved into steampak

**Submit issues.** If you spotted something weird in application behavior or want to propose a feature you can do that at <https://github.com/idlesign/steampak/issues>

**Write code.** If you are eager to participate in application development, fork it at <https://github.com/idlesign/steampak>, write your code, whether it should be a bugfix or a feature implementation, and make a pull request right from the forked project page.

**Spread the word.** If you have some tips and tricks or any other words in mind that you think might be of interest for the others — publish them.
