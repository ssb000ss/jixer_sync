# Jixer - sync IP Search Engine

A Python library for seamless querying of Shodan, Netlas, Zoomeye, and Fofa IP search engines. Simplify IP address information retrieval and integrate easily into applications.

## Installation

Install the IP Search Engine library using `pip`:

```bash
pip install jixer-sync
```

## Usage

```python
from jixer-sync import BaseEngine, ShodanEngine, NetlasEngine

# Example usage of BaseEngine
with BaseEngine(api_key='your_api_key') as engine:
    results = engine.fetch_ip_str(query='your_search_query')
    print(results)

# Example usage of ShodanEngine
with ShodanEngine(api_key='your_shodan_api_key') as engine:
    results = engine.fetch_ip_str(query='your_search_query')
    print(results)

# Example usage of NetlasEngine
with NetlasEngine(api_key='your_netlas_api_key') as engine:
    results = engine.fetch_ip_str(query='your_search_query')
    print(results)
```

For detailed information on configuration and supported engines, refer to the documentation.

## Configuration

The library provides configuration options for each supported engine. Set up API keys, customize search queries, and adjust parameters as needed.

## Supported Engines

- **ShodanEngine**: Queries Shodan IP search engine.
- **NetlasEngine**: Queries Netlas IP search engine.
- **ZoomeyeEngine**: Queries Zoomeye IP search engine.
- **FofaEngine**: Queries Fofa IP search engine.

## Credits

This library relies on the [Requests](https://docs.python-requests.org/en/latest/) library for making HTTP requests.

## License

This project is licensed under the [MIT License](LICENSE).

## Issues

Report issues or suggestions on the [GitHub repository](https://github.com/ssb000ss/jixer-sync).

## Changelog

- **Version 1.0.0** (2023-11-22): Initial release.

## Acknowledgments

Special thanks to the developers of Shodan, Netlas, Zoomeye, and Fofa for providing access to their IP search services.

## Contact

For support or collaboration, contact via email at [ssb000ss@gmail.com](mailto:ssb000ss@gmail.com).
