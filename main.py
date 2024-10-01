#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import uuid
from flask import Flask, jsonify, request, render_template
from datetime import datetime
import random

app = Flask(__name__)

# Ler o JSON de um arquivo externo
def load_data():
    with open('dispositivos.json') as f:
        return json.load(f)


@app.route('/dispositivos', methods=['GET'])
def get_dispositivos():
    return jsonify(load_data())


# construir as funcionalidades
@app.route('/')
def homepage():
    return render_template("homepage.html")


@app.route('/lista_dispositivos_cadastrados')
def lista_dispositivos_cadastrados():
    data = load_data()
    return render_template('dispositivos.html', data=data)

@app.route('/busca_status_dispositivo/<int:codigo>', methods=['GET'])
def get_status(codigo):
    data = load_data()
    # Encontrar o status com base no código fornecido
    for item in data:
        if item['codigo'] == codigo:
            return jsonify({"codigo": codigo, "nome": item['nome'], "status": item['status']})
    # Se o código não for encontrado
    return jsonify({"error": "Código não encontrado"}), 404


@app.route('/altera_status_dispositivo', methods=['PUT'])
def update_status():
    nome = request.args.get('nome')  # Obtém o parâmetro 'nome' da URL
    novo_status = request.args.get('status')  # Obtém o parâmetro 'status' da URL

    if not nome or novo_status is None:
        return jsonify({"error":
                            "Parâmetros 'nome' e 'status' são necessários"}), 400

    if novo_status not in ['0', '1']:
        return jsonify({"error": "O status deve ser 0 ou 1"}), 400

    indice = buscar_por_nome(nome)
    if indice is not None:
        # Atualizar o status no JSON
        dispositivos["status"][str(indice)] = int(novo_status)

        # Salvar as alterações de volta no arquivo JSON
        with open('dispositivos.json', 'w') as file:
            json.dump(dispositivos, file, indent=4)

        return jsonify(
            {"message": f"Status de '{nome}' atualizado para {novo_status}"}), 200
    else:
        return jsonify({"error": "Nome não encontrado"}), 404


@app.route('/get-pagamento', methods=['GET'])
def get_data():
    rModality = random.choice([1, 3, 5, 6, 7, 47])
    if rModality == 6 or rModality == 7:
        rInstallmnt = random.randint(1, 12)
    else:
        rInstallmnt = 0
    data = {
        "id": str(uuid.uuid4()),  # Gera um UUID aleatório
        "store": 1,
        "date": datetime.now().strftime('%Y-%m-%d'),  # Data atual
        "time": datetime.now().strftime('%H:%M:%S'),  # Hora atual
        "cupon": random.randint(1, 99999),  # Gera um número aleatório entre 1 e 99999
        "sequence": random.randint(1, 10),  # Gera um número aleatório entre 1 e 10
        "action": "create",
        "state": 1,
        "checkout": "602",
        "opercode": 1000,
        "opername": "Suporte Kw",
        "brand": "VISA",
        "duedate": "",
        "modality": rModality,
        "installmnt": rInstallmnt,
        "amount": random.randint(100, 30000),
        "data": {
            "termid": "",
            "datetime": "",
            "result": "",
            "retcode": "",
            "retmsg": "",
            "cardno": "",
            "cardholder": "",
            "nsu": "",
            "autoriz": "",
            "acquirer": "",
            "brand": "",
            "receipt": ""
        }
    }

    return jsonify(data)


# rodar a api
app.run(host='0.0.0.0', port=5000)
