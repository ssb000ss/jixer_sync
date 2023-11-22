import base64
import math
from urllib.parse import urljoin

from typing import List, Tuple, Any
from .base import BaseEngine


class ShodanEngine(BaseEngine):
    def __init__(self, api_key: str):
        """
        Initializes the ShodanEngine object.

        Args:
            api_key (str): Client's API key.
        """
        super().__init__(api_key)
        self.PARAMS['key'] = self.api_key
        self.BASE_URL = 'https://api.shodan.io/shodan/host/'
        self.COUNT_ENDPOINT = urljoin(self.BASE_URL, 'count')
        self.SEARCH_ENDPOINT = urljoin(self.BASE_URL, 'search')
        self._QUERY_KWORD = 'query'
        self._COUNT_KWORD = 'total'
        self._TOTAL_ITEMS_KWORD = 'matches'

    def parse_ip_str(self, results: List[dict[str, Any]]) -> set[str]:
        """
        Parse the results and return a set of IP addresses.

        Args:
            results (List[Dict[str, Any]]): The list of results.

        Returns:
            Set[str]: The set of IP addresses.
        """
        return set([_.get('ip_str') for _ in results])

    def __str__(self) -> str:
        return 'shodan'


class NetlasEngine(BaseEngine):
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.BASE_URL = 'https://app.netlas.io/api/'
        self.COUNT_ENDPOINT = urljoin(self.BASE_URL, 'responses_count')
        self.SEARCH_ENDPOINT = urljoin(self.BASE_URL, 'responses')
        self.HEADERS['X-API-Key'] = self.api_key
        self.RESULTS_PER_PAGE = 20
        self.PARAMS = {
            'source_type': 'include',
            'fields': 'ip',
        }
        self._IP_KWORD = 'ip'
        self._COUNT_KWORD = 'count'
        self._PAGE_KWORD = 'start'
        self._QUERY_KWORD = 'q'
        self._TOTAL_ITEMS_KWORD = 'items'

    def page_iterator(self, total_count: int) -> range:
        """Create a generator for iterating over pages."""
        total_page = math.ceil(total_count / self.RESULTS_PER_PAGE)
        return range(0, min(total_page, self.MAX_PAGES_COUNT) * self.RESULTS_PER_PAGE, self.RESULTS_PER_PAGE)

    def parse_ip_str(self, results: List[dict[str, Any]]) -> set[str]:
        """
        Parse the results and return a set of IP addresses.

        Args:
            results (List[Dict[str, Any]]): The list of results.

        Returns:
            Set[str]: The set of IP addresses.
        """
        return set([_.get('data').get('ip') for _ in results])

    def __str__(self) -> str:
        return 'netlas'


class ZoomeyeEngine(BaseEngine):
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.BASE_URL = 'https://api.zoomeye.org/host/'
        self.COUNT_ENDPOINT = urljoin(self.BASE_URL, 'search')
        self.SEARCH_ENDPOINT = urljoin(self.BASE_URL, 'search')
        self.HEADERS['API-KEY'] = self.api_key
        self._IP_KWORD = 'ip'
        self._COUNT_KWORD = 'total'
        self._QUERY_KWORD = 'query'
        self._RESULTS_PER_PAGE = 20
        self._TOTAL_ITEMS_KWORD = 'matches'

    def parse_ip_str(self, results: List[dict[str, Any]]) -> set[str]:
        """
        Parse the results and return a set of IP addresses.

        Args:
            results (List[Dict[str, Any]]): The list of results.

        Returns:
            Set[str]: The set of IP addresses.
        """
        return set([_.get('ip') for _ in results])

    def __str__(self) -> str:
        return 'zoomeye'


class FofaEngine(BaseEngine):
    def __init__(self, api_key: str, email: str):
        """
        Initializes the FofaEngine object.

        Args:
            api_key (str): Client's API key.
            email (str): Client's email address.
        """
        super().__init__(api_key)
        self.BASE_URL = 'https://fofa.info/api/v1/'
        self.COUNT_ENDPOINT = urljoin(self.BASE_URL, 'search/all')
        self.SEARCH_ENDPOINT = urljoin(self.BASE_URL, 'search/all')
        self.RESULTS_PER_PAGE = 1000
        self._COUNT_KWORD = 'size'
        self._QUERY_KWORD = 'qbase64'
        self._TOTAL_ITEMS_KWORD = 'results'
        self.PARAMS = {
            'email': email,
            'key': self.api_key,
            'size': self.RESULTS_PER_PAGE
        }

    def get_query(self, query: str) -> str:
        """
        Return the Base64 encoded query string.

        Args:
            query (str): The query string.

        Returns:
            str: The Base64 encoded query string.
        """
        return self.query_to_bs64(query)

    @staticmethod
    def query_to_bs64(query_str: str) -> str:
        """
        Encodes a query string in Base64 format.

        Args:
            query_str (str): The query string to encode.

        Returns:
            str: The encoded string in Base64 format.
        """
        encoded_query = query_str.encode()
        encoded_query = base64.b64encode(encoded_query)
        return encoded_query.decode()

    def parse_ip_str(self, results: List[Tuple[Any]]) -> set[str]:
        """
        Parse the results and return a set of IP addresses.

        Args:
            results (List[Tuple[Any]]): The list of results.

        Returns:
            Set[str]: The set of IP addresses.
        """
        return set([_[1] for _ in results])

    def __str__(self) -> str:
        return 'fofa'
