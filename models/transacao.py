from datetime import datetime
from controllers.validador_controller import ValidadorController
import sys
import os

sys.path.append(os.path.dirname(os.getcwd()))

class Transacao:
    def __init__(self):
        self.sender = ''
        self.receiver = ''
        self.amount = 0.0
        self.taxa = 0.0
        self.timestamp = datetime.now()
        self.chave_validador = ''

validador_controller = ValidadorController()

transacao = Transacao(sender='Alice', receiver='Bob', amount=50, taxa=1, timestamp=datetime.now(), chave_validador='chave_validador_123')

if validador_controller.validar_transacao("chave_validador_123", transacao):
    print("Transação concluída com sucesso")
else:
    print("Transação não aprovada")
    
json_object = validador_controller.retornar_objeto_json("chave_validador_123")
print(json_object)
