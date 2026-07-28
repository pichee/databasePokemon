# %%
import pandas as pd

def pega_primeiro_flavor(entries):
    if isinstance(entries, list) and len(entries) > 0:

        for entry in entries:
            if isinstance(entry, dict) and entry.get('language', {}).get('name') == 'en':
                return entry.get('flavor_text', '').replace('\n', ' ')
        

        return entries[0].get('flavor_text', '').replace('\n', ' ')
    return None

def pega_segundo_desc(entries):
    if isinstance(entries, list) and len(entries) > 1:
        return entries[1].get('short_effect')
    elif isinstance(entries, list) and len(entries) > 0:
        return entries[0].get('short_effect')
    return None

def formata_stat_changes(changes):
    if isinstance(changes, list) and len(changes) > 0:
        formatados = []
        for change in changes:
            if isinstance(change, dict):
                stat_name = change.get('stat', {}).get('name')
                val = change.get('change')
                if stat_name and val is not None:
                    formatados.append(f"{stat_name}: {val}")
        return ", ".join(formatados) if formatados else None
    return None

df = pd.read_json("../data/raw/move_pokemon.json")

df = df.drop(['contest_combos','contest_type','contest_effect',
              'effect_chance','learned_by_pokemon','super_contest_effect',
              'past_values','names','machines','generation',
              'effect_changes'], axis=1)

df['damage_class'] = df['damage_class'].str.get('name')
df['type'] = df['type'].str.get('name')
df['target'] = df['target'].str.get('name')
df['flavor_text_entries'] = df['flavor_text_entries'].apply(pega_primeiro_flavor)
df['effect_entries'] = df['effect_entries'].apply(pega_segundo_desc)

if 'stat_changes' in df.columns:
    df['stat_changes'] = df['stat_changes'].apply(formata_stat_changes)

df_aux = pd.json_normalize(df["meta"])
df_aux = df_aux.drop([
    'ailment.url', 'category.url'
], axis=1, errors='ignore')


df = pd.concat([df.drop('meta', axis=1), df_aux], axis=1)

df = df.sort_values('id', ascending=True).reset_index(drop=True)


ordem_desejada = [
    'id', 'name', 'type', 'damage_class', 'target', 
    'power', 'accuracy', 'pp', 'priority',
    'crit_rate', 'drain', 'healing', 
    'ailment.name', 'ailment_chance', 'category.name', 
    'flinch_chance', 'stat_chance',
    'min_hits', 'max_hits', 'min_turns', 'max_turns',
    'flavor_text_entries', 'effect_entries', 'stat_changes'
]

colunas_finais = [col for col in ordem_desejada if col in df.columns]
df = df[colunas_finais]
df = df.dropna(subset=['flavor_text_entries'])
df['power'] = df['power'].fillna(0)
df['accuracy'] = df['accuracy'].fillna(100)
colunas_numericas = df.select_dtypes(include=['number']).columns
df[colunas_numericas] = df[colunas_numericas].fillna(0)

df.to_csv("../data/processed/move_details.csv", index=False)
# %%