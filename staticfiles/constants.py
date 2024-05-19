from enum import Enum

SCRAPING_SERVICE_NAME = "RealEstateScrapingService"


class ScrapeDuration(Enum):
    TODAY = 'today'
    ALL = 'all'
    ONERECORD = 'onerecord'
