import logging
import math
import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry
from typing import List, Tuple, Any, Dict


class BaseEngine:
    def __init__(self, api_key: str):
        """Initialize the BaseEngine with common parameters and configurations.

        Args:
            api_key (str): The API key for authentication.
        """
        self.MAX_RETRY_ATTEMPTS: int = 10
        self.RESULTS_PER_PAGE: int = 100
        self.MAX_PAGES_COUNT: int = 2500
        self.BASE_URL: str = ''
        self.COUNT_ENDPOINT: str = ''
        self.SEARCH_ENDPOINT: str = ''
        self.PARAMS: Dict[str, Any] = {}
        self.HEADERS: Dict[str, str] = {}
        self._TOTAL_ITEMS_KWORD: str = ''
        self._PAGE_KWORD: str = 'page'
        self._QUERY_KWORD: str = ''
        self._COUNT_KWORD: str = ''
        self._IP_KWORD: str = ''
        self.api_key: str = api_key
        self.session: requests.Session = requests.Session()
        self.configure_session()
        self.logger: logging.Logger = logging.getLogger(__name__)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.session.close()

    def configure_session(self):
        """Configure the session with retry strategy for HTTP requests."""
        retry_strategy = Retry(
            total=5,
            backoff_factor=2,
            status_forcelist=[500, 502, 503, 504]
        )
        self.session.mount('https://', HTTPAdapter(max_retries=retry_strategy))

    def get_query(self, query: str) -> str:
        """Return the processed query.

        Args:
            query (str): The input query.

        Returns:
            str: The processed query.
        """
        return query

    def prepare_request_list(self, query: str, total_count: int) -> List[requests.PreparedRequest]:
        """Create a list of prepared requests using all pages.

        Args:
            query (str): The search query.
            total_count (int): The total count of items.

        Returns:
            List[requests.PreparedRequest]: List of prepared requests.
        """
        params = self.PARAMS.copy()
        params[self._QUERY_KWORD] = self.get_query(query)
        request_list = []
        page_iterator = self.page_iterator(total_count)
        for page in page_iterator:
            params = params.copy()
            params.update({self._PAGE_KWORD: page})
            prepared_request = requests.Request(
                method='GET',
                url=self.SEARCH_ENDPOINT,
                params=params,
                headers=self.HEADERS
            ).prepare()
            request_list.append(prepared_request)
        return request_list

    def parse_ip_str(self, results: List[Any]) -> List[Tuple[str, str]]:
        """Parse the results and return a list of tuples (ip, domain).

        Args:
            results (List[Any]): The list of results.

        Returns:
            List[Tuple[str, str]]: The list of tuples (ip, domain).
        """
        raise NotImplementedError

    def get_total_count(self, query: str) -> int:
        """Get the total count of results for a given query.

        Args:
            query (str): The search query.

        Returns:
            int: The total count of results.
        """
        params = self.PARAMS.copy()
        params[self._QUERY_KWORD] = self.get_query(query)

        with self.session as s:
            try:
                self.logger.info(f'Getting the number of servers for query: {query}')
                response = s.get(
                    self.COUNT_ENDPOINT,
                    params=params,
                    headers=self.HEADERS
                )
                response.raise_for_status()
                total_count = response.json()[self._COUNT_KWORD]
                self.logger.info(f'{total_count} servers have been received for this request')
                return total_count
            except requests.RequestException as e:
                self.logger.error(f"HTTP error occurred: {e}")
            return 0

    def page_iterator(self, total_count: int) -> range:
        """Create a generator for iterating over pages.

        Args:
            total_count (int): The total count of items.

        Returns:
            range: A range generator for pages.
        """
        total_page = math.ceil(total_count / self.RESULTS_PER_PAGE)
        return range(1, min(total_page, self.MAX_PAGES_COUNT) + 1)

    def _fetch_all(self, query: str) -> List[Any]:
        """Fetch all results for a given query.

        Args:
            query (str): The search query.

        Returns:
            List[Any]: The list of results.
        """
        total_count = self.get_total_count(query)
        if total_count == 0:
            return []
        responses = []
        pages = self.prepare_request_list(query, total_count)
        with self.session as s:
            for count, page in enumerate(pages, start=1):
                self.logger.info(f'Getting page {count} out of {len(pages)} for query: {query[:100]}')
                try:
                    response = s.send(page)
                    response.raise_for_status()
                    result = response.json()[self._TOTAL_ITEMS_KWORD]
                    if result:
                        responses.extend(result)
                except requests.RequestException as e:
                    self.logger.error(f"HTTP error occurred: {e}")
        return responses

    def fetch_ip_str(self, query: str) -> List[Tuple[str, str]]:
        """Fetch and return the sorted list of IP addresses.

        Args:
            query (str): The search query.

        Returns:
            List[Tuple[str, str]]: The sorted list of IP addresses.
        """
        responses = self._fetch_all(query)
        results = self.parse_ip_str(responses)
        return results
