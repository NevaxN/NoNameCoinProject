import sys
import os

sys.path.append(os.path.dirname(os.getcwd()))

import random
import threading

from flask import Flask, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dataclasses import dataclass
from datetime import datetime, timedelta
import requests

from util.status_transacao import STATUS_TRANSACAO_CONCLUIDA, STATUS_NAO_APROVADA, STATUS_NAO_EXECUTADA

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


@dataclass
class Cliente(db.Model):
    id: int
    nome: str
    senha: int
    qtdMoeda: int

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(20), unique=False, nullable=False)
    senha = db.Column(db.String(20), unique=False, nullable=False)
    qtdMoeda = db.Column(db.Integer, unique=False, nullable=False)


@dataclass
class Seletor(db.Model):
    id: int
    nome: str
    ip: str

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(20), unique=False, nullable=False)
    ip = db.Column(db.String(15), unique=False, nullable=False)


@dataclass
class Transacao(db.Model):
    id: int
    remetente: int
    recebedor: int
    valor: int
    horario: datetime
    status: int

    id = db.Column(db.Integer, primary_key=True)
    remetente = db.Column(db.Integer, unique=False, nullable=False)
    recebedor = db.Column(db.Integer, unique=False, nullable=False)
    valor = db.Column(db.Integer, unique=False, nullable=False)
    horario = db.Column(db.DateTime, unique=False, nullable=False)
    status = db.Column(db.Integer, unique=False, nullable=False)


with app.app_context():
    db.create_all()


@app.route("/")
def index():
    return jsonify(['API sem interface do banco!'])


@app.route('/cliente', methods=['GET'])
def ListarCliente():
    clientes = Cliente.query.all()
    return jsonify(clientes)


@app.route('/cliente/<string:nome>/<string:senha>/<int:qtdMoeda>', methods=['POST'])
def InserirCliente(nome, senha, qtdMoeda):
    if request.method == 'POST' and nome != '' and senha != '' and qtdMoeda != '':
        objeto = Cliente(nome=nome, senha=senha, qtdMoeda=qtdMoeda)
        db.session.add(objeto)
        db.session.commit()
        return jsonify(objeto)
    else:
        return jsonify(['Method Not Allowed'])


@app.route('/cliente/<int:id>', methods=['GET'])
def UmCliente(id):
    if (request.method == 'GET'):
        objeto = Cliente.query.get(id)
        return jsonify(objeto)
    else:
        return jsonify(['Method Not Allowed'])


@app.route('/cliente/<int:id>/<int:qtdMoedas>', methods=["POST"])
def EditarCliente(id, qtdMoedas):
    if request.method == 'POST':
        try:
            cliente = Cliente.query.filter_by(id=id).first()

            if cliente is None:
                return jsonify({"message": "Cliente não encontrado"}), 404

            cliente.qtdMoedas = qtdMoedas
            db.session.commit()
            return jsonify({"message": "Alteração feita com sucesso"}), 200
        except Exception as e:
            app.logger.error(f"Erro ao atualizar o cliente: {e}")
            return jsonify({"message": "Atualização não realizada"}), 500

    else:
        return jsonify({"message": "Método não permitido"}), 405


@app.route('/cliente/<int:id>', methods=['DELETE'])
def ApagarCliente(id):
    if (request.method == 'DELETE'):
        objeto = Cliente.query.get(id)
        db.session.delete(objeto)
        db.session.commit()

        data = {
            "message": "Cliente Deletado com Sucesso"
        }

        return jsonify(data)
    else:
        return jsonify(['Method Not Allowed'])


@app.route('/seletor', methods=['GET'])
def ListarSeletor():
    if (request.method == 'GET'):
        produtos = Seletor.query.all()
        return jsonify(produtos)


@app.route('/seletor/<string:nome>/<string:ip>', methods=['POST'])
def InserirSeletor(nome, ip, saldo):
    if request.method == 'POST' and nome != '' and ip != '':
        objeto = Seletor(nome=nome, ip=ip)
        db.session.add(objeto)
        db.session.commit()
        return jsonify(objeto)
    else:
        return jsonify(['Method Not Allowed'])


@app.route('/seletor/<int:id>', methods=['GET'])
def UmSeletor(id):
    if (request.method == 'GET'):
        produto = Seletor.query.get(id)
        return jsonify(produto)
    else:
        return jsonify(['Method Not Allowed'])


