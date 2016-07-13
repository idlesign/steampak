import click
from operator import itemgetter
from functools import partial

from steampak import VERSION
from .webapi.settings import CURRENCIES, CURRENCY_RUB
from .webapi.resources.user import User
from .webapi.resources.apps import Application
from .webapi.resources.market import Item, TAG_ITEM_CLASS_BOOSTER


opt_currency = partial(
    click.option, '--currency',
    help='Currency ISO code. Default: %s. Variants: %s. ' % (CURRENCIES[CURRENCY_RUB], ', '.join(CURRENCIES.values())),
    default=CURRENCIES[CURRENCY_RUB])


def print_card_prices(appid, currency, detailed=True):

    app = Application(appid)

    click.secho('Card prices for `%s` [appid: %s]' % (app.title, appid), fg='green')

    cards, booster = app.get_cards()

    cards_total = len(cards)
    prices = []

    if not cards_total:
        click.secho('This app has no cards.', fg='red', err=True)
        return

    def get_line(card):
        card.get_price_data(currency)
        return '%s: %s %s' % (card.title, card.price_lowest, card.price_currency)

    for card in cards.values():
        detailed and click.echo(get_line(card))
        prices.append(card.price_lowest)

    avg_card = round(sum(prices) / cards_total, 2)
    avg_3cards = avg_card * 3

    click.secho('* Total cards: %d' % len(cards), fg='green')

    click.secho('* Avg 1 card: %s' % avg_card, fg='blue')
    click.secho('* Avg 3 cards: %s' % avg_3cards, fg='blue')

    if booster:
        click.secho('* Booster price: %s' % get_line(booster), fg='yellow')


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
@opt_currency()
@click.pass_context
def get_price(ctx, currency):
    """Prints out market item price."""
    appid = ctx.obj['appid']
    title = ctx.obj['title']

    item_ = Item(appid, title)
    item_.get_price_data(currency)

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
        click.secho('This app has no cards.', fg='red', err=True)
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
@opt_currency()
@click.pass_context
def get_card_prices(ctx, currency):
    """Prints out lowest card prices for an application.
    Comma-separated list of application IDs is supported.

    """
    appid = ctx.obj['appid']

    detailed = True

    appids = [appid]
    if ',' in appid:
        appids = [appid.strip() for appid in appid.split(',')]
        detailed = False

    for appid in appids:
        print_card_prices(appid, currency, detailed=detailed)
        click.echo('')


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


@user.command()
@opt_currency()
@click.pass_context
def get_booster_stats(ctx, currency):
    """Prints out price stats for booster packs available in Steam user inventory."""

    username = ctx.obj['username']

    inventory = User(username)._get_inventory_raw()
    boosters = {}
    for item in inventory['rgDescriptions'].values():

        is_booster = False
        tags = item['tags']
        for tag in tags:
            if tag['internal_name'] == TAG_ITEM_CLASS_BOOSTER:
                is_booster = True
                break

        if not is_booster:
            continue

        appid = item['app_data']['appid']
        title = item['name']

        boosters[appid] = title

    if not boosters:
        click.secho('User `%s` has no booster packs' % username, fg='red', err=True)
        return

    for appid, title in boosters.items():
        click.secho('Found booster: `%s`' % title, fg='blue')
        print_card_prices(appid, currency)


def main():
    start(obj={})
