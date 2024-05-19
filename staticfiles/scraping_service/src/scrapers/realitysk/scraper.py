import math
import platform
from datetime import datetime, date

import requests
from bs4 import BeautifulSoup

if platform.system() == 'Windows':
    from staticfiles.scraping_service.src.constants import ScrapeType, ScrapeDuration
    from staticfiles.scraping_service.src.utils.db.db_manager import DBManager
    from staticfiles.scraping_service.src.utils.helpers.helper import find_element_with_value
    from staticfiles.scraping_service.src.utils.logger import logger
elif platform.system() == 'Linux':
    from src.constants import ScrapeType, ScrapeDuration
    from src.utils.db.db_manager import DBManager
    from src.utils.helpers.helper import find_element_with_value
    from src.utils.logger import logger


class RealityScraper:
    """
    A class for scraping real estate data from reality.sk website.
    """

    def __init__(self, location: str, db_file_path: str):
        """
        Initialize the RealityScraper.

        Parameters:
        - location (str): The location for which real estate data will be scraped.
        - db_file_path (str): The path to the SQLite database file for storing the scraped data.
        """
        self.base_url = "https://www.reality.sk"
        self.location = location
        self.location_url = self.base_url + "/" + self.location
        self.page_url = f"{self.location_url}/?page="
        self.district = self.location_url.split("/")[3]
        self.db_file_path = db_file_path
        self.scrape_type = ScrapeType.EXTENDED
        self.db_manager = DBManager(self.db_file_path)

    def set_location(self, new_location: str):
        """
        Set a new location for scraping.

        Parameters:
        - new_location (str): The new location for which real estate data will be scraped.
        """
        self.location = new_location
        self.location_url = "https://www.reality.sk/" + new_location
        self.page_url = f"{self.location_url}/?page="
        self.district = self.location_url.split("/")[3]

    def get_location(self):
        """
        Gets the current location where the service is scraping data.
        """
        return self.location

    def set_scrape_type(self, scrape_type: ScrapeType):
        """
        Set a new scrape type for scraping.

        Parameters:
        - scrape_type (ScrapeType): The new ScrapeType to determine how much data to scrape from offer.
        """
        self.scrape_type = scrape_type

    def get_scrape_type(self):
        """
        Gets a new scrape type for scraping.
        """
        return self.scrape_type

    def is_scraping_supported(self):
        """
        Detects whether the scraping is still supported
        """
        try:
            if self.scrape_one_record(save_data=False):
                return True
            else:
                return False
        except():
            return False

    def scrape_all_records(self, save_data=True):
        """
        Scrape all real estate records.

        Parameters:
        - save_data (Boolean): This parameter determines whether the scraped data should be inserted directly into the database or returned.
        """
        return self._scrape_records(ScrapeDuration.ALL, save_data)

    def scrape_today_records(self, save_data=True):
        """
        Scrape real estate records posted today.

        Parameters:
        - save_data (Boolean): This parameter determines whether the scraped data should be inserted directly into the database or returned.
        """
        return self._scrape_records(ScrapeDuration.TODAY, save_data)

    def scrape_one_record(self, save_data=True):
        """
        Scrape one real estate record.

        Parameters:
        - save_data (Boolean): This parameter determines whether the scraped data should be inserted directly into the database or returned.
        """
        return self._scrape_records(ScrapeDuration.ONERECORD, save_data)

    def _scrape_records(self, scrape_duration: ScrapeDuration, save_data=True):
        """
        Scrape real estate records based on the specified duration and save them to the database.

        Parameters:
        - scrape_duration (ScrapeDuration): The duration for which records should be scraped.
        - save_data (Boolean): This parameter determines whether the scraped data should be inserted directly into the database or returned.
        """
        logger.log_info(f'Starting to scrape data in location {self.location_url}')
        scraped_data = []
        today = date.today().strftime("%d.%m.%Y")
        offers_not_posted_today = 0

        try:
            for page in range(1, self._get_number_of_pages() + 1):
                logger.log_info(f"{self.page_url}{page}")
                page_response = requests.get(f"{self.page_url}{page}")

                page_soup = BeautifulSoup(page_response.content, "html.parser")

                offers = page_soup.findAll("div", class_="offer-item-in")

                for offer in offers:
                    title_elem = offer.find("h2")
                    if title_elem is not None and title_elem != -1:
                        # Prepare variables
                        all_data = title_elem.find_parent("div")
                        general_data = all_data.find("div")
                        type_street_size_data = general_data.find("p")

                        # Title
                        title = title_elem["title"]

                        # City
                        city_elem = general_data.find("a")
                        city = city_elem.get_text(strip=True).replace("Reality ", "") if city_elem else ''

                        # Type
                        type_elem = type_street_size_data.findAll("span")[0]
                        type = type_elem.get_text(strip=True).replace("|", "").strip() if type_elem else ''

                        # Street
                        street_elem = type_street_size_data.findAll("span")[1]
                        street = street_elem.get_text(strip=True).replace("|", "").replace("Ulica", "").strip() if street_elem else ''

                        # Size
                        size_elem = type_street_size_data.findAll("span")[2]
                        usable_area = size_elem.get_text(strip=True).replace("|", "").strip() if size_elem else ''

                        # Short description
                        description_element = all_data.find("p")
                        short_description = description_element.get_text(strip=True) if description_element else ''

                        # Offer dates
                        published_date_elem = all_data.findAll("div")[1]
                        published_date = published_date_elem.find("span").get_text(strip=True).replace("Publikované: ","").strip() if published_date_elem else ''

                        if offers_not_posted_today >= 10 or page >= 10:
                            return scraped_data

                        if scrape_duration == ScrapeDuration.TODAY and published_date != today:
                            offers_not_posted_today += 1
                            continue

                        # Price
                        price_elem = all_data.findAll("div")[2].find("div").find("p")
                        if price_elem.small:
                            price_elem.small.decompose()
                        preprocessed_price = price_elem.get_text(strip=True).replace('\xa0', '').replace("€", "").replace("/m2", "").replace("/mesiac", "").replace(" ", "").strip()
                        price = preprocessed_price if preprocessed_price.isdigit() else 0

                        # URL
                        url_elem = title_elem.find_parent("a")
                        url = url_elem["href"]

                        if self.scrape_type == ScrapeType.EXTENDED:
                            print(f"{self.base_url}{url}")
                            offer_response = requests.get(f"{self.base_url}{url}")
                            offer_soup = BeautifulSoup(offer_response.content, "html.parser")

                            # Prepare variables
                            offer_info_elem = offer_soup.find('div', id='page-info').findParent("div").findAll("div")[1].find("div").find("div")

                            # Offer type
                            offer_type_elem = find_element_with_value(offer_info_elem, "div", "Typ:")
                            offer_type = offer_type_elem.find_next("div").get_text(strip=True) if offer_type_elem else ''

                            # Heating
                            heating_elem = find_element_with_value(offer_info_elem, "div", "Vykurovanie:")
                            heating = heating_elem.find_next("div").get_text(strip=True) if heating_elem else ''

                            # Land area
                            land_area_elem = find_element_with_value(offer_info_elem, "div", "Úžitková plocha:")
                            land_area = land_area_elem.find_next("div").get_text(strip=True) if land_area_elem else ''

                            # Property condition
                            property_condition_elem = find_element_with_value(offer_info_elem, "div", "Stav nehnuteľnosti:")
                            property_condition = property_condition_elem.find_next("div").get_text(strip=True) if property_condition_elem else ''

                            # Ownership
                            ownership_elem = find_element_with_value(offer_info_elem, "div", "Vlastníctvo:")
                            ownership = ownership_elem.find_next("div").get_text(strip=True) if ownership_elem else ''

                            # Year of construction
                            year_of_construction_elem = find_element_with_value(offer_info_elem, "div", "Rok výstavby:")
                            year_of_construction = year_of_construction_elem.find_next("div").get_text(strip=True) if year_of_construction_elem else ''

                            # Number of rooms
                            number_of_rooms_elem = find_element_with_value(offer_info_elem, "div", "Počet izieb / miestností:")
                            number_of_rooms = number_of_rooms_elem.find_next("div").get_text(strip=True) if number_of_rooms_elem else ''

                            # Basement
                            basement_elem = find_element_with_value(offer_info_elem, "div", "Podpivničenie:")
                            basement = basement_elem.find_next("div").get_text(strip=True) if basement_elem else ''

                            # Access communication
                            access_communication_elem = find_element_with_value(offer_info_elem, "div", "Prístupová komunikácia:")
                            access_communication = access_communication_elem.find_next("div").get_text(strip=True) if access_communication_elem else ''

                            # Facilities
                            facilities_elem = find_element_with_value(offer_info_elem, "div", "Vybavenie:")
                            facilities = facilities_elem.find_next("div").get_text(strip=True) if facilities_elem else ''

                            # Telecommunications
                            telecommunications_elem = find_element_with_value(offer_info_elem, "div", "Telekomunikácie:")
                            telecommunications = telecommunications_elem.find_next("div").get_text(strip=True) if telecommunications_elem else ''

                            # Leisure activities
                            leisure_activities_elem = find_element_with_value(offer_info_elem, "div", "Voľnočasové aktivity:")
                            leisure_activities = leisure_activities_elem.find_next("div").get_text(strip=True) if leisure_activities_elem else ''

                            # Long description
                            long_description_elem = \
                            find_element_with_value(offer_info_elem, "span", "Info").findParent("div").findParent("div").findAll("div")[1].find("span")
                            long_description = long_description_elem.get_text(strip=True) if long_description_elem and long_description_elem != -1 else ''

                            data_entry = {
                                "website": "realitysk",
                                "title": title,
                                "district": self.district,
                                "city": city,
                                "street": street,
                                "type": type,
                                "offer_type": offer_type,
                                "land_area": land_area,
                                "price": price,
                                "ownership": ownership,
                                "property_condition": property_condition,
                                "year_of_construction": year_of_construction,
                                "number_of_rooms": number_of_rooms,
                                "heating": heating,
                                "basement": basement,
                                "access_communication": access_communication,
                                "facilities": facilities,
                                "telecommunications": telecommunications,
                                "leisure_activities": leisure_activities,
                                "date_posted": published_date,
                                "short_description": short_description,
                                "long_description": long_description,
                                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "url": self.base_url + url
                            }
                        else:
                            data_entry = {
                                "website": "realitysk",
                                "title": title,
                                "district": self.district,
                                "city": city,
                                "street": street,
                                "type": type,
                                "usable_area": usable_area,
                                "price": price,
                                "date_posted": published_date,
                                "short_description": short_description,
                                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "url": self.base_url + url
                            }

                        logger.log_info(data_entry)
                        if save_data:
                            self.db_manager.insert_data_into_db(data_entry)
                        else:
                            scraped_data.append(data_entry)

                        if scrape_duration == ScrapeDuration.ONERECORD:
                            return scraped_data

            return scraped_data
        except Exception as e:
            logger.log_error(f'Failed to scrape records: {str(e)}')
            raise Exception(f'Failed to scrape records: {str(e)}')

    def _get_number_of_pages(self):
        """
        Get the total number of pages for scraping.

        Returns:
        - int: The total number of pages.
        """
        # Make a GET request to the website
        response = requests.get(self.location_url)

        # Create a BeautifulSoup object to parse the HTML content
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the number of offers
        no_of_offers = soup.find("h1", class_="page-title").find_parent("div").find("div")
        no_of_offers = no_of_offers.get_text().replace(" ", "")
        no_of_offers = ''.join(map(str, [int(i) for i in no_of_offers if i.isdigit()]))

        # Calculate the number of pages
        return math.ceil(int(no_of_offers) / 24)
