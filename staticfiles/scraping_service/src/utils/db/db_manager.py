import platform
import sqlite3

if platform.system() == 'Windows':
    from staticfiles.scraping_service.src.utils.db.preprocess_offer import preprocess_property
    from staticfiles.scraping_service.src.utils.logger import logger
elif platform.system() == 'Linux':
    from src.utils.db.preprocess_offer import preprocess_property
    from src.utils.logger import logger

class DBManager:
    def __init__(self, db_file_path):
        self.db_file_path = db_file_path

    def init_db(self):
        logger.log_info(f'Initializing Database at {self.db_file_path}...')
        with sqlite3.connect(self.db_file_path) as conn:
            cursor = conn.cursor()

            # Create a table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS properties (
                    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    "website" TEXT,
                    "title" TEXT UNIQUE,
                    "district" TEXT,
                    "city" TEXT,
                    "street" TEXT,
                    "type" TEXT,
                    "offer_type" TEXT,
                    "land_area" TEXT,
                    "price" TEXT,
                    "ownership" TEXT,
                    "property_condition" TEXT,
                    "year_of_construction" TEXT,
                    "number_of_rooms" INTEGER,
                    "lift" INTEGER,
                    "parking_space" INTEGER,
                    "basement" INTEGER,
                    "gazebo" INTEGER,
                    "terrace" INTEGER,
                    "pool" INTEGER,
                    "air_conditioning" INTEGER,
                    "sauna" INTEGER,
                    "balcony" INTEGER,
                    "garage" INTEGER,
                    "loggia" INTEGER,
                    "garden" INTEGER,
                    "fireplace" INTEGER,
                    "bathroom" INTEGER,
                    "new_building" INTEGER,
                    "latitude" NUMERIC,
                    "longitude" NUMERIC,
                    "date_posted" TEXT,
                    "short_description" TEXT,
                    "long_description" TEXT,
                    "timestamp" TEXT,
                    "url" TEXT UNIQUE
                )
            ''')

    def insert_data_into_db(self, data):
        with sqlite3.connect(self.db_file_path) as conn:
            cursor = conn.cursor()
            try:
                refactored_offer = preprocess_property(data)
                logger.log_info(f'Inserting record into database {refactored_offer}')
                cursor.execute('''
                    INSERT OR IGNORE INTO properties (
                        website, title, district, city, street, type, offer_type, land_area, price, ownership,
                        property_condition, year_of_construction, number_of_rooms, lift, parking_space, basement,
                        gazebo, terrace, pool, air_conditioning, sauna, balcony, garage, loggia, garden, fireplace,
                        bathroom, new_building, latitude, longitude, date_posted, short_description, long_description,
                        timestamp, url
                    ) VALUES (
                        :website, :title, :district, :city, :street, :type, :offer_type, :land_area, :price, :ownership,
                        :property_condition, :year_of_construction, :number_of_rooms, :lift, :parking_space, :basement,
                        :gazebo, :terrace, :pool, :air_conditioning, :sauna, :balcony, :garage, :loggia, :garden, :fireplace,
                        :bathroom, :new_building, :latitude, :longitude, :date_posted, :short_description, :long_description,
                        :timestamp, :url
                    )
                ''', refactored_offer)
            except sqlite3.OperationalError as msg:
                print(msg)
