import pandas as pd
import numpy as np

def extract_status(lista_stats):
    new_columns = {}
    
    for item in lista_stats:
        
        nome_stats = item['stat']['name']
        value = item["base_stat"]
        new_columns[nome_stats] = value

    return pd.Series(new_columns)

def extract_abilities(lista_abilities):
        new_columns = {}
        for item in lista_abilities:
            nome = item['ability']['name']

            if item['is_hidden']:
                new_columns['hidden_ability'] = nome
            elif item['slot'] == 1:
                new_columns['ability_1'] = nome
            elif item['slot'] == 2:
                new_columns['ability_2'] = nome

        return pd.Series(new_columns)

def extract_moves(lista_moves):
    new_columns = {}
    for item in lista_moves:
        nome = item['']

def fill_missing_sprites(df, col_principal, coluna_secundaria):
    return df[col_principal].fillna(df[coluna_secundaria])

df = pd.read_json("../data/raw/data_pokemon.json")
df['id'] = df.index
df['pokemon'] = df['species'].str['name']
df['weight (KG)'] = df['weight'].apply(lambda x:x /10)
df['height (M)'] = df['height'].apply(lambda x:x /10)
df['id'] = df['id'].apply(lambda x:x+1)


df = df.explode('types')


df['type'] = df['types'].str.get('type').str.get('name')
df['slot_type'] = df['types'].str.get('slot')

df['first_type'] = np.where(df['slot_type'] == 1, df['type'], np.nan)
df['second_type'] = np.where(df['slot_type'] == 2, df['type'], np.nan)
df = df.groupby(by='pokemon',as_index=False).first()

df_stats = df['stats'].apply(extract_status)
df_abilities = df['abilities'].apply(extract_abilities)
df = pd.concat([df,df_stats,df_abilities],axis=1)

df['legacy'] = df['cries'].str.get('legacy')
df['latest'] = df['cries'].str.get('latest')

df['official-artwork-default'] = df['sprites'].str.get('other').str.get("official-artwork").str.get("front_default")
df['official-artwork-shiny'] = df['sprites'].str.get('other').str.get("official-artwork").str.get("front_shiny")



df_sprites = pd.json_normalize(df['sprites'])
colunas = ["front_default", "front_female" ,"front_shiny",
        "front_shiny_female","other.showdown.front_default",
        "other.showdown.front_female","other.showdown.front_shiny",
        "other.showdown.front_shiny_female","other.official-artwork.front_default",
        "other.official-artwork.front_shiny",]
df_sprites = df_sprites[colunas]


df_sprites['front_shiny_female'] = fill_missing_sprites(df_sprites, 'front_shiny_female', 'front_shiny')
df_sprites['front_female'] = fill_missing_sprites(df_sprites, 'front_female', 'front_default')
df_sprites['other.showdown.front_female'] = fill_missing_sprites(df_sprites, 'other.showdown.front_female','other.showdown.front_default')
df_sprites['other.showdown.front_shiny_female'] = fill_missing_sprites(df_sprites, 'other.showdown.front_shiny_female', 'other.showdown.front_shiny')

df = df.drop(['weight','type','slot_type','types','height',
              'species','game_indices','stats','cries',
              'abilities','past_types','past_stats','past_abilities',
              'forms','name','order','location_area_encounters',
              'moves','held_items','is_default','sprites'],axis=1)

df = pd.concat([df,df_sprites],axis=1)

# 1. Renomear as colunas chatas/com pontos/traços
df = df.rename(columns={
    'pokemon': 'name',
    'special-attack': 'sp_atk',
    'special-defense': 'sp_def',
    'legacy': 'cry_legacy',
    'latest': 'cry_latest',
    'front_default': 'sprite_front_default',
    'front_female': 'sprite_front_female',
    'front_shiny': 'sprite_front_shiny',
    'front_shiny_female': 'sprite_front_shiny_female',
    'other.showdown.front_default': 'gif_front_default',
    'other.showdown.front_female': 'gif_front_female',
    'other.showdown.front_shiny': 'gif_front_shiny',
    'other.showdown.front_shiny_female': 'gif_front_shiny_female',
    'other.official-artwork.front_default': 'arte_normal',
    'other.official-artwork.front_shiny': 'arte_shiny'
})

df = df[[
    # identificao
    'id', 'name', 'first_type', 'second_type', 'height (M)', 'weight (KG)', 'base_experience',
    # status
    'hp', 'attack', 'defense', 'sp_atk', 'sp_def', 'speed',
    # habilidades
    'ability_1','ability_2','hidden_ability',
    # audios
    'cry_latest', 'cry_legacy',
    # artes
    'arte_normal', 'arte_shiny',
    # sprites
    'sprite_front_default', 'sprite_front_female', 'sprite_front_shiny', 'sprite_front_shiny_female',
    # gifs
    'gif_front_default', 'gif_front_female', 'gif_front_shiny', 'gif_front_shiny_female'
]].sort_values(by='id')

df.to_csv("../data/cleaned/data_pokemon.csv")