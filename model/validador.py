from datetime import datetime
from transacao import Transacao
from util.status_transacao import * 

class Validador:
    def __init__(self, chave_unica):
        self.saldo_atual = 0.0
        self.horario_ultima_trans = None
        self.total_transacoes = 0
        self.chave_unica = chave_unica
        self.status_transacao = STATUS_NAO_EXECUTADA  # 0 = Não executada, 1 = Concluída com Sucesso, 2 = Não aprovada (erro)
        self.quant_flag = 0

    def validar_transacao(self):
        # Regra 1: Verificar saldo
        if self.saldo_atual < Transacao.amount + Transacao.taxa:
            self.status_transacao = 2  # Saldo insuficiente
            return False

        # Regra 2: Verificar horário da transação
        if Transacao.timestamp > datetime.now():
            self.status_transacao = 2  # Horário da transação é no futuro
            return False

        # Regra 2: Verificar horário da última transação
        if self.horario_ultima_trans and Transacao.timestamp <= self.horario_ultima_trans:
            self.status_transacao = 2  # Horário da transação é menor ou igual ao horário da última transação
            return False

        # Regra 3: Verificar número de transações no último minuto
        if self.quant_flag > 100:
            self.status_transacao = 2  # Mais de 100 transações no último minuto
            return False

        # Atualizar status e contador de transações
        self.saldo_atual -= Transacao.amount + Transacao.taxa
        self.horario_ultima_trans = Transacao.timestamp
        self.total_transacoes += 1
        self.status_transacao = 1  # Transação válida

        return True

    def atualizar_saldo(self, amount):
        self.saldo_atual += amount

    def incrementar_flag(self):
        self.quant_flag += 1

    def resetar_flag(self):
        self.quant_flag = 0
