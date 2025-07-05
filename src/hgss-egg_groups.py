import requests
from bs4 import BeautifulSoup
import pandas as pd

groups = ['bug', 'ditto', 'dragon', 'fairy', 'flying', 'ground', 'humanshape', 'indeterminate', 'mineral',
          'monster', 'plant', 'water1', 'water2', 'water3', 'noeggs']
data = []

for egg in groups:
    pokemon = []
    url = f"https://www.serebii.net/pokedex-dp/egg/{egg}.shtml"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html5lib")
    table = soup.find('table', class_ = 'dextable')
    rows = table.find_all('tr')

    for row in rows:
        tds = row.find_all('td', class_ = 'fooinfo')
        if len(tds) < 1:
            continue
        else:
            pokemon.append(tds[2].text.strip())
    

    data.append({'Egg Group': egg, 
                 'Pokemon': pokemon
                 })


df = pd.DataFrame(data)
df.to_csv('data/hgss-egg_groups.csv', index = False)



