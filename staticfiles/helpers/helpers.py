import datetime
import getpass
import json
import os.path
import platform
import sqlite3
from pathlib import Path

import joblib
import pandas as pd
import requests
from django.core.cache import cache

from staticfiles.constants import *

BASE_DIR = Path(__file__).resolve().parent.parent


def does_database_exist():
    """
    Checks if the database file exists.

    Returns:
    str/bool: Path to the database file if it exists, False otherwise.
    """
    db_path = get_db_file_path()
    if os.path.exists(db_path):
        return db_path
    else:
        return False


class Property:
    def __init__(self, id=None, website=None, title=None, district=None, city=None, street=None, type=None,
                 offer_type=None, land_area=None, price=None, ownership=None, property_condition=None,
                 year_of_construction=None, number_of_rooms=None, lift=None, parking_space=None, basement=None,
                 gazebo=None, terrace=None, pool=None, air_conditioning=None, sauna=None, balcony=None, garage=None,
                 loggia=None, garden=None, fireplace=None, bathroom=None, new_building=None, latitude=None,
                 longitude=None, date_posted=None, short_description=None, long_description=None, timestamp=None,
                 url=None):
        self.id = id
        self.website = website
        self.title = title
        self.district = district
        self.city = city
        self.street = street
        self.type = type
        self.offer_type = offer_type
        self.land_area = land_area
        self.price = price
        self.ownership = ownership
        self.property_condition = property_condition
        self.year_of_construction = year_of_construction
        self.number_of_rooms = number_of_rooms
        self.lift = lift
        self.parking_space = parking_space
        self.basement = basement
        self.gazebo = gazebo
        self.terrace = terrace
        self.pool = pool
        self.air_conditioning = air_conditioning
        self.sauna = sauna
        self.balcony = balcony
        self.garage = garage
        self.loggia = loggia
        self.garden = garden
        self.fireplace = fireplace
        self.bathroom = bathroom
        self.new_building = new_building
        self.latitude = latitude
        self.longitude = longitude
        self.date_posted = date_posted
        self.short_description = short_description
        self.long_description = long_description
        self.timestamp = timestamp
        self.url = url

    def to_dict(self):
        return {attr: getattr(self, attr) for attr in vars(self)}


def get_stored_data_from_database(to_dict=False):
    db = does_database_exist()

    if not db:
        return []

    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()

        # Select all data from the properties table
        cursor.execute('SELECT * FROM properties')
        data = cursor.fetchall()

    properties = []
    for row in data:
        if to_dict:
            prop = Property(*row).to_dict()
        else:
            prop = Property(*row)
        properties.append(prop)

    return properties


def get_db_file_path():
    system = platform.system()
    if system == 'Windows':
        return os.path.join(f'C:\\Users\\{getpass.getuser()}\\AppData\\Roaming', 'RealEstateWebScraper', 'database.db')
    elif system == 'Linux':
        return os.path.join(f'/home/{getpass.getuser()}', 'RealEstateWebScraper', 'database.db')
    else:
        raise NotImplementedError('Unsupported operating system')


def get_model_file_path(offer_type):
    system = platform.system()
    if system == 'Windows':
        if offer_type == 'Predaj':
            return os.path.join(f'C:\\Users\\{getpass.getuser()}\\AppData\\Roaming', 'RealEstateWebScraper', 'predaj_model.pkl')
        elif offer_type == 'Prenájom':
            return os.path.join(f'C:\\Users\\{getpass.getuser()}\\AppData\\Roaming', 'RealEstateWebScraper', 'prenajom_model.pkl')
    elif system == 'Linux':
        if offer_type == 'Predaj':
            return os.path.join(f'/home/{getpass.getuser()}', 'RealEstateWebScraper', 'predaj_model.pkl')
        elif offer_type == 'Prenájom':
            return os.path.join(f'/home/{getpass.getuser()}', 'RealEstateWebScraper', 'prenajom_model.pkl')
    else:
        raise NotImplementedError('Unsupported operating system')