@app.route('/seletor/<int:id>/<string:nome>/<string:ip>', methods=["POST"])
def EditarSeletor(id, nome, ip):
    if request.method == 'POST':
        try:
            seletor = Seletor.query.filter_by(id=id).first()
            if seletor is None:
                return jsonify({"message": "Seletor não encontrado"}), 404

            seletor.nome = nome
            seletor.ip = ip
            db.session.commit()
            return jsonify(seletor)
        except Exception as e:
            data = {
                "message": f"Atualização não realizada; {e}",
            }
            return jsonify(data)
    else:
        return jsonify(['Method Not Allowed'])


@app.route('/seletor/<int:id>', methods=['DELETE'])
def ApagarSeletor(id):
    if (request.method == 'DELETE'):
        objeto = Seletor.query.get(id)
        db.session.delete(objeto)
        db.session.commit()

        data = {
            "message": "Validador Deletado com Sucesso"
        }

        return jsonify(data)
    else:
        return jsonify(['Method Not Allowed'])


@app.route('/hora', methods=['GET'])
def horario():
    current_time = datetime.now()
    return jsonify({'horario': current_time})


@app.route('/transacoes', methods=['GET'])
def ListarTransacoes():
    if (request.method == 'GET'):
        transacoes = Transacao.query.all()
        return jsonify(transacoes)


@app.route('/transacoes/<int:rem>/<int:reb>/<int:valor>', methods=['POST'])
def CriaTransacao(rem, reb, valor):
    remetente = Cliente.query.get(rem)
    recebedor = Cliente.query.get(reb)

    if remetente is None:
        return jsonify({"message": "Remetente não encontrado"}), 404
    if recebedor is None:
        return jsonify({"message": "Recebedor não encontrado"}), 404

    if remetente.qtdMoeda < valor:
        return jsonify({"message": "Saldo insuficiente"}), 400

    um_minuto_atras = datetime.now() - timedelta(minutes=1)
    transacoes_recentes = Transacao.query.filter(Transacao.remetente == rem,
                                                 Transacao.horario >= um_minuto_atras).count()

    if transacoes_recentes >= 10:
        return jsonify({"message": "Limite de transações por minuto excedido"}), 429

    transacao = Transacao(remetente=rem, recebedor=reb, valor=valor, status=STATUS_NAO_EXECUTADA,
                          horario=datetime.now())
    db.session.add(transacao)
    db.session.commit()

    seletores = Seletor.query.order_by(Seletor.saldo.desc()).limit(3).all()

    def enviar_validacao(transacao, validadores):
        respostas = []
        for seletor in validadores:
            url = f'http://{seletor.ip}/transacoes/validar'
            try:
                response = requests.post(url,
                                         json={"id": transacao.id, "remetente": rem, "recebedor": reb, "valor": valor,
                                               "horario": transacao.horario.isoformat()})
                if response.status_code == 200:
                    respostas.append(response.json())
            except Exception as e:
                app.logger.error(f"Erro ao enviar transação para o seletor {seletor.ip}: {e}")

        validacoes_positivas = sum(1 for resp in respostas if resp.get('status') == STATUS_TRANSACAO_CONCLUIDA)

        if validacoes_positivas >= 2:
            transacao.status = STATUS_TRANSACAO_CONCLUIDA
            remetente.qtdMoeda -= valor
            recebedor.qtdMoeda += valor
        else:
            transacao.status = STATUS_NAO_APROVADA

        db.session.commit()
        return transacao.status

    # Enviar validação de forma síncrona e aguardar o resultado
    status_final = enviar_validacao(transacao, seletores)

    return jsonify({"id": transacao.id, "status": status_final})


@app.route('/transacoes/<int:id>', methods=['GET'])
def VerificarStatusTransacao(id):
    transacao = Transacao.query.get(id)
    if transacao is None:
        return jsonify({"message": "Transação não encontrada"}), 404
    return jsonify({"status": transacao.status})


@app.route('/transacoes/<int:id>/<int:status>', methods=["POST"])
def EditaTransacao(id, status):
    if request.method == 'POST':
        try:
            objeto = Transacao.query.filter_by(id=id).first()
            db.session.commit()
            objeto.id = id
            objeto.status = status
            db.session.commit()
            return jsonify(objeto)
        except Exception as e:
            data = {
                "message": "transação não atualizada"
            }
            return jsonify(data)
    else:
        return jsonify(['Method Not Allowed'])


'''@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404'''

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

app.run(host='0.0.0.0', debug=True)
