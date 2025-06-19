import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.serebii.net/heartgoldsoulsilver/tmhm.shtml"
headers = {"User-Agent": "Mozilla/5.0"}

res = requests.get(url, headers=headers)

# ✅ html5lib = browser-grade tolerance for malformed HTML
soup = BeautifulSoup(res.text, "html5lib")

# Grab the correct table
tables = soup.find_all("table", class_="dextable")
table = tables[0]
rows = table.find_all("tr")

print(f"Total rows found: {len(rows)}")

data = []

for row in rows:
    cols = row.find_all("td")
    if len(cols) != 9:
        continue
    if "Move Name" in cols[1].text:
        continue

    tm = cols[0].text.strip()
    move = cols[1].text.strip()
    effect = cols[2].text.strip()

    type_img = cols[3].find("img")
    move_type = type_img["src"].split("/")[-1].replace(".gif", "").capitalize() if type_img else ""

    kind_img = cols[4].find("img")
    kind = kind_img["src"].split("/")[-1].replace(".png", "").capitalize() if kind_img else ""

    power = cols[5].text.strip()
    accuracy = cols[6].text.strip()
    pp = cols[7].text.strip()
    location = cols[8].get_text(separator=" ", strip=True)

    data.append({
        "TM": tm,
        "Move": move,
        "Effect": effect,
        "Type": move_type,
        "Kind": kind,
        "Power": power,
        "Accuracy": accuracy,
        "PP": pp,
        "Location": location
    })

df = pd.DataFrame(data)
df.to_csv("hgss-moves.csv", index=False)
