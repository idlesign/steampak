from collections import OrderedDict
from operator import attrgetter

from ..settings import URL_COMMUNITY_BASE, URL_STORE_API_BASE, APPID_CARDS, APP_CATEGORY_CARDS
from ..utils import str_sub, DataFetcher

from .market import TAG_ITEM_CLASS_CARD, TAG_CARDBORDER_NORMAL, TAG_CARDBORDER_FOIL


URL_GAMECARDS = (
    URL_COMMUNITY_BASE +
    '/market/search/render/?'
    'category_' + APPID_CARDS + '_Game[]=tag_app_$appid&'
    '$cardboarder&'
    'category_' + APPID_CARDS + '_item_class[]=tag_' + TAG_ITEM_CLASS_CARD + '&'
    'appid=' + APPID_CARDS)

URL_STORE_APP_DETAILS = URL_STORE_API_BASE + '/appdetails?appids=$appid'


def get_filter_cardborder(*cardborder_type):
    """Returns game cards URL filter for a given cardborder
    type (TAG_CARDBORDER_NORMAL / TAG_CARDBORDER_FOIL).

    To be used in URL_GAMECARDS.

    :param str|unicode cardborder_type:
    :rtype: str|unicode
    """
    filter_ = []

    for type_ in cardborder_type:
        if not type_:
            continue
        filter_.append('category_' + APPID_CARDS + '_cardborder[]=tag_' + type_)

    return '&'.join(filter_)


class Application(object):

    def __init__(self, appid):
        self.appid = appid
        self._data_raw = {}

    def _get_data_raw(self):
        url = str_sub(URL_STORE_APP_DETAILS, appid=self.appid)
        response = DataFetcher(url).fetch_json()
        data = response[self.appid]

        if not data['success']:
            return {}

        data = data['data']
        self._data_raw = data
        return data

    @property
    def has_cards(self):
        not self._data_raw and self._get_data_raw()
        for category in self._data_raw['categories']:
            if category['id'] == APP_CATEGORY_CARDS:
                return True
        return False

    @property
    def title(self):
        not self._data_raw and self._get_data_raw()
        return self._data_raw.get('name', '<unresolved %s>' % self.appid)

    def get_cards(self, normal=True, foil=False):
        from .market import Card

        url = str_sub(
            URL_GAMECARDS,
            appid=self.appid,
            cardboarder=get_filter_cardborder(
                normal and TAG_CARDBORDER_NORMAL,
                foil and TAG_CARDBORDER_FOIL))

        data = DataFetcher(url).fetch_json()
        soup = DataFetcher.get_soup(data['results_html'])

        rows = soup.select('.market_listing_row_link')
        cards = []

        for row in rows:
            name = row.select('.market_listing_item_name')[0].text
            cards.append(Card(self, name))

        cards = OrderedDict(
            [(card.market_hash, card) for card in sorted(cards, key=attrgetter('title'))])

        booster = Card.get_booster(self) if cards else None

        return cards, booster
