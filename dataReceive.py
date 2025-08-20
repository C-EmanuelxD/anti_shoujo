import requests # type: ignore
import json
import re

def gera_json(entrada_nome):
    valores = {}
    nome = 'entradas.json'

    for i in entrada_nome:
        query = '''
        query ($nome: String){
            Media(type: MANGA, search: $nome, tag_not_in: ["Male Harem", "Age Gap", "Boys' Love", "Female Protagonist", "LGBTQ+ Themes", "Shoujo", "Office Lady", "Harem"]){
                genres
                chapters
                volumes
                format
                description
                countryOfOrigin
                coverImage {
                    medium
                }
            }
        }
        '''

        variables = {'nome': i}

        url = 'https://graphql.anilist.co'

        response = requests.post(url, json={'query': query, 'variables': variables})

        if response.status_code == 200:
            print("Sucesso na requisição!")
            json_resposta = response.json()
            valores[i] = json_resposta
        else:
            print(f"Erro de requisição. CODIGO: {response.status_code}")
            json_erro = response.json()
            with open("log_erro.json", 'w', encoding='utf-8') as log:
                json.dump(json_erro, log, indent=4, ensure_ascii=False)

    with open(nome, 'w', encoding='utf-8') as arquivo:
        json.dump(valores, arquivo, indent=4, ensure_ascii=False)
        arquivo.write("\n")

def trata_entradas():
    print("\n--- Tratando os dados do arquivo JSON ---")
    data_manga = []
    try:
        with open('entradas.json', 'r', encoding='utf-8') as arquivo:
            entradas = json.load(arquivo)
            
            for nome_manga, dados_manga in entradas.items():
                print(f"=========================================")
                print(f"Tratando entrada: {nome_manga.upper()}")
                print(f"=========================================")

                if not dados_manga:
                    print("--> Nenhum dado encontrado para este título.\n")
                    continue

                capitulos = dados_manga['data']['Media']['chapters'] or "Não disponível"

                descricao = dados_manga['data']['Media'].get('description', 'Descrição não encontrada.')
                if descricao:
                    descricao_limpa = re.sub(r'<[^>]+>', '', descricao)

                url_imagem = dados_manga['data']['Media']['coverImage'].get('medium', 'Imagem não disponível')

                data_manga.append({
                    "titulo": nome_manga,
                    "capitulos": capitulos,
                    "descricao": descricao_limpa.strip(),
                    "url_imagem": url_imagem
                    })
        return data_manga

    except FileNotFoundError:
        print("Erro: O arquivo 'entradas.json' não foi encontrado. Execute 'gera_json()' primeiro.")
    except json.JSONDecodeError:
        print("Erro: O arquivo 'entradas.json' está mal formatado ou vazio.")
