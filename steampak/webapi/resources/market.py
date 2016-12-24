import re
from decimal import Decimal

from ..settings import CURRENCY_RUB, URL_COMMUNITY_BASE, APPID_CARDS, CURRENCIES
from ..utils import DataFetcher

RE_CURRENCY = re.compile(r'[^\d]*(\d+([.,]\d+)?)[^\d]*', re.U)

URL_PRICE_OVERVIEW = URL_COMMUNITY_BASE + '/market/priceoverview/'

# Below are `internal_name` values for tags:
# category: cardborder
TAG_CARDBORDER_NORMAL = 'cardborder_0'
TAG_CARDBORDER_FOIL = 'cardborder_1'
# category: item_class
TAG_ITEM_CLASS_CARD = 'item_class_2'
TAG_ITEM_CLASS_BACKGROUND = 'item_class_3'
TAG_ITEM_CLASS_EMOTICON = 'item_class_4'
TAG_ITEM_CLASS_BOOSTER = 'item_class_5'
TAG_ITEM_CLASS_GEM = 'item_class_7'


class Item(object):

    def __init__(self, app, title):
        from .apps import Application

        self.title = title
        self.app = app

        if not isinstance(app, Application):
            self.app = Application(app)

        self._price_data = {}

    def get_price_data(self, currency=CURRENCY_RUB):
        url = URL_PRICE_OVERVIEW

        if not isinstance(currency, int):
            # Consider ISO currency code.
            currency = {cur_code: cur_id for cur_id, cur_code in CURRENCIES.items()}.get(currency)

        json = DataFetcher(url, params={
            'appid': APPID_CARDS,
            'currency': currency,
            'market_hash_name': self.market_hash
        }, fetch_limits=(20, 60)).fetch_json()

        def format_money(val):
            match = RE_CURRENCY.search(val)
            if match:
                val = match.group(1)

            val = val.replace(',', '.')
            return Decimal(val)

        price_data = {}
        if json['success']:

            price_data = json
            price_data['lowest_price'] = format_money(price_data.get('lowest_price', '0'))
            price_data['median_price'] = format_money(price_data.get('median_price', '0'))
            price_data['volume'] = format_money(price_data.get('volume', '0'))
            price_data['currency'] = CURRENCIES[currency]

        self._price_data = price_data

        return price_data

    @property
    def price_lowest(self):
        not self._price_data and self.get_price_data()
        return self._price_data.get('lowest_price', 0)

    @property
    def price_median(self):
        not self._price_data and self.get_price_data()
        return self._price_data.get('median_price', 0)

    @property
    def price_currency(self):
        not self._price_data and self.get_price_data()
        return self._price_data.get('currency')

    @property
    def market_hash(self):
        return self.get_market_hash(self.app.appid, self.title)

    @classmethod
    def get_market_hash(cls, appid, title):
        # todo sometimes : is used in hash and shouldn't be stripped
        return '%s-%s' % (appid, title.replace('/', '-').replace(':', ''))


class Card(Item):

    @classmethod
    def get_booster(cls, app):
        from .apps import Application

        if not isinstance(app, Application):
            app = Application(app)

        booster_title = '%s Booster Pack' % app.title

        return Card(app, booster_title)
