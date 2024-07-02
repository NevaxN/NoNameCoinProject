import sys
import os

sys.path.append(os.path.dirname(os.getcwd()))

import random
from time import sleep
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dataclasses import dataclass
from datetime import datetime, timedelta
from string import ascii_letters

from util.status_transacao import STATUS_TRANSACAO_CONCLUIDA, STATUS_NAO_APROVADA, STATUS_NAO_EXECUTADA

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

CHAVES = {}


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
    saldo: int

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(20), unique=False, nullable=False)
    ip = db.Column(db.String(15), unique=False, nullable=False)
    saldo = db.Column(db.Integer, unique=False, nullable=False)


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
    expulsoes: int

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(20), unique=False, nullable=False)
    chave_unica = db.Column(db.String(50), unique=True, nullable=False)
    saldo = db.Column(db.Integer, nullable=False, default=50)
    flags = db.Column(db.Integer, nullable=False, default=0)
    hold = db.Column(db.Integer, nullable=False, default=0)
    selecoes_consecutivas = db.Column(db.Integer, nullable=False, default=0)
    transacoes_coerentes = db.Column(db.Integer, nullable=False, default=0)
    horario_ultima_transacao = db.Column(db.DateTime, unique=False, nullable=False)
    expulsoes = db.Column(db.Integer, default=0)


@dataclass
class EleicaoLog(db.Model):
    id: int
    timestamp: datetime
    acao: str
    detalhes: str

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    acao = db.Column(db.String(100), nullable=False)
    detalhes = db.Column(db.String(250), nullable=False)


with app.app_context():
    db.create_all()


@app.route("/")
def index():
    # Rota principal da API. Retorna uma mensagem de boas-vindas.
    return jsonify({'message': 'API sem interface do banco!'})


@app.route('/cliente', methods=['GET'])
def ListarCliente():
    clientes = Cliente.query.all() # Consulta todos os clientes no banco de dados.
    return jsonify({"Clientes": clientes}) # Retorna a lista de clientes em formato JSON.


@app.route('/cliente/<string:nome>/<string:senha>/<int:qtdMoeda>', methods=['POST'])
 # Rota para inserir um novo cliente. Recebe nome, senha e quantidade de moeda como parâmetros.
def InserirCliente(nome, senha, qtdMoeda):
    if request.method == 'POST' and nome != '' and senha != '' and qtdMoeda != '':
        # Verifica se o método é POST e os parâmetros não estão vazios.
        objeto = Cliente(nome=nome, senha=senha, qtdMoeda=qtdMoeda) # Cria um novo cliente.
        db.session.add(objeto) # Adiciona o cliente à sessão do banco de dados
        db.session.commit() # Salva as alterações no banco de dados.
        return jsonify({"Cliente": objeto}) # Retorna o cliente inserido em formato JSON.
    else:
        # Caso contrário, retorna um erro indicando que o método não é permitido.
        return jsonify({'message': 'Method Not Allowed'}), 405


@app.route('/cliente/<int:id>', methods=['GET'])
def UmCliente(id):
        # Rota para obter um cliente específico pelo ID.
    if request.method == 'GET':
        # Verifica se o método é GET.
        objeto = Cliente.query.get(id)# Consulta o cliente com o ID fornecido.
        # Se o cliente não for encontrado, retorna um erro 404.
        if not objeto:
            return jsonify({"message": "Cliente não encontrado"}), 404
        return jsonify({"Cliente": objeto})# Retorna o cliente encontrado em formato JSON.
    else:
        # Caso contrário, retorna um erro indicando que o método não é permitido.
        return jsonify({'message': 'Method Not Allowed'}), 405


@app.route('/cliente/<int:id>/<int:qtdMoedas>', methods=["POST"])
def EditarCliente(id, qtdMoedas):
    # Rota para editar a quantidade de moedas de um cliente específico.
    if request.method == 'POST':
        # Verifica se o método é POST.
        try:
            cliente = Cliente.query.filter_by(id=id).first()
            # Consulta o cliente com o ID fornecido.
            if cliente is None:
                return jsonify({"message": "Cliente não encontrado"}), 404
            # Se o cliente não for encontrado, retorna um erro 404.
            cliente.qtdMoedas = qtdMoedas # Atualiza a quantidade de moedas do cliente.
            db.session.commit() # Salva as alterações no banco de dados.
            return jsonify({"message": "Alteração feita com sucesso"}), 200
        except Exception as e: # Se ocorrer uma exceção, registra o erro e retorna uma mensagem de erro 500.
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
        seletores = Seletor.query.all() # Consulta todos os seletores no banco de dados.
        return jsonify({"Seletores:": seletores})


