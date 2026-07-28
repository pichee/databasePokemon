# %%
import json
import requests

BASE_URL = "https://pokeapi.co/api/v2/evolution-chain/"
OUTPUT_FILE = "../data/raw/evolution_pokemon.json"

response = requests.get(f"{BASE_URL}?limit=10000")
urls = response.json().get("results", [])

total = len(urls)
print(f"Total de cadeias de evolução encontradas: {total}\n")

all_evolution = []

for index, url in enumerate(urls, 1):
    link = url["url"]
    res = requests.get(link)

    if res.status_code == 200:
        all_evolution.append(res.json())

        print(f"Evolução {index} de {total} baixada com sucesso")

with open(OUTPUT_FILE, "w") as arquivo:
    json.dump(all_evolution, fp=arquivo, indent=4)

print("\nDownload concluído!")
# %%