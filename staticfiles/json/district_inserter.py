import json


def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def write_json(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


def insert_city(file_path, new_city, insert_position):
    cities = read_json(file_path)

    # Adjust the IDs of existing cities
    for city in cities:
        if city["id"] >= insert_position:
            city["id"] += 1

    # Insert the new city
    new_city["id"] = insert_position
    cities.insert(insert_position - 1, new_city)  # List index starts from 0

    write_json(file_path, cities)


# Example usage
file_path = 'districts.json'
new_city = {
    "name": "Bratislava",
    "veh_reg_num": "BL",
    "code": 100,
    "region_id": 2,
    "nehnutelnostiskurl": "bratislava",
    "toprealityskurl": "bratislava",
    "realityskurl": "bratislava"
}
insert_position = 5

insert_city(file_path, new_city, insert_position)
