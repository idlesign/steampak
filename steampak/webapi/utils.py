import logging
from time import sleep
from xml.etree import ElementTree
from string import Template

import requests
from bs4 import BeautifulSoup


LOGGER = logging.getLogger(__name__)

# logging.basicConfig(level=logging.DEBUG)
# logging.getLogger('requests').setLevel(logging.ERROR)


def str_sub(string, **kwargs):
    tpl = Template(string)
    return tpl.safe_substitute(**kwargs)


_FETCHER_LIMITS = {}


class DataFetcher(object):

    def __init__(self, url, params=None, fetch_limits=None):
        self.url = url
        self.params = params
        self.fetch_limits = fetch_limits

    def fetch_data(self):

        limits = self.fetch_limits
        if limits:
            LOGGER.debug('Fetching limit %s imposed. Checking ...', limits)

            req_counter = _FETCHER_LIMITS.setdefault(limits, 0)
            req_max, req_timeout = limits

            if req_counter == req_max:
                LOGGER.debug('Fetching limit exceeded waiting %d seconds ...', req_timeout)

                sleep(req_timeout)
                _FETCHER_LIMITS[limits] = 0

            _FETCHER_LIMITS[limits] += 1

        LOGGER.debug('Fetching data from %s ...', self.url)
        return requests.get(self.url, self.params, headers={
            'User-Agent': 'Valve/Steam HTTP Client 1.0 (tenfoot)',
        })

    def fetch_json(self):
        json = self.fetch_data().json()
        return json

    def fetch_xml(self):
        data = self.fetch_data()
        xml = ElementTree.fromstring(data.text.encode('utf8'))
        return xml

    @classmethod
    def get_soup(cls, data):
        return BeautifulSoup(data, 'html5lib')
