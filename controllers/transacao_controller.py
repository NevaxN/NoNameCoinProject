'''
Mudança no controller 

Explicacao do criaTransacao

Verifica se o remetente e o recebedor existem no banco de dados (Cliente.query.get(rem) e Cliente.query.get(reb)).
Verifica se o remetente possui saldo suficiente (if remetente.qtdMoeda < valor:).
Inicia uma transação no banco de dados (db.session.begin()).
Atualiza os saldos do remetente e do recebedor.
Cria um novo objeto de transação (Transacao) com os dados fornecidos.
Adiciona a transação ao banco de dados (db.session.add(objeto)).
Notifica os seletores (seletors) sobre a nova transação através de requisições POST para seus respectivos IPs.
Comita as alterações no banco de dados (db.session.commit()).
'''
import sys
import os

sys.path.append(os.path.dirname(os.getcwd()))

from flask import jsonify
from datetime import datetime
import requests
from services.app import Transacao, Cliente, Seletor


def listar_transacoes():
    transacoes = Transacao.query.all()
    return jsonify(transacoes), 200

def cria_transacao(rem, reb, valor):
    remetente = Cliente.query.get(rem)
    recebedor = Cliente.query.get(reb)

    if remetente is None or recebedor is None:
        return jsonify({"message": "Remetente ou recebedor não encontrado"}), 404

    if remetente.qtdMoeda < valor:
        return jsonify({"message": "Saldo insuficiente"}), 400

    try:
        # Iniciar a transação
        db.session.begin()

        # Atualizar os saldos dos clientes
        remetente.qtdMoeda -= valor
        recebedor.qtdMoeda += valor

        # Criar a transação
        objeto = Transacao(remetente=rem, recebedor=reb, valor=valor, status=0, horario=datetime.now())
        db.session.add(objeto)
        db.session.commit()

        # Notificar os seletores
        seletores = Seletor.query.all()
        for seletor in seletores:
            url = f'http://{seletor.ip}/transacoes'
            try:
                requests.post(url, json={"remetente": rem, "recebedor": reb, "valor": valor, "status": 0, "horario": datetime.now().isoformat()})
            except requests.exceptions.RequestException as e:
                app.logger.error(f"Erro ao notificar seletor {seletor.nome}: {e}")

        # Commit da transação
        db.session.commit()

        return jsonify(objeto), 201

    except Exception as e:
        # Rollback em caso de erro
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

def uma_transacao(id):
    objeto = Transacao.query.get(id)
    if objeto is None:
        return jsonify({"message": "Transação não encontrada"}), 404
    return jsonify(objeto), 200

def edita_transacao(id, status):
    objeto = Transacao.query.filter_by(id=id).first()
    if objeto is None:
        return jsonify({"message": "Transação não encontrada"}), 404

    objeto.status = status
    try:
        db.session.commit()
        return jsonify(objeto), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500