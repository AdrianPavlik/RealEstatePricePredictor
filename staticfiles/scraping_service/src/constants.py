from enum import Enum

SCRAPER_VERSION = '1.0.0'
SCRAPING_CONTROLLER_PORT = 8088
REALITY_SCRAPING_CONTROLLER_PORT = 8081
DEFAULT_SCRAPING_INTERVAL_HOURS = 1
ALLOWED_SCRAPING_INTERVAL_HOURS = [1, 2, 3, 4, 5, 6, 12, 24, 48]


class ScrapeDuration(Enum):
    TODAY = 'today'
    ALL = 'all'
    ONERECORD = 'onerecord'


class ScrapeType(Enum):
    BASIC = 'basic'
    EXTENDED = 'extended'


class RealitySKScrapeEndpoints(Enum):
    SCRAPE_ALL = str(f'http://localhost:{REALITY_SCRAPING_CONTROLLER_PORT}/reality/scraper/scrape/all')
    SCRAPE_TODAY = str(f'http://localhost:{REALITY_SCRAPING_CONTROLLER_PORT}/reality/scraper/scrape/today')
    SCRAPE_ONE_RECORD = str(f'http://localhost:{REALITY_SCRAPING_CONTROLLER_PORT}/reality/scraper/scrape/one_record')
    LOCATION = str(f'http://localhost:{REALITY_SCRAPING_CONTROLLER_PORT}/reality/scraper/location')
    SCRAPE_TYPE = str(f'http://localhost:{REALITY_SCRAPING_CONTROLLER_PORT}/reality/scraper/scrape_type')
    IS_SUPPORTED = str(f'http://localhost:{REALITY_SCRAPING_CONTROLLER_PORT}/reality/scraper/is_supported')
    IS_SCRAPING_IN_PROGRESS = str(f'http://localhost:{REALITY_SCRAPING_CONTROLLER_PORT}/reality/scraping/status')
