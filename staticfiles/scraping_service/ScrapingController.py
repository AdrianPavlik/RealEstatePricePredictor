import json
import platform
from abc import ABC

import tornado
from tornado import web

if platform.system() == 'Windows':
    from staticfiles.scraping_service.src.constants import ScrapeDuration, DEFAULT_SCRAPING_INTERVAL_HOURS, \
        SCRAPING_CONTROLLER_PORT, REALITY_SCRAPING_CONTROLLER_PORT, SCRAPER_VERSION, RealitySKScrapeEndpoints, \
        ALLOWED_SCRAPING_INTERVAL_HOURS
    from staticfiles.scraping_service.src.utils.db.db_manager import DBManager
    from staticfiles.scraping_service.src.utils.helpers.helper import get_db_file_path, \
        ScrapeAtInterval, validate_request_parameters, call_api_endpoint, is_location_supported
    from staticfiles.scraping_service.src.utils.logger import logger
    from staticfiles.scraping_service.src.utils.messages import info, error, success
elif platform.system() == 'Linux':
    from src.constants import ScrapeDuration, DEFAULT_SCRAPING_INTERVAL_HOURS, \
        SCRAPING_CONTROLLER_PORT, REALITY_SCRAPING_CONTROLLER_PORT, SCRAPER_VERSION, RealitySKScrapeEndpoints, \
        ALLOWED_SCRAPING_INTERVAL_HOURS
    from src.utils.db.db_manager import DBManager
    from src.utils.helpers.helper import get_db_file_path, \
        ScrapeAtInterval, validate_request_parameters, call_api_endpoint, is_location_supported
    from src.utils.logger import logger
    from src.utils.messages import info, error,  success


db_manager = DBManager(get_db_file_path())

scrape_at_interval = ScrapeAtInterval(
    DEFAULT_SCRAPING_INTERVAL_HOURS,
    [f'http://localhost:{REALITY_SCRAPING_CONTROLLER_PORT}/reality/scraper/scrape/today']
)

reality_scraping_in_progress = False


class ScrapingServiceAbout(tornado.web.RequestHandler, ABC):
    def get(self):
        logger.log_info(f'Service is running on version {SCRAPER_VERSION}')
        info.raise_default_info(
            self,
            f'v.{SCRAPER_VERSION}'
        )


class ScrapingServiceStatus(tornado.web.RequestHandler, ABC):
    def get(self):
        logger.log_info(f'Scraping service running.')
        info.raise_default_info(self, True)


class ScrapingServiceScrape(tornado.web.RequestHandler, ABC):
    async def post(self):
        global reality_scraping_in_progress
        try:
            request_body = json.loads(self.request.body)
            if not validate_request_parameters(self, request_body, ['scrape_duration']):
                logger.log_error(f'Request parameters not supported.')
                error.raise_default_error(
                    self,
                    f'Request parameters not supported.'
                )
            scrape_duration = request_body.get('scrape_duration')
            print(scrape_duration)

            if scrape_duration:
                response = None
                if scrape_duration in [e.value for e in ScrapeDuration]:
                    if scrape_duration == ScrapeDuration.TODAY.value:
                        logger.log_info('Scraping all records from present day...')
                        reality_scraping_in_progress = True
                        response = await call_api_endpoint(self, RealitySKScrapeEndpoints.SCRAPE_TODAY.value, 'POST')
                    elif scrape_duration == ScrapeDuration.ALL.value:
                        logger.log_info('Scraping all records...')
                        reality_scraping_in_progress = True
                        response = await call_api_endpoint(self, RealitySKScrapeEndpoints.SCRAPE_ALL.value, 'POST')
                    elif scrape_duration == ScrapeDuration.ONERECORD.value:
                        logger.log_info('Scraping one record...')
                        reality_scraping_in_progress = True
                        response = await call_api_endpoint(self, RealitySKScrapeEndpoints.SCRAPE_ONE_RECORD.value, 'POST')

                    if 'error' not in response:
                        logger.log_info('Scraping finished and data were stored.')
                        success.raise_default_success(
                            self,
                            'Scraping finished and data were stored.'
                        )
                    else:
                        logger.log_info('Scraping error')
                        error.raise_default_error(
                            self,
                            'Scraping error.'
                        )
                    reality_scraping_in_progress = False
                else:
                    custom_errors = {'supported_types': ScrapeDuration}
                    logger.log_error('Scrape duration parameter type is not supported.')
                    error.raise_custom_error(
                        self,
                        'Scrape duration parameter type is not supported.',
                        custom_errors
                    )
            else:
                logger.log_error('Scrape duration parameter not provided.')
                error.raise_default_error(
                    self,
                    'Scrape duration parameter not provided.'
                )

        except Exception as e:
            reality_scraping_in_progress = False
            logger.log_error(f'Scraping error: {e}')
            error.raise_default_error(
                self,
                f'Scraping error: {e}'
            )


class ScrapingServiceScrapeStatus(tornado.web.RequestHandler, ABC):
    def get(self):
        global reality_scraping_in_progress
        try:
            custom_info = {
                'nehnutelnostisk_scraping_in_progress': {'info': False},
                'realitysk_scraping_in_progress': {'info': reality_scraping_in_progress},
                'toprealitysk_scraping_in_progress': {'info': False}
            }

            info.raise_custom_info(
                self,
                f'Scraping status:',
                custom_info
            )
        except Exception as e:
            logger.log_error(f'Scraping status error: {e}')
            error.raise_default_error(
                self,
                f'Scraping status error: {e}'
            )