@app.route('/seletor/<string:nome>/<string:ip>/<int:saldo>', methods=['POST'])
def InserirSeletor(nome, ip, saldo):
    if request.method == 'POST' and nome != '' and ip != '' and saldo > 0:
        # Verifica se o método é POST e os parâmetros são válidos.
        objeto = Seletor(nome=nome, ip=ip, saldo=saldo) # Cria um novo seletor.
        db.session.add(objeto)  # Adiciona o seletor à sessão do banco de dados.
        db.session.commit() 
        return jsonify({"Seletor:": objeto})
    else:
        return jsonify({'message': 'Method Not Allowed'}), 405


@app.route('/seletor/<int:id>', methods=['GET'])
def UmSeletor(id):
    if request.method == 'GET':
        seletor = Seletor.query.get(id) # Consulta o seletor com o ID fornecido.
        if not seletor:
            return jsonify({"message": "Seletor não encontrado"}), 404
        return jsonify({"Seletor:": seletor})
    else:
        return jsonify({'message': 'Method Not Allowed'}), 405


@app.route('/seletor/<int:id>/<string:nome>/<string:ip>/<int:saldo>', methods=["POST"])
def EditarSeletor(id, nome, ip, saldo):
    if request.method == 'POST':
        try:
            seletor = Seletor.query.filter_by(id=id).first()  # Consulta o seletor com o ID fornecido.
            if not seletor:
                return jsonify({"message": "Seletor não encontrado"}), 404

            seletor.nome = nome # Atualiza o nome do seletor.
            seletor.ip = ip  # Atualiza o IP do seletor.
            seletor.saldo = saldo # Atualiza o saldo do seletor.
            db.session.commit() # Salva as alterações no banco de dados.
            return jsonify({"Seletor:": seletor}) # Retorna o seletor atualizado em formato JSON.
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
    current_time = datetime.utcnow()  # Obtém o horário atual em UTC.
    return jsonify({'horario': current_time.isoformat()})


@app.route('/transacoes', methods=['GET'])
def ListarTransacoes():
    if request.method == 'GET':
        transacoes = Transacao.query.all() # Consulta todas as transações no banco de dados.
        return jsonify({"Transações:": transacoes})


