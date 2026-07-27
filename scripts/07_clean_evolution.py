import json
import pandas as pd


def extract_evolutions(item):
    lista_evolucoes = []

    def extrair_id(url):
        if url:
            partes = url.strip("/").split("/")
            return int(partes[-1])
        return None

    def processar_cadeia(no_atual, id_cadeia):
        de_id = extrair_id(no_atual["species"]["url"])

        for proximo in no_atual.get("evolves_to", []):
            para_id = extrair_id(proximo["species"]["url"])

            detalhes = {}
            if proximo.get("evolution_details"):
                detalhes = proximo["evolution_details"][0]

            item_usado = None
            if detalhes.get("item"):
                item_usado = detalhes["item"]["name"]

            item_segurado = None
            if detalhes.get("held_item"):
                item_segurado = detalhes["held_item"]["name"]

            golpe = None
            if detalhes.get("known_move"):
                golpe = detalhes["known_move"]["name"]

            tipo_golpe = None
            if detalhes.get("known_move_type"):
                tipo_golpe = detalhes["known_move_type"]["name"]

            local = None
            if detalhes.get("location"):
                local = detalhes["location"]["name"]

            metodo = None
            if detalhes.get("trigger"):
                metodo = detalhes["trigger"]["name"]

            horario = None
            if detalhes.get("time_of_day") != "":
                horario = detalhes.get("time_of_day")

            lista_evolucoes.append(
                {
                    "chain_id": id_cadeia,
                    "de_id": de_id,
                    "para_id": para_id,
                    "metodo": metodo,
                    "nivel_minimo": detalhes.get("min_level"),
                    "item_usado": item_usado,
                    "item_segurado": item_segurado,
                    "felicidade_minima": detalhes.get("min_happiness"),
                    "horario": horario,
                    "local": local,
                    "golpe_conhecido": golpe,
                    "tipo_golpe_conhecido": tipo_golpe,
                }
            )

            processar_cadeia(proximo, id_cadeia)

  
    processar_cadeia(item["chain"], item["id"])
    return pd.DataFrame(lista_evolucoes)


df_raw = pd.read_json("../data/raw/evolution_pokemon.json")


list_dfs = df_raw.apply(extract_evolutions, axis=1)
df = pd.concat(list_dfs.tolist(), ignore_index=True)


df = df[
    [
        "chain_id",
        "de_id",
        "para_id",
        "metodo",
        "nivel_minimo",
        "item_usado",
        "item_segurado",
        "felicidade_minima",
        "horario",
        "local",
        "golpe_conhecido",
        "tipo_golpe_conhecido",
    ]
].sort_values(by=["chain_id", "de_id"])

df.to_csv("../data/cleaned/evolucoes.csv", index=False)

