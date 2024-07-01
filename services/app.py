import sys
import os

sys.path.append(os.path.dirname(os.getcwd()))

import random
import threading
from time import sleep
from flask import Flask, request, jsonify
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
    senha: str
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


@dataclass
class Validador(db.Model):
    id: int
    nome: str
    saldo: int
    flags: int
    hold: int
    chave_unica: str
    selecoes_consecutivas: int
    transacoes_coerentes: int
    horario_ultima_transacao: datetime

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(20), unique=False, nullable=False)
    chave_unica = db.Column(db.String(50), unique=True, nullable=False)
    saldo = db.Column(db.Integer, nullable=False, default=50)
    flags = db.Column(db.Integer, nullable=False, default=0)
    hold = db.Column(db.Integer, nullable=False, default=0)
    selecoes_consecutivas = db.Column(db.Integer, nullable=False, default=0)
    transacoes_coerentes = db.Column(db.Integer, nullable=False, default=0)
    horario_ultima_transacao = db.Column(db.DateTime, unique=False, nullable=False)


with app.app_context():
    db.create_all()


@app.route("/")
def index():
    return jsonify({'message': 'API sem interface do banco!'})


@app.route('/cliente', methods=['GET'])
def ListarCliente():
    clientes = Cliente.query.all()
    return jsonify({"Clientes": clientes})


@app.route('/cliente/<string:nome>/<string:senha>/<int:qtdMoeda>', methods=['POST'])
def InserirCliente(nome, senha, qtdMoeda):
    if request.method == 'POST' and nome != '' and senha != '' and qtdMoeda != '':
        objeto = Cliente(nome=nome, senha=senha, qtdMoeda=qtdMoeda)
        db.session.add(objeto)
        db.session.commit()
        return jsonify({"Cliente": objeto})
    else:
        return jsonify({'message': 'Method Not Allowed'}), 405


@app.route('/cliente/<int:id>', methods=['GET'])
def UmCliente(id):
    if request.method == 'GET':
        objeto = Cliente.query.get(id)
        if not objeto:
            return jsonify({"message": "Cliente não encontrado"}), 404
        return jsonify({"Cliente": objeto})
    else:
        return jsonify({'message': 'Method Not Allowed'}), 405


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
    if request.method == 'DELETE':
        objeto = Cliente.query.get(id)
        if not objeto:
            return jsonify({"message": "Cliente não encontrado"}), 404
        db.session.delete(objeto)
        db.session.commit()
        return jsonify({"message": "Cliente Deletado com Sucesso"})
    else:
        return jsonify({'message': 'Method Not Allowed'}), 405


@app.route('/seletor', methods=['GET'])
def ListarSeletor():
    if request.method == 'GET':
        seletores = Seletor.query.all()
        return jsonify({"Seletores:" : seletores})


@app.route('/seletor/<string:nome>/<string:ip>', methods=['POST'])
def InserirSeletor(nome, ip):
    if request.method == 'POST' and nome != '' and ip != '':
        objeto = Seletor(nome=nome, ip=ip)
        db.session.add(objeto)
        db.session.commit()
        return jsonify({"Seletor:": objeto})
    else:
        return jsonify({'message': 'Method Not Allowed'}), 405


@app.route('/seletor/<int:id>', methods=['GET'])
def UmSeletor(id):
    if request.method == 'GET':
        seletor = Seletor.query.get(id)
        if not seletor:
            return jsonify({"message": "Seletor não encontrado"}), 404
        return jsonify({"Seletor:": seletor})
    else:
        return jsonify({'message': 'Method Not Allowed'}), 405


@app.route('/seletor/<int:id>/<string:nome>/<string:ip>', methods=["POST"])
def EditarSeletor(id, nome, ip):
    if request.method == 'POST':
        try:
            seletor = Seletor.query.filter_by(id=id).first()
            if not seletor:
                return jsonify({"message": "Seletor não encontrado"}), 404

            seletor.nome = nome
            seletor.ip = ip
            db.session.commit()
            return jsonify({"Seletor:": seletor})
        except Exception as e:
            data = {
                "message": f"Atualização não realizada; {e}",
            }
            return jsonify(data), 500
    else:
        return jsonify({'message': 'Method Not Allowed'}), 405


@app.route('/seletor/<int:id>', methods=['DELETE'])
def ApagarSeletor(id):
    if request.method == 'DELETE':
        seletor = Seletor.query.get(id)
        if not seletor:
            return jsonify({"message": "Seletor não encontrado"}), 404
        db.session.delete(seletor)
        db.session.commit()
        return jsonify({"message": "Seletor Deletado com Sucesso"})
    else:
        return jsonify({'message': 'Method Not Allowed'}), 405


@app.route('/hora', methods=['GET'])
def horario():
    current_time = datetime.now()
    return jsonify({'horario': current_time})


@app.route('/transacoes', methods=['GET'])
def ListarTransacoes():
    if request.method == 'GET':
        transacoes = Transacao.query.all()
        return jsonify({"Transações:": transacoes})


