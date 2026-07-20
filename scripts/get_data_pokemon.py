# %% 
import pandas as pd
import requests
import os
import json
import time

df = pd.read_csv("../data/cleaned/pokemon_names.csv")
x = df['id'].max()

lista_json = []

for i in range(1,x+1): 
    url = f"https://pokeapi.co/api/v2/pokemon/{i}"

    body = requests.get(url=url)

    if body.status_code == 200:

        lista_json.append(body.json())
    time.sleep(0.25)

        
with open("../data/raw/data_pokemon.json","w") as arquivo:
    json.dump(lista_json,fp=arquivo ,indent=4)

# %%
