from decimal import Decimal

from ..settings import CURRENCY_RUB, URL_COMMUNITY_BASE, APPID_CARDS, CURRENCIES
from ..utils import DataFetcher


URL_PRICE_OVERVIEW = URL_COMMUNITY_BASE + '/market/priceoverview/'


_REQ_TIMEOUT = 60
_REQ_MAX = 20
_REQ_COUNTER = 0


class Item(object):

    def __init__(self, app, title):
        from .apps import Application

        self.title = title
        self.app = app

        if not isinstance(app, Application):
            self.app = Application(app)

        self._price_data = None

    def get_price_data(self, currency=CURRENCY_RUB):
        url = URL_PRICE_OVERVIEW

        json = DataFetcher(url, params={
            'appid': APPID_CARDS,
            'currency': currency,
            'market_hash_name': self.market_hash
        }, fetch_limits=(20, 60)).fetch_json()

        def format_money(val):
            val = val.split(' ')[0].replace(',', '.')
            return Decimal(val)

        price_data = None
        if json['success']:

            price_data = json
            price_data['lowest_price'] = format_money(price_data['lowest_price'])
            price_data['median_price'] = format_money(price_data['median_price'])
            price_data['volume'] = int(price_data['volume'])
            price_data['currency'] = CURRENCIES[currency]

        self._price_data = price_data

        return price_data

    @property
    def price_lowest(self):
        not self._price_data and self.get_price_data()
        return self._price_data['lowest_price']

    @property
    def price_median(self):
        not self._price_data and self.get_price_data()
        return self._price_data['median_price']

    @property
    def price_currency(self):
        not self._price_data and self.get_price_data()
        return self._price_data['currency']

    @property
    def market_hash(self):
        return self.get_market_hash(self.app.appid, self.title)

    @classmethod
    def get_market_hash(cls, appid, title):
        return '%s-%s' % (appid, title)


class Card(Item):

    @classmethod
    def get_booster(cls, app):
        from .apps import Application

        if not isinstance(app, Application):
            app = Application(app)

        booster_title = '%s Booster Pack' % app.title

        return Card(app, booster_title)
