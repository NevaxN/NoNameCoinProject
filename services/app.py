import NoNameCoinProject.controller.validador_controller
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
    return "Funcionando"

@app.route('/validador')
def validador():
    return "Funcionando"

if __name__ == "__main__":
    app.run(debug=True)