def execute_sql_query(sql_query):
    """
    Executes a SQL query on a SQLite database and returns the results as a list of dictionaries.

    Args:
    sql_query (str): SQL query string to be executed.

    Returns:
    list: A list of dictionaries where each dictionary represents a property.
    """
    try:
        db = does_database_exist()

        if not db:
            return []
        with sqlite3.connect(db) as conn:
            cursor = conn.cursor()
            cursor.execute(sql_query)
            results = cursor.fetchall()
            properties = [Property(*row).to_dict() for row in results]

        return properties
    except sqlite3.Error as e:
        print(f"An error occurred while executing the SQL query: {e}")
        return None


def get_database_stats():
    properties = get_stored_data_from_database()

    if not properties:
        return {}

    min_date = datetime.datetime.max.date()
    max_date = datetime.datetime.min.date()
    unique_cities = set()
    unique_types = set()
    min_price = float('inf')
    max_price = float('-inf')
    city_locations = {}

    for prop in properties:
        try:
            date_posted = datetime.datetime.strptime(prop.date_posted, '%d.%m.%Y').date()
            min_date = min(min_date, date_posted)
            max_date = max(max_date, date_posted)
        except ValueError:
            print(f"Error parsing date for property ID {prop.id}: {prop.date_posted}")

        unique_cities.add(prop.city)
        unique_types.add(prop.type)

        try:
            price = int(prop.price) if prop.price is not None else None
            if price is not None:
                min_price = min(min_price, price)
                max_price = max(max_price, price)
        except ValueError:
            continue

        if prop.city not in city_locations:
            city_locations[prop.city] = {'latitude': prop.latitude, 'longitude': prop.longitude}
        else:
            existing = city_locations[prop.city]

            def safe_float(value):
                try:
                    return float(value)
                except (TypeError, ValueError):
                    return None

            existing_lat = safe_float(existing['latitude'])
            prop_lat = safe_float(prop.latitude)
            existing_lon = safe_float(existing['longitude'])
            prop_lon = safe_float(prop.longitude)

            if existing_lat is not None and prop_lat is not None:
                avg_latitude = (existing_lat + prop_lat) / 2
            else:
                avg_latitude = 0

            if existing_lon is not None and prop_lon is not None:
                avg_longitude = (existing_lon + prop_lon) / 2
            else:
                avg_longitude = 0

            city_locations[prop.city] = {
                'latitude': avg_latitude,
                'longitude': avg_longitude
            }

    return {
        'min_date': min_date.strftime('%Y-%m-%d'),
        'max_date': max_date.strftime('%Y-%m-%d'),
        'unique_cities': sorted(list(unique_cities)),
        'unique_types': sorted(list(unique_types)),
        'min_price': min_price if min_price != float('inf') else None,
        'max_price': max_price if max_price != float('-inf') else None,
        'city_locations': city_locations
    }


def load_json(file_path):
    with open(file_path, 'r', encoding='utf8') as json_file:
        return json.load(json_file)


def get_cities():
    regions_data = load_json(os.path.join(BASE_DIR, 'json/regions.json'))
    districts_data = load_json(os.path.join(BASE_DIR, 'json/districts.json'))

    region_districts_mapping = {}

    for district in districts_data:
        region_id = district['region_id']
        region_name = next((region['name'] for region in regions_data if region['id'] == region_id), 'Unknown Region')
        district_record = {
            'name': district['name'],
            'nehnutelnostiskurl': district['nehnutelnostiskurl'],
            'toprealityskurl': district['toprealityskurl'],
            'realityskurl': district['realityskurl']
        }

        region_districts_mapping.setdefault(region_name, []).append(district_record)

    for region_name, cities in region_districts_mapping.items():
        region_districts_mapping[region_name] = sorted(cities, key=lambda x: x['name'])

    return dict(sorted(region_districts_mapping.items()))


