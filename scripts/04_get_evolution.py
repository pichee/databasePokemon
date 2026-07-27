# %%
import requests
import json

BASE_URL = 'https://pokeapi.co/api/v2/evolution-chain/'
OUTPUT_FILE = '../data/raw/evolution_pokemon.json'


response = requests.get(f"{BASE_URL}?limit=10000")
urls = response.json().get("results", [])

total = len(urls)

all_evolution = []

for url in urls:
    link = url["url"]
    res = requests.get(link)

    if res.status_code == 200:
        all_evolution.append(res.json())

with open(OUTPUT_FILE, "w") as arquivo:
    json.dump(all_evolution,fp=arquivo ,indent=4)
# %%

