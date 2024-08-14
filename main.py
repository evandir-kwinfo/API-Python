#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# Ler o JSON de um arquivo externo
with open('dispositivos.json', 'r') as file:
  dados = json.load(file)

# Função auxiliar para buscar informações por nome
def buscar_por_nome(nome):
  for i in range(len(dados["nome"])):
    if dados["nome"][str(i)] == nome:
      return i  # Retorna o índice onde o nome foi encontrado
  return None

# construir as funcionalidades
@app.route('/')
def homepage():

  return render_template("homepage.html")

@app.route('/lista_dispositivos_cadastrados')
def lista_dispositivos_cadastrados():
  # Criar um array combinando os valores do JSON
  resultado = [{
      "nome": dados["nome"][str(i)],
      "status": dados["status"][str(i)]
  } for i in range(len(dados["nome"]))]

  # Retorna o array como JSON
  return render_template('dispositivos.html', dispositivos=resultado)


@app.route('/busca_status_dispositivo', methods=['GET'])
def get_dados():
  nome = request.args.get('nome')  # Obtém o parâmetro 'nome' da URL

  if nome:
    indice = buscar_por_nome(nome)
    if indice is not None:
      resultado = {"nome": nome, "status": dados["status"][str(indice)]}
      return jsonify(resultado)
    else:
      return jsonify({"error": "Nome não encontrado"}), 404
  else:
    return jsonify({"error": "Parâmetro 'nome' é necessário"}), 400


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
    dados["status"][str(indice)] = int(novo_status)

    # Salvar as alterações de volta no arquivo JSON
    with open('dados.json', 'w') as file:
      json.dump(dados, file, indent=4)

    return jsonify(
        {"message": f"Status de '{nome}' atualizado para {novo_status}"}), 200
  else:
    return jsonify({"error": "Nome não encontrado"}), 404


# rodar a api
app.run(host='0.0.0.0', port=5000)