@app.route('/transacoes/<int:rem>/<int:reb>/<int:valor>', methods=['POST'])
def CriaTransacao(rem, reb, valor):
    # Rota para criar uma nova transação. Verifica a validade da transação e seleciona validadores.
    try:
        remetente = Cliente.query.get(rem) # Consulta o cliente remetente.
        recebedor = Cliente.query.get(reb) # Consulta o cliente recebedor.

        # Se o remetente não for encontrado, retorna um erro 404.
        if not remetente:
            return jsonify({"message": "Remetente não encontrado"}), 404
        if not recebedor:
            return jsonify({"message": "Recebedor não encontrado"}), 404

        if remetente.qtdMoeda < valor:
            return jsonify({"message": "Saldo insuficiente"}), 400

        um_minuto_atras = datetime.now() - timedelta(minutes=1) # Define o limite de um minuto.
        transacoes_recentes = Transacao.query.filter(Transacao.remetente == rem,
                                                     Transacao.horario >= um_minuto_atras).count()  # Conta transações recentes.

        if transacoes_recentes >= 100:
            return jsonify({"message": "Limite de transações por minuto excedido"}), 429

        transacao = Transacao(remetente=rem, recebedor=reb, valor=valor, status=STATUS_NAO_EXECUTADA,
                              horario=datetime.now())  # Cria uma nova transação com status não executada.
        db.session.add(transacao) # Adiciona a transação à sessão do banco de dados.
        db.session.commit()  # Salva as alterações no banco de dados.

        # Obter os validadores, ordenando por flags e saldo
        validadores = Validador.query.order_by(Validador.flags.asc(), Validador.saldo.desc()).all()

        # Esperar até que pelo menos três validadores estejam disponíveis, ou até um minuto
        tempo_limite = datetime.now() + timedelta(minutes=1)
        while len(validadores) < 3 and datetime.now() < tempo_limite:
            app.logger.info(
                f"Esperando validadores. Tempo restante: {(tempo_limite - datetime.now()).seconds} segundos")
            sleep(1)
            validadores = Validador.query.order_by(Validador.flags.asc(), Validador.saldo.desc()).all()

        if len(validadores) < 3:
            return jsonify({"message": "Não há validadores suficientes disponíveis"}), 503

        validadores_selecionados = []
        for validador in validadores:
            chance_selecao = 1.0  # 100% de chance inicialmente

            if validador.flags == 1:
                chance_selecao *= 0.5  # Reduz em 50% a chance de seleção
            elif validador.flags == 2:
                chance_selecao *= 0.25  # Reduz em 75% a chance de seleção

            if validador.hold > 0:
                continue  # Pula validadores em HOLD

            # Gerar um número aleatório entre 0 e 1 para decidir se seleciona o validador
            if random.random() < chance_selecao:
                validadores_selecionados.append(validador)

        # Limitar a seleção a 20% do total de validadores
        max_validadores = max(3, int(len(validadores) * 0.2))
        validadores_ordenados = sorted(validadores, key=lambda v: (v.flags, -v.saldo))

        # Selecionar os top `max_validadores` validadores
        validadores_selecionados = validadores_ordenados[:max_validadores]

        registrar_log('Seleção dos validadores',
                      f'Validadores selecionados: {[v.id for v in validadores_selecionados]}')

        # Exibir os validadores selecionados
        for validador in validadores_selecionados:
            print(f"Validador ID: {validador.id}, Flags: {validador.flags}, Saldo: {validador.saldo}")
            registrar_log('Detalhes do validador selecionado',
                          f'ID: {validador.id}, Flags: {validador.flags}, Saldo: {validador.saldo}')

        # Chamar a função de validação com os IDs do remetente e recebedor
        status_final = enviar_validacao(transacao, validadores_selecionados, remetente, recebedor)

        # Retornar o status final da transação
        return jsonify({"id": transacao.id, "status": status_final})

    except Exception as e:
        app.logger.error(f"Erro ao criar transação: {e}")
        return jsonify({"message": "Erro ao criar transação"}), 500


@app.route('/transacoes/<int:id>', methods=["POST"])
def ValidarTransacaoUnica(id):
    try:
        transacao = Transacao.query.filter_by(id=id).first()

        if not transacao:
            return jsonify({"message": "Transação não encontrada"}), 404

        db.session.commit()

        remetente = Cliente.query.get(transacao.remetente)
        recebedor = Cliente.query.get(transacao.recebedor)

        if not remetente or not recebedor:
            return jsonify({"message": "Remetente ou recebedor não encontrado"}), 404

        # Obter os validadores, ordenando por flags e saldo
        validadores = Validador.query.order_by(Validador.flags.asc(), Validador.saldo.desc()).all()

        # Esperar até que pelo menos três validadores estejam disponíveis, ou até um minuto
        tempo_limite = datetime.now() + timedelta(minutes=1)
        while len(validadores) < 3 and datetime.now() < tempo_limite:
            app.logger.info(
                f"Esperando validadores. Tempo restante: {(tempo_limite - datetime.now()).seconds} segundos")
            sleep(1)
            validadores = Validador.query.order_by(Validador.flags.asc(), Validador.saldo.desc()).all()

        if len(validadores) < 3:
            return jsonify({"message": "Não há validadores suficientes disponíveis"}), 503

        validadores_selecionados = []
        for validador in validadores:
            chance_selecao = 1.0  # 100% de chance inicialmente

            if validador.flags == 1:
                chance_selecao *= 0.5  # Reduz em 50% a chance de seleção
            elif validador.flags == 2:
                chance_selecao *= 0.25  # Reduz em 75% a chance de seleção

            # Gerar um número aleatório entre 0 e 1 para decidir se seleciona o validador
            if random.random() < chance_selecao:
                validadores_selecionados.append(validador)

        # registrar_log('Início da eleição', 'Iniciando o processo de eleição dos validadores.')

        max_validadores = max(3, int(len(validadores) * 0.2))
        validadores_ordenados = sorted(validadores, key=lambda v: (v.flags, -v.saldo))

        # Selecionar os top `max_validadores` validadores
        validadores_selecionados = validadores_ordenados[:max_validadores]

        registrar_log('Seleção dos validadores',
        f'Validadores selecionados: {[v.id for v in validadores_selecionados]}')

        # Exibir os validadores selecionados
        for validador in validadores_selecionados:
            print(f"Validador ID: {validador.id}, Flags: {validador.flags}, Saldo: {validador.saldo}")
            registrar_log('Detalhes do validador selecionado',
            f'ID: {validador.id}, Flags: {validador.flags}, Saldo: {validador.saldo}')

        # Chamar a função de validação com os IDs do remetente e recebedor
        status_final = enviar_validacao(transacao, validadores_selecionados, remetente, recebedor)

        return jsonify({"id": transacao.id, "status": status_final})

    except Exception as e:
        app.logger.error(f"Erro ao editar transação: {e}")
        return jsonify({"message": "Erro ao editar transação"}), 500


