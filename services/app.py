import sys
import os

sys.path.append(os.path.dirname(os.getcwd()))

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
    return v.retornar_objeto_json(chave_unica)


if __name__ == "__main__":
    app.run(debug=True)
