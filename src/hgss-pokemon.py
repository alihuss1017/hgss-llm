import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.serebii.net/pokemon/nationalpokedex.shtml"
res = requests.get(url)
soup = BeautifulSoup(res.text, "html5lib")
rows = soup.select('tr')

pokemon_entries = []
for row in rows:
    tds = row.find_all('td', class_ = 'fooinfo')
    if len(tds) < 9:
        continue
    num = tds[0].text.strip()
    name = tds[2].text.strip()
    
    type_links = tds[3].find_all('a', href = lambda href: href and '/pokemon/type/' in href)
    types = [a['href'].split('/')[-1].capitalize() for a in type_links]

    if types[0] == 'Fairy':
        types[0] = 'Normal'
    
    if len(types) > 1 and types[1] == 'Fairy':
            if types[0] == 'Normal':
                types[1] = None
            else:
                types[1] = 'Normal'

    type1 = types[0]
    type2 = types[1] if len(types) > 1 else None
    ability_links = tds[4].find_all('a', href = lambda href: href and '/abilitydex/' in href)
    abilities = [a.text.strip() for a in ability_links]

    stats = [int(td.text.strip()) for td in tds[5:]]
    hp, atk, defense, sp_atk, sp_def, speed = stats 
    pokemon_entries.append({
        '#': num,
        'name': name, 
        'type1': type1,
        'type2': type2,
        'abilities': ', '.join(abilities),
        'hp': hp,
        'atk': atk,
        'def': defense,
        'sp_atk': sp_atk,
        'sp_def': sp_def,
        'speed': speed
    })

    if int(num[1:]) == 251:
        break


df = pd.DataFrame(pokemon_entries)
df.to_csv('data/hgss-pokemon.csv', index = False)
print("Saved to data/hgss-pokemon.csv")