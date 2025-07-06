import requests
from bs4 import BeautifulSoup
import pandas as pd


data = []
gens = [1,2,3,4]
for gen in gens:

    url = f"https://pokemondb.net/move/generation/{gen}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, features = 'lxml')
    table = soup.find('table', class_ = 'data-table sticky-header block-wide')
    rows = table.find_all('tr')

    for row in rows:
        tds = row.find_all('td')
        if len(tds) < 5:
            continue
        
        move_name = tds[0].text.strip()
        move_type = tds[1].text.strip()
        move_cat = tds[2]['data-sort-value'].capitalize()
        move_dmg = tds[3].text.strip()
        move_acc = tds[4].text.strip()
        move_pp = tds[5].text.strip()
        move_effect = tds[6].text.strip()

        data.append({
            'Move': move_name,
            'Type': move_type,
            'Category': move_cat,
            'Power': move_dmg,
            'Accuracy': move_acc,
            'PP': move_pp,
            'Effect': move_effect,
        })

df = pd.DataFrame(data)
df.to_csv('data/scraped/hgss-moves.csv')