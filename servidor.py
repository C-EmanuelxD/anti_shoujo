from flask import Flask, request, jsonify # type: ignore
from flask_cors import CORS # type: ignore
import dataReceive
import json

app = Flask(__name__)
CORS(app)

@app.route('/receive', methods=['POST'])
def receive_tags():
    try:
        dados = request.get_json()
        lista_de_tags = dados.get('lista')

        if not lista_de_tags or not isinstance(lista_de_tags, list):
            return jsonify({"status": "erro", "mensagem": "A chave 'tags' deve ser uma lista de nomes e não pode estar vazia."}), 400

        print(f"Servidor recebeu a seguinte lista de nomes: {lista_de_tags}")

        # Chama a nossa nova função para buscar e tratar os dados
        dataReceive.gera_json(lista_de_tags)
        itens_para_frontend = dataReceive.trata_entradas()
        print(itens_para_frontend)

        

        print(f"Enviando {len(itens_para_frontend)} itens formatados para o frontend.")

        # Retorna a lista de itens prontos para o JavaScript
        return jsonify({
            "status": "sucesso", 
            "mensagem": "Dados buscados e processados!",
            "createdItems": itens_para_frontend # A chave que o seu JS espera
        }), 200

    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)