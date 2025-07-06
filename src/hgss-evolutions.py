import csv 
import requests
from bs4 import BeautifulSoup, Tag
import pandas as pd 

poke_df = pd.read_csv('data/hgss-pokemon.csv')
poke_names = [name.lower() for name in poke_df['name']]
evo_filters = ['alolan', 'galarian', 'hisuian', 'paldean']
data = []

for poke_name in poke_names:
    url = f'https://pokemondb.net/pokedex/{poke_name}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, features = 'lxml')

    evo_chart = soup.find('div', class_ = 'infocard-list-evo')
    if evo_chart:
        names = evo_chart.find_all('a', class_ = 'ent-name')

        for name in names:
            if name.text.strip().lower() == f'{poke_name}':
                if name.find_next('span', class_ = 'infocard infocard-arrow'):
                    next_element = name.find_next('span', class_ = 'infocard infocard-arrow')
                    evo_method = next_element.find('small').text.strip()
                    evo_info = next_element.find_next('span', class_ = 'infocard-lg-data text-muted').find_all('small')
                    evo_dex = int(evo_info[0].text.strip().replace('#', ''))
                    evo_form = evo_info[1].text.strip()
                    evo_name = next_element.find_next('a', class_ = 'ent-name').text.strip()
                    if any(evo_filter in evo_form.lower() for evo_filter in evo_filters) or evo_dex > 492:
                        break
                    else:
                        data.append({
                            'Pokemon' : name.text.strip(),
                            'Method': evo_method, 
                            'Evolves to': evo_name
                        })
                    break
                else:
                    break
            else:
                continue
        else:
            continue

df = pd.DataFrame(data)
df.to_csv('data/scraped/hgss-evolutions.csv', index = False)