def enviar_validacao(transacao, validadores, rem, rec):
    try:
        respostas = [] # Lista para armazenar as respostas de cada validador.
        manter_chave_cheia() # Função para garantir que a chave está cheia.
        status_validadores = [] # Lista para armazenar o status de cada validador.
        seletor_id = 1 # ID do seletor (presumivelmente fixo para este exemplo).
        seletor = Seletor.query.get(seletor_id) # Consulta o seletor com o ID fornecido.

        # Itera sobre cada validador para verificar as regras de validação.
        for validador in validadores:
            status = 0
            # Verifica se a transação tem valor maior que o saldo do remetente.
            if transacao.valor > rem.qtdMoeda:
                print("Não Aprovada Valor")
                status = STATUS_NAO_APROVADA
            # Verifica se a chave única do validador é inválida.
            elif validador.chave_unica != CHAVES[str(validador.id)]:
                print("Não Aprovada Chave Unica")
                status = STATUS_NAO_APROVADA
            elif validador.saldo < 100:  # Exemplo de saldo mínimo
                print("Não Aprovada Saldo")
                status = STATUS_NAO_APROVADA
            elif validador.horario_ultima_transacao > transacao.horario > datetime.now():  # Exemplo de horário de
                # operação
                print("Não Aprovada Hora")
                status = STATUS_NAO_APROVADA
            # Verifica se o número de transações coerentes do validador é muito alto.
            elif validador.transacoes_coerentes > 100:
                status = STATUS_NAO_APROVADA
            else:
                status = STATUS_TRANSACAO_CONCLUIDA

            status_validadores.append(status)

            respostas.append({"validador_id": validador.id, "status": status})

            # Atualiza o horário da última transação do validador.
            validador.horario_ultima_transacao = datetime.now()

            # Atualiza o número de seleções consecutivas do validador.

            validador.selecoes_consecutivas += 1
            if validador.selecoes_consecutivas > 5:
                # Se o número de seleções consecutivas for maior que 5, coloca o validador em HOLD.
                validador.hold += 1  # Coloca o validador em HOLD pelas próximas 5 transações
                validador.selecoes_consecutivas = 0
                validador.hold_ate = datetime.now() + timedelta(seconds=10)
                # Se o HOLD tiver expirado, reseta o estado do validador.
                if validador.hold_ate == datetime.now():
                    validador.hold = 0
                db.session.commit()

        # Conta o número de validações bem-sucedidas.
        aprovacoes = sum(1 for r in respostas if r["status"] == STATUS_TRANSACAO_CONCLUIDA)
        # Define o status final da transação baseado no número de aprovações.       
        status_final = STATUS_TRANSACAO_CONCLUIDA if aprovacoes >= 2 else STATUS_NAO_APROVADA

        if aprovacoes >= 2:
            recompensa_total = transacao.valor * 0.02
            recompensa_seletor = transacao.valor * 0.015
            recompensa_validador_travada = transacao.valor * 0.005
            recompensa_validadores = recompensa_total - recompensa_seletor - recompensa_validador_travada
            recompensa_por_validador = recompensa_validadores / len(validadores)

            # Atualiza o saldo do seletor
            seletor.saldo += recompensa_seletor
            db.session.commit()

            for i in range(len(status_validadores)):
                if status_validadores[i] != status_final:
                    # Se o status do validador não corresponder ao status final, aumenta o número de flags do validador.

                    validadores[i].flags += 1
                    if validadores[i].flags >= 2:
                        # Se o número de flags exceder o limite, exclui o validador e cria um novo.
                        db.session.delete(validadores[i])
                        validadores[i].expulsoes += 1
                        db.session.commit()
                        if validadores[i].expulsoes <= 2:
                            saldo_travado = validadores[i].saldo
                            db.session.delete(validadores[i])
                            db.session.commit()
                            novo_validador = Validador(
                                nome='novo_validador',
                                saldo=saldo_travado * 2,
                                chave_unica=CHAVES[str(validadores[i].id)],
                                horario_ultima_transacao=datetime.now()
                            )
                            db.session.add(novo_validador)
                            db.session.commit()
                        else:
                            db.session.delete(validadores[i])
                            db.session.commit()
                    else:
                        db.session.commit()
                else:
                    # Se o status do validador corresponder ao status final, atualiza seu saldo e transações coerentes.
                    validadores[i].saldo += recompensa_por_validador
                    validadores[i].saldo += recompensa_validador_travada
                    validadores[i].transacoes_coerentes += 1

                    # Se o número de transações coerentes atingir um múltiplo de 10.000, reduz o número de flags.
                    if validadores[i].transacoes_coerentes % 10000 == 0:
                        validadores[i].flags = max(0, validadores[i].flags - 1)

                    db.session.commit()

        # Atualiza o status da transação no banco de dados.
        transacao.status = status_final
        db.session.commit()

        sincronizar_tempo() # Função para sincronizar o tempo.

        return status_final
    except Exception as e:
        app.logger.error(f"Erro ao validar transação: {e}")
        return STATUS_NAO_EXECUTADA


