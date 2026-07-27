# %%
import pandas as pd
import os

processed_dir = '../data/processed/'

os.makedirs(processed_dir, exist_ok=True)
df = pd.read_json("../data/raw/move_pokemon.json")

colums = ['id','learned_by_pokemon']
df = df[colums]

df = df.explode('learned_by_pokemon')
df['learned_by_pokemon'] = (
    df['learned_by_pokemon']
    .str.get('url')
    .str.replace("https://pokeapi.co/api/v2/pokemon/", "", regex=False)
    .str.replace("/","",regex = False))

df = df.dropna(subset=['learned_by_pokemon'])
df.head()
df = df.rename(columns={'learned_by_pokemon': 'id_pokemon'})


df.to_csv("../data/processed/move_pokemon.csv",index=False)
