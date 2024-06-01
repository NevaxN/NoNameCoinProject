'''
1- O seletor deve escolher pelo menos três Validados para a transação ser concluída. Caso a
quantidade mínima não esteja disponível, colocar a transação em espera, por no máximo, um
minuto;

2- O consenso é gerado com mais de 50% de um status (Aprovada ou Não Aprovada);

3- O percentual de chance de escolha do validador é dinâmico, a depender da quantidade de
moedas que o mesmo irá disponibilizar, tendo 50% de redução para Flag=1 e 75% de redução
para Flag=2;

4- A percentual mínimo de escolha de um validador não é limitado e o percentual máximo de
escolha deve ser de 20%;

5- Validadores inconsistentes ou mal intencionados serão identificados por uma FLAG de alerta.
Caso o Validador receba mais que duas FLAGs, o mesmo deve ser eliminado da rede, perdendo
seu saldo. Uma FLAG é retirada a cada 10.000 transações coerentes;

6- Caso o mesmo validador seja escolhido por cinco vezes seguidas, o mesmo deve ficar em HOLD
pelas próximas 5 trasações;

7- Após a expulsão, um validador pode retorna a rede até duas vezes, sendo obrigatório o dobro do
saldo travado anteriormente para o retorno;

8- É obrigatório que o Validador se cadastre no Seletor, travando um saldo mínimo de 50
NoNameCoins;

9- Para cada validação bem sucedida o seletor recebera 1,5% da quantidade de NoNameCoins
transacionadas, ficando 0,5% travado para o validador e o restante distribuído igualitariamente
entre os validadores;'''
from flask import Blueprint, request, jsonify
from model.seletor import Seletor


def criar_chave_unica():
    from random import randint
    from string import ascii_letters

    chave_unica = ''
    for i in range (10):
        chave_unica += ascii_letters[(randint(0, 50))]

    return chave_unica
# Criação do blueprint do Flask
'''seletor_bp = Blueprint('seletor_bp', __name__)

# Inicialização do objeto Seletor
seletor = Seletor()

# Rota para cadastrar um validador
@seletor_bp.route('/cadastrar_validador', methods=['POST'])
def cadastrar_validador():
    data = request.get_json()
    id_validador = data.get('id_validador')
    moedas = data.get('moedas')

    if not id_validador or moedas is None:
        return jsonify({"status": "Erro", "mensagem": "Dados incompletos"}), 400

    resultado = seletor.cadastrar_validador(id_validador, moedas)
    return jsonify(resultado)

# Rota para listar validadores
@seletor_bp.route('/listar_validadores', methods=['GET'])
def listar_validadores():
    resultado = seletor.listar_validadores()
    return jsonify(resultado)

# Rota para adicionar flag a um validador
@seletor_bp.route('/adicionar_flag', methods=['POST'])
def adicionar_flag():
    data = request.get_json()
    id_validador = data.get('id_validador')

    if not id_validador:
        return jsonify({"status": "Erro", "mensagem": "ID do validador não fornecido"}), 400

    resultado = seletor.adicionar_flag(id_validador)
    return jsonify(resultado)

# Rota para expulsar um validador
@seletor_bp.route('/expulsar_validador', methods=['POST'])
def expulsar_validador():
    data = request.get_json()
    id_validador = data.get('id_validador')

    if not id_validador:
        return jsonify({"status": "Erro", "mensagem": "ID do validador não fornecido"}), 400

    resultado = seletor.expulsar_validador(id_validador)
    return jsonify(resultado)

# Rota para selecionar validadores
@seletor_bp.route('/selecionar_validadores', methods=['POST'])
def selecionar_validadores():
    data = request.get_json()
    transacao = data.get('transacao')

    if not transacao:
        return jsonify({"status": "Erro", "mensagem": "Dados da transação não fornecidos"}), 400

    resultado = seletor.selecionar_validadores(transacao)
    return jsonify(resultado)'''
