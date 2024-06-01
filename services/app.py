import sys

sys.path.append('C:\\Users\\arthu\\prog_Projects\\Universidade\\programacao_distribuida\\NoNameCoinProject')

from controllers.validador_controller import ValidadorController
from controllers.seletor_controller import Seletor_Controller
from flask import Flask

app = Flask(__name__)

@app.route('/')
def conexao_banco():
    return "Funcionando"

@app.route('/trans')
def transacoes():
    return "Funcionando"

@app.route('/hora')
def hora():
    return "Funcionando"

@app.route('/seletor')
def seletor():
    s = Seletor_Controller()
    s.cadastrar_validador()
    return s.listar_validadores()

@app.route('/validador')
def validador():
    seletor = Seletor_Controller()
    chave_unica = seletor.criar_chave_unica()
    v = ValidadorController()
    '''
    v.validar_transacao()
    return v.retornar_objeto_json()'''
    return "Funcionando"

if __name__ == "__main__":
    app.run(debug=True)