def is_scraping_service_running():
    scraping_service_status_url = 'http://localhost:8088/service/status'
    try:
        response = requests.get(scraping_service_status_url, timeout=0.1)
        response.raise_for_status()
        response_json = response.json()
        return response_json.get('info', False)
    except Exception as e:
        print(f'Failed to fetch scraping service status: {str(e)}')
        return False


def scraping_service_version():
    scraping_service_about_url = 'http://localhost:8088/service/about'
    try:
        response = requests.get(scraping_service_about_url, timeout=0.1)
        response.raise_for_status()
        response_json = response.json()
        return response_json.get('info', 'VERSION ERROR')
    except Exception as e:
        return {'error': f'Failed to fetch scraping service version: {str(e)}'}


def scraping_service_scrape_interval(interval=0):
    scraping_service_interval_url = 'http://localhost:8088/service/scrape/interval'
    try:
        if interval == 0:
            response = requests.get(scraping_service_interval_url, timeout=0.1)
            response.raise_for_status()
            response_json = response.json()
            return {
                'scraping_service_interval': response_json.get('info', 'INTERVAL ERROR')
            }
        else:
            data = {
                'interval_hours': interval,
            }
            response = requests.post(scraping_service_interval_url, json=data)
            response.raise_for_status()
            return {
                'scraping_service_interval': 'Scraping interval updated.'
            }
    except Exception as e:
        return {'error': f'Failed to fetch scraping interval: {str(e)}'}


def scraping_service_scrape_location(nehnutelnostisk_location='', toprealitysk_location='', realitysk_location=''):
    scraping_service_location_url = 'http://localhost:8088/service/scrape/location'
    try:
        if nehnutelnostisk_location == '' and toprealitysk_location == '' and realitysk_location == '':
            response = requests.get(scraping_service_location_url, timeout=0.1)
            response.raise_for_status()
            response_json = response.json()
            return {
                'nehnutelnostisk_location': 'LOCATION ERROR',
                'realitysk_location': response_json.get('other', {}).get('realitysk_scraping_location', {}).get('info',
                                                                                                                'LOCATION ERROR'),
                'toprealitysk_location': 'LOCATION ERROR'
            }
        else:
            data = {
                'realitysk_location': realitysk_location,
            }
            response = requests.post(scraping_service_location_url, json=data)
            response.raise_for_status()
            return {
                'scraping_service_location': 'Scraping location updated.'
            }
    except Exception as e:
        return {'error': f'Failed to fetch scraping location: {str(e)}'}


def scraping_service_supported_websites(force_update=False):
    scraping_service_location_url = 'http://localhost:8088/service/scrape/support'
    cached_supported_websites = cache.get('scraping_service_supported_websites')
    cache.delete('scraping_service_supported_websites_force_update')
    cache.set('scraping_service_supported_websites_force_update', force_update, 18000)
    if cached_supported_websites is not None and not force_update:
        return cached_supported_websites
    elif force_update:
        cache.delete('scraping_service_supported_websites')
    try:
        response = requests.get(scraping_service_location_url, timeout=10)
        response.raise_for_status()
        response_json = response.json()
        supported_websites = {
            'nehnutelnostisk_support': response_json.get('other', {}).get('nehnutelnostisk_support', {}).get('info',
                                                                                                             'SUPPORTED WEBSITE ERROR'),
            'realitysk_support': response_json.get('other', {}).get('realitysk_support', {}).get('info',
                                                                                                 'SUPPORTED WEBSITE ERROR'),
            'toprealitysk_support': response_json.get('other', {}).get('toprealitysk_support', {}).get('info',
                                                                                                       'SUPPORTED WEBSITE ERROR'),
        }
        cache.set('scraping_service_supported_websites', supported_websites, 18000)
        return supported_websites
    except Exception as e:
        return {'error': f'Failed to fetch supported scraping websites: {str(e)}'}


