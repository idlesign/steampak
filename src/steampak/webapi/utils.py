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


class DataFetcher(object):

    def __init__(self, url, params=None):
        self.url = url
        self.params = params

    def fetch_data(self, req_timeout=0):

        if req_timeout:
            sleep(req_timeout)

        LOGGER.debug('Fetching data from %s ...', self.url)

        response = requests.get(self.url, self.params, headers={
            'User-Agent': 'Valve/Steam HTTP Client 1.0 (tenfoot)',
        })
        response.encoding = 'utf-8'

        if response.status_code == 429:  # 429 Too Many Requests
            pause_sec = 60
            LOGGER.debug('Request limit hit for %s. Waiting for %d seconds ...', self.url, pause_sec)
            response = self.fetch_data(pause_sec)

        return response

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
