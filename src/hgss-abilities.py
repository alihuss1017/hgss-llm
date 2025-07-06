import requests
from bs4 import BeautifulSoup
import pandas as pd

data = []

url = f"https://pokemondb.net/ability"
response = requests.get(url)
soup = BeautifulSoup(response.text, features = 'lxml')
table = soup.find('table', class_ = 'data-table sticky-header block-wide')
rows = table.find_all('tr')
for row in rows:
    tds = row.find_all('td')
    if len(tds) < 1 or int(tds[3].text.strip()) > 4:
        continue
    else:
        ability = tds[0].text.strip()
        description = tds[2].text.strip()

        data.append({
            'Ability': ability,
            'Effect': description
        })

df = pd.DataFrame(data)
df.to_csv('data/scraped/hgss-abilities.csv')