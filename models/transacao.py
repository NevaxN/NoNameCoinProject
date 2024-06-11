from time import time

import sys
import os

sys.path.append(os.path.dirname(os.getcwd()))

class Transacao:
    def __init__(self):
        self.sender = ''
        self.receiver = ''
        self.amount = 0.0
        self.taxa = 0.0
        self.timestamp = time()
        self.chave_validador = ''