@app.route('/transacoes/<int:rem>/<int:reb>/<int:valor>', methods=['POST'])
def CriaTransacao(rem, reb, valor):
    try:
        remetente = Cliente.query.get(rem)
        recebedor = Cliente.query.get(reb)

        if not remetente:
            return jsonify({"message": "Remetente não encontrado"}), 404
        if not recebedor:
            return jsonify({"message": "Recebedor não encontrado"}), 404

        if remetente.qtdMoeda < valor:
            return jsonify({"message": "Saldo insuficiente"}), 400

        um_minuto_atras = datetime.now() - timedelta(minutes=1)
        transacoes_recentes = Transacao.query.filter(Transacao.remetente == rem,
                                             Transacao.horario >= um_minuto_atras).count()

        if transacoes_recentes >= 100:
            return jsonify({"message": "Limite de transações por minuto excedido"}), 429

        transacao = Transacao(remetente=rem, recebedor=reb, valor=valor, status=STATUS_NAO_EXECUTADA,
                              horario=datetime.now())
        db.session.add(transacao)
        db.session.commit()

        # Obter os validadores
        validadores = Seletor.query.all()

        # Esperar até que pelo menos três validadores estejam disponíveis, ou até um minuto
        tempo_limite = datetime.now() + timedelta(minutes=1)
        while len(validadores) < 3 and datetime.now() < tempo_limite:
            app.logger.info(
                f"Esperando validadores. Tempo restante: {(tempo_limite - datetime.now()).seconds} segundos")
            sleep(1)
            validadores = Seletor.query.all()

        if len(validadores) < 3:
            return jsonify({"message": "Não há validadores suficientes disponíveis"}), 503

        validadores_selecionados = random.choices(validadores, k=3)

        # Chamar a função de validação com os IDs do remetente e recebedor
        status_final = enviar_validacao(transacao, validadores_selecionados, remetente, recebedor)

        # Retornar o status final da transação
        return jsonify({"id": transacao.id, "status": status_final})

    except Exception as e:
        app.logger.error(f"Erro ao criar transação: {e}")
        return jsonify({"message": "Erro ao criar transação"}), 500


@app.route('/transacoes/<int:id>/<int:status>', methods=["POST"])
def EditaTransacao(id, status):
    try:
        transacao = Transacao.query.filter_by(id=id).first()
        if not transacao:
            return jsonify({"message": "Transação não encontrada"}), 404

        transacao.status = status
        db.session.commit()

        remetente = Cliente.query.get(transacao.remetente)
        recebedor = Cliente.query.get(transacao.recebedor)

        if not remetente or not recebedor:
            return jsonify({"message": "Remetente ou recebedor não encontrado"}), 404

        # Obter os validadores
        seletores = Seletor.query.all()
        validadores = random.sample(seletores, min(3, len(seletores)))

        # Chamar a função de validação com os IDs do remetente e recebedor
        status_final = enviar_validacao(transacao, validadores, remetente, recebedor)

        return jsonify({"id": transacao.id, "status": status_final})

    except Exception as e:
        app.logger.error(f"Erro ao editar transação: {e}")
        return jsonify({"message": "Erro ao editar transação"}), 500


def enviar_validacao(transacao, validadores, rem, rec):
    try:
        respostas = []
        for validador in validadores:
            status = 0
            #status = validador.validar_transacao(transacao, validador)
            respostas.append({"validador_id": validador.id, "status": status})

            if status == STATUS_NAO_APROVADA:
                validador.atualizar_flags("Transação não aprovada")
            elif validador.chave_unica != transacao.chave_unica:
                return jsonify({"message": "Chave única do validador inválida"}), 400

        # Contar validações positivas
        validacoes_positivas = sum(1 for resp in respostas if resp.get('status') == STATUS_TRANSACAO_CONCLUIDA)

        # Decidir o status final da transação com base nas validações
        if validacoes_positivas >= 2:
            transacao.status = STATUS_TRANSACAO_CONCLUIDA
            rem.qtdMoeda -= transacao.valor
            rec.qtdMoeda += transacao.valor
        else:
            transacao.status = STATUS_NAO_APROVADA

        db.session.commit()
        return transacao.status

    except Exception as e:
        db.session.rollback()
        return STATUS_NAO_APROVADA


@app.route('/transacoes/<int:id>', methods=['GET'])
def VerificarStatusTransacao(id):
    transacao = Transacao.query.get(id)
    if not transacao:
        return jsonify({"message": "Transação não encontrada"}), 404
    return jsonify({"status": transacao.status})


@app.route('/validador/cadastrar', methods=['POST'])
def cadastrar_validador():
    data = request.get_json()
    nome = data.get('nome')
    chave_unica = data.get('chave_unica')

    if not nome or not chave_unica:
        return jsonify({"message": "Dados incompletos"}), 400

    validador = Validador(nome=nome, chave_unica=chave_unica)
    db.session.add(validador)
    db.session.commit()

    return jsonify({"message": "Validador cadastrado com sucesso", "id": validador.id}), 201


@app.route('/validador/validar', methods=['POST'])
def validar_transacao():
    data = request.get_json()
    id_validador = data.get('id_validador')
    id_transacao = data.get('id_transacao')

    validador = Validador.query.get(id_validador)
    transacao = Transacao.query.get(id_transacao)

    if not validador or not transacao:
        return jsonify({"message": "Validador ou transação não encontrados"}), 404

    status = validador.validar_transacao(transacao)

    return jsonify({"status": status})


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
