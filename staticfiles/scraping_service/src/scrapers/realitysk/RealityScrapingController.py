import json
import platform
from abc import ABC

import tornado
from tornado import web

from staticfiles.scraping_service.src.constants import ScrapeType, REALITY_SCRAPING_CONTROLLER_PORT
from staticfiles.scraping_service.src.scrapers.realitysk import scraper
from staticfiles.scraping_service.src.utils.helpers.helper import get_db_file_path, validate_request_parameters
from staticfiles.scraping_service.src.utils.logger import logger
from staticfiles.scraping_service.src.utils.messages import info, error

db_file_path = get_db_file_path()
realityskscraper = scraper.RealityScraper("kosice", db_file_path)


class RealityScrapeAllRecords(tornado.web.RequestHandler, ABC):
    def post(self):
        try:
            realityskscraper.scrape_all_records()
            info.raise_default_info(
                self,
                f'All records were scraped and stored into database.'
            )
        except Exception as e:
            error.raise_default_error(
                self,
                f'There was an error scraping all records: {str(e)}'
            )


class RealityScrapeTodayRecords(tornado.web.RequestHandler, ABC):
    def post(self):
        try:
            realityskscraper.scrape_today_records()
            info.raise_default_info(
                self,
                f'Today records were scraped and stored into database.'
            )
        except Exception as e:
            error.raise_default_error(
                self,
                f'There was an error scraping today records: {str(e)}'
            )


class RealityScrapeOneRecord(tornado.web.RequestHandler, ABC):
    def post(self):
        try:
            realityskscraper.scrape_one_record()
            info.raise_default_info(
                self,
                f'One record was scraped and stored into database.'
            )
        except Exception as e:
            error.raise_default_error(
                self,
                f'There was an error scraping one record: {str(e)}'
            )


class RealityLocation(tornado.web.RequestHandler, ABC):
    def post(self):
        try:
            request_body = json.loads(self.request.body)
            if not validate_request_parameters(self, request_body, ['location']):
                return
            location = request_body.get('location')
            realityskscraper.set_location(location)
            info.raise_default_info(
                self,
                f'Scraping location was changed to {location}.'
            )
        except Exception as e:
            error.raise_default_error(
                self,
                f'Error setting new location: {e}.'
            )

    def get(self):
        current_location = realityskscraper.get_location()
        info.raise_default_info(
            self,
            f'{current_location}'
        )


class RealityScrapeType(tornado.web.RequestHandler, ABC):
    def post(self):
        try:
            request_body = json.loads(self.request.body)
            if not validate_request_parameters(self, request_body, ['scrape_type']):
                return
            scrape_type = request_body.get('scrape_type')
            realityskscraper.set_scrape_type(ScrapeType(scrape_type))
            info.raise_default_info(
                self,
                f'Scrape type was changed to {scrape_type}.'
            )
        except Exception as e:
            error.raise_default_error(
                self,
                f'Error setting new scrape type: {e}.'
            )

    def get(self):
        current_scrape_type = realityskscraper.get_scrape_type().name
        info.raise_default_info(
            self,
            f'{current_scrape_type}'
        )


class RealityIsScrapingSupported(tornado.web.RequestHandler, ABC):
    def get(self):
        is_supported = realityskscraper.is_scraping_supported()
        info.raise_default_info(
            self,
            is_supported
        )


class RealityScrapingStatus(tornado.web.RequestHandler, ABC):
    def get(self):
        info.raise_default_info(
            self,
            False
        )


def make_app():
    return tornado.web.Application([
        (r"/reality/scraper/scrape/all", RealityScrapeAllRecords),
        (r"/reality/scraper/scrape/today", RealityScrapeTodayRecords),
        (r"/reality/scraper/scrape/one_record", RealityScrapeOneRecord),
        (r"/reality/scraper/location", RealityLocation),
        (r"/reality/scraper/scrape_type", RealityScrapeType),
        (r"/reality/scraper/is_supported", RealityIsScrapingSupported),
        (r"/reality/scraping/status", RealityScrapingStatus),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(REALITY_SCRAPING_CONTROLLER_PORT)
    logger.log_info("Reality scraping controller is now running...")
    tornado.ioloop.IOLoop.current().start()
