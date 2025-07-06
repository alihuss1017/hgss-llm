import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import csv

# ---------------------------
# Utilities
# ---------------------------

def split_pokemon_level(text):
    """Extract Pokémon name and level from a string like 'Pidgeotto Lv. 13'."""
    match = re.match(r"(.+?)\s+Lv\.?\s*(\d+)", text)
    if match:
        return match.group(1).strip(), int(match.group(2))
    return text, None

def extract_reward_fields(reward_lines):
    badge = obedience = tm = hm_unlock = None
    full_text = " ".join(reward_lines)

    for i, line in enumerate(reward_lines):
        if 'Badge' in line:
            # Always assign badge
            badge = line.split('-')[0].strip()

            # Check next line for obedience
            if i + 1 < len(reward_lines) and 'Traded Pokémon' in reward_lines[i + 1]:
                obedience = reward_lines[i + 1].strip()
            break

    # TM
    tm_match = re.search(r"(TM\d+)", full_text)
    if tm_match:
        tm = tm_match.group(1)

    # HM unlock
    hm_match = re.search(r"(Can now use\s+HM\d+\s*[-–]?\s*[\w\s]+?in the field)", full_text)
    if hm_match:
        hm_unlock = hm_match.group(1).strip()

    return {
        "badge": badge,
        "obedience": obedience,
        "tm": tm,
        "hm_unlock": hm_unlock
    }

def extract_specialty_type(table):
    """Extract the specialty type of the gym."""
    for b in table.find_all('b'):
        if 'Specialty Type' in b.text and b.next_sibling:
            return b.next_sibling.strip()
    return None

def extract_gym_leader(rows):
    """Extract the gym leader's name from table rows."""
    for row in rows:
        if row.find('img') is None:
            text = row.get_text(strip=True)
            if all(x not in text.lower() for x in ["lv.", "lv", "lv "]):
                return text
    return None

def extract_pokemon_team(rows):
    """Extract a team of Pokémon and their levels."""
    team = []
    for row in rows:
        if row.find('img') is None:
            text = row.get_text(separator=' ', strip=True)
            name, level = split_pokemon_level(text)
            if level is not None:
                team.append({"pokemon": name, "level": level})
    return team

def parse_gym_number_and_location(text):
    """Try to parse gym number and location from heading text."""
    gym_match = re.match(r"Gym\s+#(\d+)\s+-\s+(.+)", text)
    if gym_match:
        return int(gym_match.group(1)), gym_match.group(2).strip()
    
    kanto_match = re.search(r"Kanto Gym\s+#\d+\s+[–-]\s+(.*?)(?:,|$)", text)
    if kanto_match:
        return None, kanto_match.group(1).strip()
    
    return None, None

# ---------------------------
# Main Scraper
# ---------------------------

def scrape_hgss_gyms():
    url = "https://www.serebii.net/heartgoldsoulsilver/gym.shtml"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html5lib")

    gyms = []
    tables = soup.find_all('td', class_='foocontent')

    current_region = "Johto"
    johto_counter = 1
    kanto_counter = 1

    for table in tables:
        rows = table.find_all('td', class_='cen')
        info = table.find_all('p')

        if len(info) < 3:
            continue

        # Extract gym heading, description, and rewards
        heading_text = info[0].text.strip()
        description = info[1].text.strip()
        reward_raw = info[2].get_text(separator="\n").replace('\xa0', '')
        reward_lines = [line.strip() for line in reward_raw.split('\n') if line.strip()]
        if reward_lines and reward_lines[0].lower().startswith('rewards'):
            reward_lines = reward_lines[1:]

        # Extract fields
        gym_number, location = parse_gym_number_and_location(heading_text)
        gym_leader = extract_gym_leader(rows)
        team = extract_pokemon_team(rows)
        specialty = extract_specialty_type(table)
        rewards = extract_reward_fields(reward_lines)

        # Assign gym number and region
        if current_region == "Johto":
            region = "Johto"
            gym_number = johto_counter
            if location == "Blackthorn City":
                current_region = "Kanto"
            johto_counter += 1
        else:
            region = "Kanto"
            gym_number = kanto_counter
            kanto_counter += 1

        gyms.append({
            "Gym Number": gym_number,
            "Region": region,
            "Location": location,
            "Specialty": specialty,
            "Description": description,
            "Gym Leader": gym_leader,
            "Team": str(team),
            "Badge": rewards['badge'],
            "Obedience": rewards['obedience'],
            "TM": rewards['tm'],
            "HM Unlocked": rewards['hm_unlock'],
        })

    return gyms

# ---------------------------
# Save to CSV
# ---------------------------

def save_gyms_to_csv(gyms, filename="data/scraped/hgss-gyms.csv"):
    df = pd.DataFrame(gyms)
    df.to_csv(filename, index=False, quoting=csv.QUOTE_ALL)

# ---------------------------
# Run Everything
# ---------------------------

if __name__ == "__main__":
    gym_data = scrape_hgss_gyms()
    save_gyms_to_csv(gym_data)
    print("HGSS gym data saved to 'data/scraped/hgss-gyms.csv'")