def scraping_service_scrapers_status():
    scraping_service_scrape_status_url = 'http://localhost:8088/service/scrape/status'
    try:
        response = requests.get(scraping_service_scrape_status_url, timeout=2)
        response.raise_for_status()
        response_json = response.json()
        scrape_status = {
            'nehnutelnostisk_scrape_status': 'SCRAPE STATUS ERROR' if not do_nehnutelnosti_scraping_service_files_exist() else response_json.get(
                'other', {}).get('nehnutelnostisk_scraping_in_progress', {}).get('info', False),
            'realitysk_scrape_status': 'SCRAPE STATUS ERROR' if not do_reality_scraping_service_files_exist() else response_json.get(
                'other', {}).get('realitysk_scraping_in_progress', {}).get('info', False),
            'toprealitysk_scrape_status': 'SCRAPE STATUS ERROR' if not do_topreality_scraping_service_files_exist() else response_json.get(
                'other', {}).get('toprealitysk_scraping_in_progress', {}).get('info', False),
        }
        return scrape_status
    except Exception as e:
        return {'error': f'Failed to fetch scraping service scrape status: {str(e)}'}


def realitysk_scraping_service_scrape_records(scrape_duration: ScrapeDuration):
    realitysk_scraping_service_scrape_url = 'http://localhost:8088/service/scrape'
    try:
        data = {
            'scrape_duration': scrape_duration.value,
        }
        response = requests.post(realitysk_scraping_service_scrape_url, json=data)
        response.raise_for_status()
        response_json = response.json()
        return response_json
    except Exception as e:
        return {'error': f'Failed to start scraping: {str(e)}'}


def update_database_property(id, field, new_value):
    """
    Update a specific field of a property in the database.

    Args:
    id (int): The ID of the property to update.
    field (str): The name of the field to update.
    new_value: The new value to set for the specified field.

    Returns:
    bool: True if the update was successful, False otherwise.
    """
    try:
        db = does_database_exist()

        if not db:
            False

        with sqlite3.connect(db) as conn:
            cursor = conn.cursor()
            sql_query = f"UPDATE properties SET {field} = ? WHERE id = ?"
            cursor.execute(sql_query, (new_value, id))
            conn.commit()
            if cursor.rowcount == 0:
                print(f"No records updated, check if the ID {id} exists.")
                return False
            print(f"Record updated successfully: ID {id} field {field} updated to {new_value}.")
            return True

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    except Exception as e:
        print(f"Exception in updating record: {e}")
        return False


def load_model_and_predict(property_features, offer_type):
    """
    Load the model, predict property prices, and evaluate the model's performance.

    Args:
    property_features (list of list): List containing features for each property.
    actual_prices (list): List containing actual prices of each property.

    Returns:
    tuple: A tuple containing predicted prices and R^2 score.
    """
    model_file_path = get_model_file_path(offer_type)
    try:
        with open(model_file_path, 'rb') as model_file:
            model = joblib.load(model_file)
    except FileNotFoundError:
        raise Exception("Model file not found. Please ensure the model has been trained and saved correctly.")
    except Exception as e:
        raise Exception(f"An error occurred while loading the model: {str(e)}")

    truefalse_columns = list({
        'lift',
        'parking_space',
        'basement',
        'gazebo',
        'terrace',
        'pool',
        'air_conditioning',
        'sauna',
        'balcony',
        'garage',
        'loggia',
        'garden',
        'fireplace',
        'bathroom',
        'new_building',
    })

    property_features.pop('offer_type', None)
    feature_df = pd.DataFrame(property_features)

    feature_df['age_of_property'] = datetime.datetime.now().year - feature_df['year_of_construction']
    feature_df['area_per_room'] = feature_df['land_area'] / feature_df['number_of_rooms']
    feature_df['luxury_index'] = feature_df[truefalse_columns].sum(axis=1)
    feature_df['rooms_x_age'] = feature_df['number_of_rooms'] * feature_df['age_of_property']
    feature_df['has_outdoor_space'] = feature_df[['garden', 'gazebo', 'terrace']].any(axis=1).astype(int)
    feature_df['has_wellness_space'] = feature_df[['pool', 'sauna']].any(axis=1).astype(int)
    feature_df['has_parking'] = feature_df[['parking_space', 'garage']].any(axis=1).astype(int)

    try:
        predictions = model.predict(feature_df)
        predictions = [float(pred) for pred in predictions]
        print("Prediction successful.")
        return predictions
    except Exception as e:
        print(f"Prediction failed: {e}")
        raise Exception(f"Prediction failed: {str(e)}")


