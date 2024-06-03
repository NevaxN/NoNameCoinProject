from datetime import datetime

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

    def retornar_objeto_transacao(self):
        transacao = {
            'sender': 'Alice',
            'receiver': 'Bob',
            'amount': 50,
            'taxa': 1,
            'timestamp': datetime.now(),
            'chave_validador': ''
        }

        return transacao
