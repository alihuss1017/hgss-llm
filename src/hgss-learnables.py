from bs4 import BeautifulSoup
import requests
import json 
import pandas as pd


def extract_move_table_moves(table, key):
    """
    Extract move names (and levels if level_up=True) from a move table.
    """
    rows = table.find_all('tr')
    moves = []

    for row in rows:
        cols = row.find_all('td')
        if not cols or len(cols) < 1:
            continue  # skip rows with not enough columns

        if key == 'Level Up Moves': 
            move_name = cols[1].text.strip()
            if not move_name:
                continue
            try:
                level = int(cols[0].text.strip())
            except ValueError:
                continue  # skip rows where level is not a number

            moves.append({"Move": move_name, "Level": level})

        else:
            if key == 'HM Moves' or key == 'TM Moves':
                move_name = cols[1].text.strip()
            else: 
                move_name = cols[0].text.strip()
            
            moves.append(move_name)

    return moves

def scrape_pokemon_moves(url, pokemon_name):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    tab = soup.find('div', id='tab-moves-10')  # HGSS tab
    if not tab:
        return None

    move_data = {
        "Pokemon": pokemon_name.capitalize(),
        "Level Up Moves": [],
        "Egg Moves": [],
        "Move Tutor Moves": [],
        "HM Moves": [],
        "TM Moves": [],
        "Transfer-only Moves": []
    }

    # Find each section by <h3> title
    section_titles = {
        "Level Up Moves": "Moves learnt by level up",
        "Egg Moves": "Egg moves",
        "Move Tutor Moves": "Move Tutor moves",
        "HM Moves": "Moves learnt by HM",
        "TM Moves": "Moves learnt by TM",
        "Transfer-only Moves": "Transfer-only moves"
    }

    for key, title in section_titles.items():
        header = tab.find('h3', string=title)
        if header:
            table = header.find_next('table')
            if table:
                move_data[key] = extract_move_table_moves(table, key)

    return move_data


df = pd.read_csv('data/scraped/hgss-pokemon.csv')
names = [name.lower() for name in df['Pokemon']]
all_learnable_moves = []

for name in names:
    if name == 'nidoran♂':
        name = 'nidoran-m'

    if name == 'nidoran♀':
        name = 'nidoran-f'

    learnable_moves = scrape_pokemon_moves(f'https://pokemondb.net/pokedex/{name}/moves/4', name)
    all_learnable_moves.append(learnable_moves)

with open('data/scraped/hgss-learnables.json', 'w') as f:
    json.dump(all_learnable_moves, f, indent = 2)
