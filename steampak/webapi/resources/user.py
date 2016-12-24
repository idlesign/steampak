from ..settings import URL_COMMUNITY_BASE, APPID_STEAM
from ..utils import str_sub, DataFetcher
from ..exceptions import ResponseError
from .market import Item, Card, TAG_ITEM_CLASS_CARD


URL_USER_BASE = URL_COMMUNITY_BASE + '/id/$username'
URL_USER_INVENTORY_PUBLIC_BASE = URL_USER_BASE + '/inventory/json/'
URL_USER_INVENTORY_PUBLIC_APP = URL_USER_INVENTORY_PUBLIC_BASE + '$appid/6'
URL_USER_INVENTORY_PUBLIC_STEAM = str_sub(URL_USER_INVENTORY_PUBLIC_APP, appid=APPID_STEAM)
URL_USER_GAMES_OWNED = URL_USER_BASE + '/games/?xml=1'

INV_CLASSID_GEM = '667924416'


class User(object):

    def __init__(self, username):
        self.username = username
        self._intentory_raw = None

    def _get_inventory_raw(self):
        url = str_sub(URL_USER_INVENTORY_PUBLIC_STEAM, username=self.username)

        response = DataFetcher(url).fetch_json()
        if not response:
            raise ResponseError('No response', url)

        if not response['success']:
            raise ResponseError(response['Error'], url)

        self._intentory_raw = response

        return response

    def traverse_inventory(self, item_filter=None):
        """Generates market Item objects for each inventory item.

        :param str item_filter: See `TAG_ITEM_CLASS_` contants from .market module.

        """
        not self._intentory_raw and self._get_inventory_raw()

        for item in self._intentory_raw['rgDescriptions'].values():
            tags = item['tags']
            for tag in tags:
                internal_name = tag['internal_name']
                if item_filter is None or internal_name == item_filter:

                    item_type = Item
                    if internal_name == TAG_ITEM_CLASS_CARD:
                        item_type = Card

                    appid = item['market_fee_app']
                    title = item['name']

                    yield item_type(appid, title)

    @property
    def gems_total(self):
        not self._intentory_raw and self._get_inventory_raw()

        items = self._intentory_raw['rgInventory']
        return sum([int(item['amount']) for item in items.values() if item['classid'] == INV_CLASSID_GEM])

    def get_games_owned(self):
        url = str_sub(URL_USER_GAMES_OWNED, username=self.username)
        xml = DataFetcher(url).fetch_xml()

        games = {}
        for el in xml:
            if el.tag == 'games':
                for game in el:
                    props = {}

                    for prop in game:
                        if prop.tag == 'appID':
                            props['appid'] = prop.text

                        elif prop.tag == 'name':
                            props['title'] = prop.text

                    games[props['appid']] = props

        return games
