# %% 
import requests
import pandas as pd
import json
import os

raw_dir = "../data/raw"
cleaned_dir = "../data/cleaned"

os.makedirs(raw_dir, exist_ok=True)
os.makedirs(cleaned_dir, exist_ok=True)


url = 'https://pokeapi.co/api/v2/pokemon/?limit=100000'
pokemon_names = requests.get(url=url)
pokemon_names = pokemon_names.json()

with open("../data/raw/name_pokemon.json",'w') as arquivo:
    json.dump(pokemon_names,fp=arquivo ,indent=4)

df = pd.read_json('../data/raw/name_pokemon.json')
df['id'] = df.index
df['pokemon'] = df['results'].str['name']

df = df.drop(['count','next','previous','results'],axis=1)

df['id'] = df['id'].apply(lambda x: x+1)
df.to_csv("../data/cleaned/name_pokemon.csv",index=False)

# %%