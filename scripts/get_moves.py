import json
import requests

url_todos = "https://pokeapi.co/api/v2/move?limit=10000"
response = requests.get(url_todos)
dados_lista = response.json()

moves_list = dados_lista['results']
total_moves = len(moves_list)

print(f"total de golpes encontrados: {total_moves}")

lista_json = []

for index, move_info in enumerate(moves_list, 1):
    move_url = move_info['url']
    
    try:
        res = requests.get(move_url)
        if res.status_code == 200:
            lista_json.append(res.json())

            print(f"[{index}/{total_moves}] golpe '{move_info['name']}' baixado com sucesso")
        else:
            print(f"[{index}/{total_moves}] erro ao baixar '{move_info['name']}': status {res.status_code}")
    except Exception as e:
        print(f"erro na requisição de '{move_info['name']}': {e}")

# 3. Salva todos no arquivo JSON
caminho_arquivo = "../data/raw/move_pokemon.json"
with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo:
    json.dump(lista_json, fp=arquivo, indent=4, ensure_ascii=False)

print(f"{len(lista_json)} golpes salvos com sucesso")
