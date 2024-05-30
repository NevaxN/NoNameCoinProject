from flask import Flask

app = Flask(__name__)

@app.route('/')
def conexao_banco():
    return "Funcionando"

@app.route('/trans')
def transacoes():
    return "Funcionando"

@app.route('/seletor')
def seletor():
    return "Funcionando"

@app.route('/validador')
def validador():
    return "Funcionando"

@app.route('/hora')
def hora():
    return "Funcionando"

@app.errorhandler(400)
def bad_request(error):
    return "Erro ao carregar página", 400

if __name__ == "__main__":
    app.run(debug=True)