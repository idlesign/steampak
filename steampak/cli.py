import click
from operator import itemgetter
from functools import partial
from collections import defaultdict

from steampak import VERSION
from .webapi.settings import CURRENCIES, CURRENCY_RUB
from .webapi.resources.user import User
from .webapi.resources.apps import Application
from .webapi.resources.market import Item, TAG_ITEM_CLASS_BOOSTER, TAG_ITEM_CLASS_CARD


opt_currency = partial(
    click.option, '--currency',
    help='Currency ISO code. Default: %s. Variants: %s. ' % (CURRENCIES[CURRENCY_RUB], ', '.join(CURRENCIES.values())),
    default=CURRENCIES[CURRENCY_RUB])


def print_card_prices(appid, currency, detailed=True, owned_cards=None):

    owned_cards = owned_cards or []

    app = Application(appid)

    click.secho('Card prices for `%s` [appid: %s]' % (app.title, appid), fg='green')

    cards, booster = app.get_cards()

    price_cards_owned = 0
    price_cards_wanted = 0
    count_cards_total = len(cards)
    prices = []

    if not count_cards_total:
        click.secho('This app has no cards.', fg='red', err=True)
        return

    def get_line(card):
        card.get_price_data(currency)
        return '%s: %s %s' % (card.title, card.price_lowest, card.price_currency)

    for card in cards.values():

        is_owned = card.title in owned_cards

        if detailed:
            prefix = ''
            fg = None

            if is_owned:
                prefix = 'OWNED  - '
                fg = 'magenta'

            elif owned_cards:
                prefix = 'WANTED - '

            click.secho('%s%s' % (prefix, get_line(card)), fg=fg)

        price = card.price_lowest
        prices.append(price)

        if is_owned:
            price_cards_owned += price
        else:
            price_cards_wanted += price

    price_1avg = round(sum(prices) / count_cards_total, 2)
    price_3avg = price_1avg * 3

    click.secho('* Total cards: %d' % count_cards_total, fg='green')

    if owned_cards:
        click.secho('* Owned cards: %d' % len(owned_cards), fg='green')
        click.secho('* Price cards owned: %s' % price_cards_owned, fg='blue')
        click.secho('* Price cards wanted: %s' % price_cards_wanted, fg='blue')

    click.secho('* Price avg 1 card: %s' % price_1avg, fg='blue')
    click.secho('* Price avg 3 cards: %s' % price_3avg, fg='blue')

    if booster:
        click.secho('* Booster price: %s' % get_line(booster), fg='yellow')

    click.echo('%s\n' % ('=' * 20))


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

        appid = item['market_fee_app']
        title = item['name']

        boosters[appid] = title

    if not boosters:
        click.secho('User `%s` has no booster packs' % username, fg='red', err=True)
        return

    for appid, title in boosters.items():
        click.secho('Found booster: `%s`' % title, fg='blue')
        print_card_prices(appid, currency)


@user.command()
@opt_currency()
@click.pass_context
def get_cards_stats(ctx, currency):
    """Prints out price stats for cards available in Steam user inventory."""

    username = ctx.obj['username']
    cards_by_app = defaultdict(list)

    inventory = User(username).traverse_inventory(item_filter=TAG_ITEM_CLASS_CARD)
    for item in inventory:
        appid = item.app.appid
        cards_by_app[appid].append(item)

    if not cards_by_app:
        click.secho('User `%s` has no cards' % username, fg='red', err=True)
        return

    for appid, cards in cards_by_app.items():
        app = cards[0].app
        print_card_prices(app.appid, currency, owned_cards=[card.title for card in cards])


def main():
    start(obj={})
