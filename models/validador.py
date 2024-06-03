import sys
import os

sys.path.append(os.path.dirname(os.getcwd()))

from util.status_transacao import *


class Validador:
    def __init__(self, chave_unica):
        self.id_validador = 0
        self.saldo_atual = 0.0
        self.horario_ultima_trans = None
        self.total_transacoes = 0
        self.chave_unica = chave_unica
        self.status_transacao = STATUS_NAO_EXECUTADA  # 0 = Não executada, 1 = Concluída com
        # Sucesso, 2 = Não aprovada (erro)
        self.quant_flag = 0

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

    def objeto_validador(self):
        return {str(self.id_validador): {
            'saldo_atual': self.saldo_atual,
            'horario_ultima_trans': self.horario_ultima_trans,
            'total_transacoes': self.total_transacoes,
            'chave_unica': self.chave_unica,
            'status_transacao': self.status_transacao,
            'quant_flag': self.quant_flag}}
