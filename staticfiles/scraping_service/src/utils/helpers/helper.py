import json
import os
import platform
from tornado.httpclient import AsyncHTTPClient, HTTPRequest, HTTPError
import tornado

if platform.system() == 'Windows':
    from staticfiles.scraping_service.src.utils.helpers.json_district_cities_loader import get_cities
    from staticfiles.scraping_service.src.constants import SCRAPING_CONTROLLER_PORT
    from staticfiles.scraping_service.src.utils.logger import logger
    from staticfiles.scraping_service.src.utils.messages import error
elif platform.system() == 'Linux':
    from src.utils.helpers.json_district_cities_loader import get_cities
    from src.constants import SCRAPING_CONTROLLER_PORT
    from src.utils.logger import logger
    from src.utils.messages import error


def get_db_file_path():
    system = platform.system()
    if system == "Windows":
        return os.path.join(f"C:\\Users\\blued\\AppData\\Roaming", "RealEstateWebScraper", "database.db")
    elif system == "Linux":
        return os.path.join("/home", "scraping-control", "RealEstateWebScraper", "database.db")
    else:
        raise NotImplementedError("Unsupported operating system.")


async def call_api_endpoint(handler, endpoint: str, method: str, data=None, timeout=None):
    http_client = AsyncHTTPClient()
    try:
        headers = {'Content-Type': 'application/json'}
        body = json.dumps(data) if data is not None else json.dumps({})

        if method.upper() == 'GET':
            request = HTTPRequest(endpoint, method='GET', headers=headers, request_timeout=timeout)
        elif method.upper() == 'POST':
            request = HTTPRequest(endpoint, method='POST', headers=headers, body=body, request_timeout=timeout)
        else:
            logger.log_error('Invalid HTTP method. Supported methods are GET and POST.')
            raise ValueError('Invalid HTTP method. Supported methods are GET and POST.')

        response = await http_client.fetch(request)

        if response.code == 200:
            logger.log_info(f'API endpoint {endpoint} called successfully.')
            return json.loads(response.body.decode())
        else:
            logger.log_error(f'Failed to call API endpoint {endpoint}. Status code: {response.code}')
            return {'error': f'Failed to call API endpoint. Status code: {response.code}'}

    except HTTPError as e:
        logger.log_error(f'HTTP error occurred while calling API endpoint {endpoint}: {str(e)}')
        error.raise_default_error(handler, f'HTTP error occurred while calling API endpoint {endpoint}: {str(e)}')
        return {'error': f'HTTP error occurred: {str(e)}'}
    except Exception as e:
        logger.log_error(f'An error occurred while calling API endpoint {endpoint}: {str(e)}')
        error.raise_default_error(handler, f'An error occurred while calling API endpoint {endpoint}: {str(e)}')
        return {'error': f'An error occurred: {str(e)}'}


def validate_request_parameters(handler, request_body: dict, allowed_parameters: list):
    if len(request_body) != len(allowed_parameters) or not all(param in request_body for param in allowed_parameters):
        error.raise_default_error(
            handler,
            f'Invalid JSON body. Only \"{", ".join(allowed_parameters)}\" parameter(s) are allowed.'
        )
        return False
    return True


class ScrapeAtInterval:
    def __init__(self, initial_interval_hours, endpoints):
        self._interval_milliseconds = int(initial_interval_hours * 60 * 60 * 1000)  # Convert hours to milliseconds
        self.endpoints = endpoints
        self.scheduler = tornado.ioloop.PeriodicCallback(self.task, self._interval_milliseconds)
        self.is_running = False

    def start(self):
        self.scheduler.start()

    def stop(self):
        self.scheduler.stop()

    def set_interval(self, new_interval_hours):
        self._interval_milliseconds = int(new_interval_hours * 60 * 60 * 1000)  # Convert hours to milliseconds
        if self.is_running:
            self.stop()
            self.start()

    @property
    def interval(self):
        return int(self._interval_milliseconds / 1000 / 60 / 60)  # Convert milliseconds to hours

    async def task(self):
        self.is_running = True
        logger.log_info(f"Scraping at {self.interval} hour interval...")
        for endpoint in self.endpoints:
            await call_api_endpoint(self, endpoint, "POST")
        self.is_running = False


def find_element_with_value(container, tag_name, value, exact_value=True):
    """
    Find an HTML element within a container whose text content matches the specified value and tag name.

    Parameters:
    - container (BeautifulSoup Tag): The container element within which to search.
    - tag_name (str): The tag name to search for (e.g., 'div', 'span').
    - value (str): The value to search for in the text content of elements within the container.
    - exact_value (bool): If the search should be for exact value or the string should contain the value.

    Returns:
    - BeautifulSoup Tag or None: The first element found with text content matching the specified value and tag name, or None if not found.
    """

    # Define a function to traverse through elements recursively
    def find_element_recursive(tag):
        if not exact_value:
            if tag.name == tag_name and value in tag.get_text(strip=True):
                return tag
        else:
            if tag.name == tag_name and tag.get_text(strip=True) == value:
                return tag

        # Recursively search through children elements
        for child in tag.children:
            if isinstance(child, str):  # Check if child is a string
                continue  # Skip strings
            result = find_element_recursive(child)
            if result:
                return result

        return None  # Return None if value not found

    # Start searching from the container element
    return find_element_recursive(container)


def is_location_supported(handler, location):
    cities_data = get_cities()

    for region_name, cities in cities_data.items():
        if any(city['realityskurl'] == location or
               city['nehnutelnostiskurl'] == location or
               city['toprealityskurl'] == location for city in cities):
            return True

    error.raise_default_error(
        handler,
        f'Location {location} is not supported. Supported locations can be found at http://localhost:{SCRAPING_CONTROLLER_PORT}/service/scrape/supported/locations'
    )
    return False