def do_scraping_service_files_exist():
    '''
    Check if files exist in the specified directory.

    Returns:
    - bool: True if all files exist, False otherwise.
    '''
    # Directory path
    directory_path = f'C:\\Users\\{getpass.getuser()}\\AppData\\Roaming\\RealEstateWebScraper\\ScrapingService'

    # List of file names to test
    file_names = [
        'ScrapingController.exe',
        'scraping_service_winsw_configuration.err.log',
        'scraping_service_winsw_configuration.out.log',
        'scraping_service_winsw_configuration.wrapper.log',
        'scraping_service_winsw_configuration.xml'
    ]

    for file_name in file_names:
        file_path = os.path.join(directory_path, file_name)
        if not os.path.exists(file_path):
            return False
    return True


def do_nehnutelnosti_scraping_service_files_exist():
    '''
    Check if files exist in the specified directory.

    Returns:
    - bool: True if all files exist, False otherwise.
    '''
    # Directory path
    directory_path = f'C:\\Users\\{getpass.getuser()}\\AppData\\Roaming\\RealEstateWebScraper\\NehnutelnostiScrapingService'

    # List of file names to test
    file_names = [
        'NehnutelnostiScrapingController.exe',
        'nehnutlenosti_scraping_service_winsw_configuration.err.log',
        'nehnutelnosti_scraping_service_winsw_configuration.out.log',
        'nehnutelnosti_scraping_service_winsw_configuration.wrapper.log',
        'nehnutelnosti_scraping_service_winsw_configuration.xml'
    ]

    for file_name in file_names:
        file_path = os.path.join(directory_path, file_name)
        if not os.path.exists(file_path):
            return False
    return True


def do_reality_scraping_service_files_exist():
    '''
    Check if files exist in the specified directory.

    Returns:
    - bool: True if all files exist, False otherwise.
    '''
    # Directory path
    directory_path = f'C:\\Users\\{getpass.getuser()}\\AppData\\Roaming\\RealEstateWebScraper\\RealityScrapingService'

    # List of file names to test
    file_names = [
        'RealityScrapingController.exe',
        'reality_scraping_service_winsw_configuration.err.log',
        'reality_scraping_service_winsw_configuration.out.log',
        'reality_scraping_service_winsw_configuration.wrapper.log',
        'reality_scraping_service_winsw_configuration.xml'
    ]

    for file_name in file_names:
        file_path = os.path.join(directory_path, file_name)
        if not os.path.exists(file_path):
            return False
    return True


def do_topreality_scraping_service_files_exist():
    '''
    Check if files exist in the specified directory.

    Returns:
    - bool: True if all files exist, False otherwise.
    '''
    # Directory path
    directory_path = f'C:\\Users\\{getpass.getuser()}\\AppData\\Roaming\\RealEstateWebScraper\\TopRealityScrapingService'

    # List of file names to test
    file_names = [
        'TopRealityScrapingController.exe',
        'topreality_scraping_service_winsw_configuration.err.log',
        'topreality_scraping_service_winsw_configuration.out.log',
        'topreality_scraping_service_winsw_configuration.wrapper.log',
        'topreality_scraping_service_winsw_configuration.xml'
    ]

    for file_name in file_names:
        file_path = os.path.join(directory_path, file_name)
        if not os.path.exists(file_path):
            return False
    return True
