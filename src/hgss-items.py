import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.serebii.net/heartgoldsoulsilver/items.shtml"
headers = {"User-Agent": "Mozilla/5.0"}

res = requests.get(url, headers=headers)

soup = BeautifulSoup(res.text, "html5lib")


tables = soup.find_all("table")

data = []

# for i, table in enumerate(tables):
#     rows = table.find_all("tr")
#     print(f"Table {i}: {len(rows)} rows")

for table in tables:
    rows = table.find_all("tr")
    
    for row in rows:
        cols = row.find_all("td")
        if len(cols) != 4:
            continue
        if "Name" in cols[1].text:
            continue

        picture_img = cols[0].text.strip()
        name = cols[1].text.strip()
        effect = cols[2].text.strip()
        location = cols[3].get_text(separator=" ", strip=True)

        data.append({
            "Name": name,
            "Effect": effect,
            "Location": location
        })

df = pd.DataFrame(data)
df.to_csv("../data/hgss-items.csv", index=False)
