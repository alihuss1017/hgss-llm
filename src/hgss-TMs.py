import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://pokemondb.net/heartgold-soulsilver/tms"
response = requests.get(url)
soup = BeautifulSoup(response.text, features = 'lxml')
table = soup.find('table', class_ = 'data-table')

data = []
rows = table.find_all('tr')

for row in rows:
    tds = row.find_all('td')
    if len(tds) < 5:
        continue
    
    tm_num = tds[0].text.strip()
    tm_name = tds[1].text.strip()
    tm_type = tds[2].text.strip()
    tm_cat = tds[3]['data-sort-value'].capitalize()
    tm_dmg = tds[4].text.strip()
    tm_acc = tds[5].text.strip()
    tm_pp = tds[6].text.strip()
    tm_locs = []

    locs = tds[7].find_all('div')
    for loc in locs:
        tm_locs.append(loc.text.strip())

    url_slug = tm_name.lower().replace(" ", "-")
    url = f"https://pokemondb.net/move/{url_slug}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, features = 'lxml')

    div = soup.find('div', class_ = 'grid-col span-md-12 span-lg-8')
    table = div.find('table', class_ = 'vitals-table')

    games = ['Diamond', 'Pearl', 'Platinum', 'HeartGold', 'SoulSilver']
    for tr in table.find_all('tr'):
        if any(game in tr.text for game in games):
            td = tr.find('td', class_ = 'cell-med-text')
            tm_desc = td.text.strip()

    data.append({
        'TM': tm_num,
        'Move': tm_name,
        'Type': tm_type,
        'Category': tm_cat,
        'Power': tm_dmg,
        'Accuracy': tm_acc,
        'PP': tm_pp,
        'Location': tm_locs,
        'Effect': tm_desc
    })

df = pd.DataFrame(data)
df.to_csv('data/scraaped/hgss-TMs.csv')