from staticfiles.helpers.helpers import get_cities


def generate_html_table(data):
    table_html = "<table border='1'>\n"
    table_html += "<tr><th>Region</th><th>District</th><th>Nehnutelnosti.sk URL</th><th>TopReality.sk URL</th><th>Reality.sk URL</th></tr>\n"

    for region, districts in data.items():
        for district in districts:
            table_html += f"<tr><td>{region}</td><td>{district['name']}</td><td>{district['nehnutelnostiskurl']}</td><td>{district['toprealityskurl']}</td><td>{district['realityskurl']}</td></tr>\n"

    table_html += "</table>"
    return table_html


def save_html_table_to_file(html_table, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(html_table)


if __name__ == "__main__":
    # Get cities data
    cities_data = get_cities()

    # Generate HTML table
    html_table = generate_html_table(cities_data)

    # Specify the file path to save the HTML table
    file_path = '../../templates/supported_locations.html'

    # Save the HTML table to the file
    save_html_table_to_file(html_table, file_path)

    print(f"HTML table saved to {file_path}")
