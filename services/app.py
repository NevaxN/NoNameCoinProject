import sys
import os

sys.path.append(os.path.dirname(os.getcwd()))

from controllers.validador_controller import ValidadorController
from controllers.seletor_controller import Seletor_Controller
from flask import Flask, redirect

app = Flask(__name__)

v = ValidadorController()
s = Seletor_Controller()


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
    s.cadastrar_validador(v.listar_validadores())
    return s.listar_validadores_escolhidos()


@app.route('/validador')
def validador():
    return redirect("http://127.0.0.1:5000/validador/listar_validadores")


@app.route('/validador/listar_validadores')
def listar_validadores():
    return v.listar_validadores()


if __name__ == "__main__":
    app.run(debug=True)
