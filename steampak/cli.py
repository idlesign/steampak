import click
from operator import itemgetter

from steampak import VERSION
from .webapi.resources.user import User
from .webapi.resources.apps import Application
from .webapi.resources.market import Item


@click.group()
@click.version_option(version='.'.join(map(str, VERSION)))
def start():
    """Steampak command line utilities."""


@start.group()
def market():
    """Market-related commands."""


@market.group()
@click.argument('appid')
@click.argument('title')
@click.pass_context
def item(ctx, appid, title):
    """Market-related commands."""
    ctx.obj['appid'] = appid
    ctx.obj['title'] = title


@item.command()
@click.pass_context
def get_price(ctx):
    """Prints out market item price."""
    appid = ctx.obj['appid']
    title = ctx.obj['title']

    item_ = Item(appid, title)

    click.secho('Lowest price: %s %s' % (item_.price_lowest, item_.price_currency), fg='green')


@start.group()
@click.argument('appid')
@click.pass_context
def app(ctx, appid):
    """Application-related commands."""
    ctx.obj['appid'] = appid


@app.command()
@click.pass_context
def get_cards(ctx):
    """Prints out cards available for application."""

    appid = ctx.obj['appid']
    app = Application(appid)

    click.secho('Cards for `%s` [appid: %s]' % (app.title, appid), fg='green')

    if not app.has_cards:
        click.secho('This app has no cards', fg='red', err=True)
        return

    cards, booster = app.get_cards()

    def get_line(card):
        return '%s [market hash: `%s`]' % (card.title, card.market_hash)

    for card in cards.values():
        click.echo(get_line(card))

    if booster:
        click.secho('* Booster pack: `%s`' % get_line(booster), fg='yellow')

    click.secho('* Total cards: %d' % len(cards), fg='green')


@app.command()
@click.pass_context
def get_card_prices(ctx):
    """Prints out lowest card prices for an application."""

    appid = ctx.obj['appid']
    app = Application(appid)

    click.secho('Card prices for `%s` [appid: %s]' % (app.title, appid), fg='green')

    cards, booster = app.get_cards()

    cards_total = len(cards)
    prices = []

    def get_line(card):
        return '%s: %s %s' % (card.title, card.price_lowest, card.price_currency)

    for card in cards.values():
        click.echo(get_line(card))
        prices.append(card.price_lowest)

    avg_card = sum(prices) / cards_total
    avg_booster = avg_card * 3

    click.secho('* Total cards: %d' % len(cards), fg='green')

    click.secho('* Avg 1 card: %s' % avg_card, fg='blue')
    click.secho('* Avg 3 cards: %s' % avg_booster, fg='blue')

    if booster:
        click.secho('* Booster price: %s' % get_line(booster), fg='yellow')


@start.group()
@click.argument('username')
@click.pass_context
def user(ctx, username):
    """User-related commands."""
    ctx.obj['username'] = username


@user.command()
@click.pass_context
def get_gems(ctx):
    """Prints out total gems count for a Steam user."""

    username = ctx.obj['username']
    click.secho(
        'Total gems owned by `%s`: %d' % (username, User(username).gems_total),
        fg='green')


@user.command()
@click.pass_context
def get_games(ctx):
    """Prints out games owned by a Steam user."""

    username = ctx.obj['username']
    games = User(username).get_games_owned()

    for game in sorted(games.values(), key=itemgetter('title')):
        click.echo('%s [appid: %s]' % (game['title'], game['appid']))

    click.secho('Total gems owned by `%s`: %d' % (username, len(games)), fg='green')


def main():
    start(obj={})
