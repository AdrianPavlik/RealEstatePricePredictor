import re
import numpy as np
from geopy import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from unidecode import unidecode

# Initialize Geolocator
geolocator = Nominatim(user_agent="DP")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)


def preprocess_property(data):
    def normalize_text(text):
        text = str(text) if text is not None else ""
        return unidecode(text).lower() if text else ""

    def replace_known_values(value):
        value = str(value)
        if value in ["Nepoznané", "Nezadaná", "NULL", "None", "Cena", "Info", "\xa0"]:
            return np.nan
        return value.replace("\xa0", "")  # Remove non-breaking space characters

    def get_lat_long(city, street=None):
        location_query = f"{normalize_text(street)}, {normalize_text(city)}, Slovakia" if street else f"{normalize_text(city)}, Slovakia"
        try:
            location = geocode(location_query)
            return (location.latitude, location.longitude) if location else (None, None)
        except Exception as e:
            location_query = f"{normalize_text(city)}, Slovakia"
            location = geocode(location_query)
            return (location.latitude, location.longitude) if location else (None, None)

    def has_parking_keywords(text):
        if text:
            keywords = [normalize_text(kw) for kw in
                        ['mies', 'zabez', 'priam', 'dvore', 'statie', 'garaz', 'pred', 'sučas']]
            pattern = r'\b(\w*park\w*)(?:\s+(\w+)){1,5}'
            matches = re.finditer(pattern, normalize_text(text), re.IGNORECASE)
            for match in matches:
                words = match.group().split()
                if any(word for word in words[1:6] if any(kw in word for kw in keywords)):
                    return True
        return False

    def extract_rooms(type_field):
        for i in range(5, 0, -1):
            if str(i) in str(type_field):
                return i
        return 0

    def update_property_condition(condition):
        return 1 if 'novostavba' in normalize_text(condition) else 0

    def clean_area(area):
        return str(area).replace(' m²', '').strip() if isinstance(area, str) else area

    # Update and clean each field in the data dictionary
    cleaned_data = {}
    for key, value in data.items():
        cleaned_value = replace_known_values(str(value))
        cleaned_data[key] = cleaned_value

    # Apply transformations to specific fields
    cleaned_data['latitude'], cleaned_data['longitude'] = get_lat_long(cleaned_data.get('city'), cleaned_data.get('street'))
    cleaned_data['land_area'] = clean_area(cleaned_data.get('land_area', ''))
    cleaned_data['number_of_rooms'] = extract_rooms(cleaned_data.get('type', '')) if cleaned_data['number_of_rooms'] is None or '' else cleaned_data['number_of_rooms']
    cleaned_data['parking_space'] = int(has_parking_keywords(cleaned_data.get('long_description', '')))
    cleaned_data['new_building'] = update_property_condition(cleaned_data.get('property_condition', ''))

    keywords = {
        'lift': ["Výťah", "Paternoster", "Lift"],
        'garden': ["Záhrad"],
        'garage': ["Garáž"],
        'terrace': ["Teras"],
        'pool': ["bazen"],
        'gazebo': ["altan"],
        'fireplace': ["krb"],
        'sauna': ['saun'],
        'balcony': ['balkón'],
        'loggia': ['loggi'],
        'air_conditioning': ['klimatizac'],
        'bathroom': ['kúpeľ'],
        'basement': ['pivn', 'podpiv']
    }

    # Check for the presence of keywords
    for col, words in keywords.items():
        cleaned_data[col] = 1 if any(normalize_text(word) in normalize_text(cleaned_data.get('long_description', '')) for word in words) else 0

    return cleaned_data