@app.route('/transacoes/<int:id>', methods=['GET'])
def VerificarStatusTransacao(id):
    transacao = Transacao.query.get(id)
    if not transacao:
        return jsonify({"message": "Transação não encontrada"}), 404
    return jsonify({"status": transacao.status})


@app.route('/validador/cadastrar/<string:nome>/<int:saldo>', methods=['POST'])
def inserir_validador(nome, saldo):
    saldo_minimo = 100  # Define o saldo mínimo
    if request.method == 'POST' and nome != '' and saldo > saldo_minimo:
        try:
            validador = Validador()
            chave_unica = cadastrar_chave_unica_validador(validador.id)
            validador = Validador(nome=nome, saldo=saldo - 50, flags=0, hold=0, chave_unica=chave_unica,
                                  transacoes_coerentes=0, selecoes_consecutivas=0,
                                  horario_ultima_transacao=datetime.now())
            db.session.add(validador)
            db.session.commit()
            return jsonify({"id": validador.id})
        except Exception as e:
            app.logger.error(f"Erro ao criar validador: {e}")
            return jsonify({"message": "Erro ao criar validador"}), 500
    elif saldo < saldo_minimo:
        return jsonify({"message": "Saldo insuficiente para registrar como validador"}), 400
    else:
        return jsonify({'message': 'Method Not Allowed'}), 405


@app.route('/validador', methods=['GET'])
def ListarValidadores():
    if request.method == 'GET':
        validadores = Validador.query.all()
        return jsonify({"Validadores:": validadores})


def cadastrar_chave_unica_validador(validador_id):
    from random import randint
    try:
        letras = ascii_letters
        chave_unica = ''
        for i in range(10):
            chave_unica += letras[randint(0, len(letras))]
        CHAVES[str(validador_id)] = chave_unica
        return chave_unica
    except Exception as e:
        app.logger.error(f"Erro ao criar chave: {e}")
        return jsonify({"message": "Erro ao criar chave"}), 500


def manter_chave_cheia():
    validadores = Validador.query.all()

    for validador in validadores:
        CHAVES[str(validador.id)] = validador.chave_unica


def registrar_log(acao, detalhes=None):
    log = EleicaoLog(acao=acao, detalhes=detalhes)
    db.session.add(log)
    db.session.commit()
    
@app.route('/validador/<int:id>', methods=['DELETE'])
def ApagarValidador(id):
    if request.method == 'DELETE':
        validador = Validador.query.get(id)
        if not validador:
            return jsonify({"message": "Validador não encontrado"}), 404
        db.session.delete(validador)
        db.session.commit()
        return jsonify({"message": "Validador Deletado com Sucesso"})
    else:
        return jsonify({'message': 'Validador Not Allowed'}), 405


def sincronizar_tempo():
    import requests
    response = requests.get('http://localhost:5000/hora')
    if response.status_code == 200:
        server_time_str = response.json()['horario']
        server_time = datetime.fromisoformat(server_time_str)
        # Aqui você pode ajustar o tempo do validador conforme necessário
        print(f"Tempo do servidor sincronizado: {server_time}")
    else:
        print("Falha ao sincronizar o tempo")


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
