'''Essa camada tem por função cadastrar e verificar a viabilidades de elementos
computacionais serem validadores, assim com selecionar qual ou quais validadores receberam a
transação ativa, além de gerenciar o consenso destes validados;'''

import time
import random
from threading import Timer


class Seletor:
    def __init__(self):
        self.valor_taxa = 0.0
        self.saldo_minimo = 0.0
        self.saldo_atual = 0.0
