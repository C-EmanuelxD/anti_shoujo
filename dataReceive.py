import requests # type: ignore
import json
import re

def gera_json(entrada_nome: list):
    valores = {}
    nome = 'entradas.json'
    url = 'https://graphql.anilist.co'
    query = '''
            query ($nome: String){
                Media(type: MANGA, search: $nome){
                    genres
                    chapters
                    volumes
                    format
                    description
                    countryOfOrigin
                    coverImage {
                        medium
                    }
                    tags {
                        name
                    }
                }
            }
            '''

    with requests.Session() as session:
        for i in entrada_nome:
            variables = {'nome': i}
            response = session.post(url, json={'query': query, 'variables': variables})
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



def filtra_tags(entradas):
    filtro = {"Male Harem", "Age Gap", "Boys' Love", "Female Protagonist", 
              "LGBTQ+ Themes", "Shoujo", "Office Lady", "Harem"}

    # dict comprehension otimizado
    entradas_filtradas = {
        nome_manga: dados
        for nome_manga, dados in entradas.items()
        if not filtro & {tag['name'] for tag in dados['data']['Media']['tags']}
    }

    return entradas_filtradas

        



def trata_entradas():
    print("\n--- Tratando os dados do arquivo JSON ---")
    data_manga = []
    try:
        with open('entradas.json', 'r', encoding='utf-8') as arquivo:
            entradas = json.load(arquivo)
            entradas = filtra_tags(entradas)
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
