from ..settings import URL_COMMUNITY_BASE, APPID_STEAM
from ..utils import str_sub, DataFetcher
from ..exceptions import ResponseError


URL_USER_BASE = URL_COMMUNITY_BASE + '/id/$username'
URL_USER_INVENTORY_PUBLIC_BASE = URL_USER_BASE + '/inventory/json/'
URL_USER_INVENTORY_PUBLIC_APP = URL_USER_INVENTORY_PUBLIC_BASE + '$appid/6'
URL_USER_INVENTORY_PUBLIC_STEAM = str_sub(URL_USER_INVENTORY_PUBLIC_APP, appid=APPID_STEAM)
URL_USER_GAMES_OWNED = URL_USER_BASE + '/games/?xml=1'

INV_CLASSID_GEM = '667924416'


class User(object):

    def __init__(self, username):
        self.username = username

    def _get_inventory_raw(self):
        url = str_sub(URL_USER_INVENTORY_PUBLIC_STEAM, username=self.username)

        response = DataFetcher(url).fetch_json()
        if not response['success']:
            raise ResponseError(response['Error'], url)

        return response

    @property
    def gems_total(self):
        items = self._get_inventory_raw()['rgInventory']
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
