import requests

#Criando clientes
#response = requests.post('http://127.0.0.1:5000/validador/bob/1234/500')
#response = requests.post('http://localhost:5000/cliente/claytin/1234/500')
#Editando clientes
#response = requests.post('http://127.0.0.1:5000/validador/3/250')
#response = requests.post('http://localhost:5000/cliente/2/300')
#response = requests.delete('http://localhost:5000/cliente/2')
#Criando seletores
#response = requests.post('http://http://127.0.0.1:5000/seletor/seletor1/123.123')
#response = requests.post('http://localhost:5000/seletor/seletor3/123.123')
#Editando seletores
#response = requests.post('http://localhost:5000/seletor/1/seletorB/111111')
#response = requests.post('http://localhost:5000/seletor/2/seletorA/222222')
#response = requests.delete('http://localhost:5000/seletor/2')

#criando uma transacao
#response = requests.post('http://localhost:5000/cliente/muriel/3214/500')
#response = requests.post('http://localhost:5000/seletor/seletor1/123.123/100')
response = requests.post('http://localhost:5000/transacoes/1/3/276')
#response = requests.post('http://localhost:5000/validador/cadastrar/validador4/110')

print(response.text)
