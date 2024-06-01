from util.status_transacao import *

class Validador:
    def __init__(self, chave_unica):
        self.id_validador = 0
        self.saldo_atual = 0.0
        self.horario_ultima_trans = None
        self.total_transacoes = 0
        self.chave_unica = chave_unica
        self.status_transacao = STATUS_NAO_EXECUTADA  # 0 = Não executada, 1 = Concluída com Sucesso, 2 = Não aprovada (erro)
        self.quant_flag = 0

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
        return {str(self.id_validador): {self.saldo_atual, self.horario_ultima_trans, self.total_transacoes, self.chave_unica,self.status_transacao, self.quant_flag}}