class ScrapingServiceScrapeInterval(tornado.web.RequestHandler, ABC):
    def post(self):
        try:
            request_body = json.loads(self.request.body)
            if not validate_request_parameters(self, request_body, ['interval_hours']):
                logger.log_error(f'Request parameters not supported.')
                error.raise_default_error(
                    self,
                    f'Request parameters not supported.'
                )
            interval = int(request_body.get('interval_hours'))

            logger.log_info(interval in ALLOWED_SCRAPING_INTERVAL_HOURS)

            if interval in ALLOWED_SCRAPING_INTERVAL_HOURS:
                scrape_at_interval.set_interval(interval)
                logger.log_info(f'Scraping interval set to {interval} hours.')
                success.raise_default_success(
                    self,
                    f'{interval} hours',
                )
            else:
                custom_errors = {'supported_scraping_interval_hours': ALLOWED_SCRAPING_INTERVAL_HOURS}
                logger.log_error(f'Interval of {interval} hours is not allowed. {custom_errors}')
                error.raise_custom_error(
                    self,
                    f'Interval of {interval} hours is not allowed.',
                    custom_errors
                )

        except Exception as e:
            logger.log_error(f'Interval error: {e}')
            error.raise_default_error(
                self,
                f'Interval error: {e}'
            )

    def get(self):
        logger.log_info(f'Scraping interval is set to {scrape_at_interval.interval} hours.')
        info.raise_default_info(
            self,
            f'Scraping interval is set to {scrape_at_interval.interval} hours.'
        )


class ScrapingServiceScrapeLocation(tornado.web.RequestHandler, ABC):
    async def post(self):
        logger.log_info(f'Setting scrape location.')
        try:
            request_body = json.loads(self.request.body)
            if not validate_request_parameters(self, request_body, ['nehnutelnostisk_location', 'realitysk_location', 'toprealitysk_location']):
                logger.log_error(f'Request parameters not supported.')
                error.raise_default_error(
                    self,
                    f'Request parameters not supported.'
                )
            realitysk_location = request_body.get('realitysk_location')

            if realitysk_location:
                if not is_location_supported(self, realitysk_location):
                    logger.log_error(f'Location {realitysk_location} is not supported. Supported locations can be found at http://localhost:{SCRAPING_CONTROLLER_PORT}/service/scrape/supported/locations')
                    error.raise_default_error(
                        self,
                        f'Location {realitysk_location} is not supported. Supported locations can be found at http://localhost:{SCRAPING_CONTROLLER_PORT}/service/scrape/supported/locations'
                    )
                await call_api_endpoint(self, RealitySKScrapeEndpoints.LOCATION.value, 'POST', {'location': realitysk_location})
                logger.log_info(f'Scraping location set to {realitysk_location}.')
                success.raise_default_success(
                    self,
                    f'Scraping location set to {realitysk_location}.'
                )
            else:
                logger.log_error('Location parameter not provided.')
                error.raise_default_error(
                    self,
                    'Location parameter not provided.'
                )

        except Exception as e:
            logger.log_error(f'Location error: {e}')
            error.raise_default_error(
                self,
                f'Location error: {e}'
            )

    async def get(self):
        realitysk_scraping_location = await call_api_endpoint(self, RealitySKScrapeEndpoints.LOCATION.value, 'GET')
        scraping_locations = {
            'nehnutelnostisk_scraping_location': 'ERROR',
            'realitysk_scraping_location': realitysk_scraping_location,
            'toprealitysk_scraping_location': 'ERROR'
        }
        logger.log_info(f'Scraping locations: {scraping_locations}')
        info.raise_custom_info(
            self,
            f'Scraping locations.',
            scraping_locations
        )


class ScrapingServiceScrapeSupportedLocations(tornado.web.RequestHandler, ABC):
    def get(self):
        loader = tornado.template.Loader("templates")
        html_content = loader.load("supported_locations.html").generate()
        self.write(html_content)


class ScrapingServiceScrapeSupport(tornado.web.RequestHandler, ABC):
    async def get(self):
        supported_websites = {
            'nehnutelnostisk_support': {'info': False},
            'realitysk_support': await call_api_endpoint(self, RealitySKScrapeEndpoints.IS_SUPPORTED.value, 'GET'),
            'toprealitysk_support': {'info': False},
        }
        logger.log_info(f'Supported websites for scraping: {supported_websites}')
        info.raise_custom_info(
            self,
            'Supported scraping websites.',
            supported_websites
        )


def make_app():
    return tornado.web.Application([
        (r'/service/about', ScrapingServiceAbout),
        (r'/service/status', ScrapingServiceStatus),
        (r'/service/scrape', ScrapingServiceScrape),
        (r'/service/scrape/status', ScrapingServiceScrapeStatus),
        (r'/service/scrape/interval', ScrapingServiceScrapeInterval),
        (r'/service/scrape/location', ScrapingServiceScrapeLocation),
        (r'/service/scrape/supported/locations', ScrapingServiceScrapeSupportedLocations),
        (r'/service/scrape/support', ScrapingServiceScrapeSupport),
    ])


if __name__ == '__main__':
    app = make_app()
    app.listen(SCRAPING_CONTROLLER_PORT)
    db_manager.init_db()
    logger.log_info('Scraping controller is now running...')
    scrape_at_interval.start()
    tornado.ioloop.IOLoop.current().start()
