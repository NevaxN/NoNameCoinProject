import sys
import os

sys.path.append(os.path.dirname(os.getcwd()))

from util.status_transacao import *
from time import time, asctime

class Validador:
    def __init__(self):
        self.id_validador = 0
        self.saldo_atual = 500.0
        self.horario_ultima_trans = time()
        self.total_transacoes = 10
        self.chave_unica = ''
        self.status_transacao = STATUS_NAO_EXECUTADA  # 0 = Não executada, 1 = Concluída com
        # Sucesso, 2 = Não aprovada (erro)
        self.quant_flag = 0
        self.validadores = []

    def atualizar_id(self):
        self.id_validador += 1

    def atualizar_saldo(self, amount):
        self.saldo_atual += amount

    def incrementar_flag(self):
        self.quant_flag += 1

    def resetar_flag(self):
        self.quant_flag = 0

    def atualizar_ultima_transacao(self, timestamp):
        self.horario_ultima_trans = timestamp

    def incrementar_total_transacoes(self):
        self.total_transacoes += 1

    def atualizar_status_transacao(self, status):
        self.status_transacao = status
