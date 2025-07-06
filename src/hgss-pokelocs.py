import requests
from bs4 import BeautifulSoup
import csv

def get_location_links(region_id):
    """
    Extracts all location names and URLs for a given region (e.g., Johto or Kanto).
    """
    base_url = "https://pokemondb.net/location"
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, "html.parser")

    panel = soup.find("div", {"id": region_id})
    location_divs = panel.find_all("div", class_="grid-col span-sm-6 span-md-4 span-lg-2")

    locations = []
    for div in location_divs:
        for a_tag in div.find_all("a"):
            location_name = a_tag.text.strip()
            location_url = 'https://pokemondb.net' + a_tag['href']
            locations.append((location_name, location_url))

    return locations

def format_location_name(location_url):
    """
    Cleans the location URL to extract a human-readable route or area name.
    Example: 'https://pokemondb.net/location/johto-route-29' -> 'Route 29'
    """
    slug = location_url.split('/')[-1]  # e.g., 'johto-route-29'
    name = slug.split('-', 1)[-1]       # Remove 'johto-' or 'kanto-'
    return name.replace('-', ' ').title()

def parse_gen4_encounters(location_name, location_url):
    """
    Parses all Generation 4 encounter tables from the given location page.
    Returns a list of dictionaries containing Pokémon encounter info.
    """
    response = requests.get(location_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    gen4_sections = soup.find_all('h2', id=lambda x: x and x.startswith('gen4'))

    location_data = []

    for section in gen4_sections:
        tag = section.find_next_sibling()

        while tag and (not hasattr(tag, 'name') or not tag.name.startswith('h2')):
            if tag.name == 'div' and 'resp-scroll' in tag.get('class', []):
                table = tag.find('table', class_='data-table')
                if not table:
                    tag = tag.find_next_sibling()
                    continue

                for tbody in table.find_all('tbody'):
                    for row in tbody.find_all('tr'):
                        cols = row.find_all('td')
                        if len(cols) < 6:
                            continue

                        # Pokémon Name
                        name_tag = row.find('a', class_='ent-name')
                        name = name_tag.text.strip() if name_tag else None

                        # Games: HG and SS
                        game_cells = [td for td in cols if 'cell-loc-game' in td.get('class', [])]
                        games = []
                        for cell in game_cells:
                            if 'cell-loc-game-blank' in cell.get('class', []):
                                games.append('blank')
                            else:
                                games.append(cell.text.strip())
                        while len(games) < 2:
                            games.append('blank')

                        # Times of day (Morning, Day, Night)
                        time_status = ['blank', 'blank', 'blank']
                        slot_index = {'Morning': 0, 'Day': 1, 'Night': 2}
                        for icon in cols[3].find_all(['img', 'span']):
                            title = icon.get('title', '')
                            if icon.name == 'img' and title in slot_index:
                                time_status[slot_index[title]] = title

                        # Rarity
                        rarity_img = cols[4].find('img')
                        rarity = rarity_img['title'] if rarity_img else 'Unknown'

                        # Levels
                        levels = cols[5].text.strip()

                        # Store the extracted info
                        entry = {
                            'Pokemon': name,
                            'Location': location_name,
                            'Available in HeartGold': "Yes" if games[0] == 'HG' else 'No',
                            'Available in Soulsilver': "Yes" if games[1] == 'SS' else 'No',
                            'Appears in Morning': "Yes" if time_status[0] == 'Morning' else 'No',
                            'Appears in Daytime': "Yes" if time_status[1] == 'Day' else 'No',
                            'Appears in Nighttime': "Yes" if time_status[2] == 'Night' else 'No',
                            'Rarity': rarity,
                            'Levels': levels
                        }

                        location_data.append(entry)
            tag = tag.find_next_sibling()

    return location_data

def main():
    all_data = []

    # Get all Johto and Kanto locations
    johto_locations = get_location_links('loc-johto')
    kanto_locations = get_location_links('loc-kanto')
    all_locations = johto_locations + kanto_locations

    # Visit each location and parse Gen 4 encounter data
    for _, location_url in all_locations:
        readable_name = format_location_name(location_url)
        try:
            location_data = parse_gen4_encounters(readable_name, location_url)
            all_data.extend(location_data)
        except Exception as e:
            print(f"Error scraping {location_url}: {e}")
            continue

    # Write to CSV
    if all_data:
        with open('data/scraped/hgss-pokelocs.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=all_data[0].keys())
            writer.writeheader()
            writer.writerows(all_data)
        print("CSV file saved as 'hgss-pokelocs.csv'")
    else:
        print("No data collected.")

if __name__ == "__main__":
    main()
