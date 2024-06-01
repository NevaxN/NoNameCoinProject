from datetime import datetime
from models.validador import Validador
from models.transacao import Transacao
from controllers.seletor_controller import criar_chave_unica
from util.status_transacao import *

class ValidadorController:
    def __init__(self):
        #chave_unica
        self.chave_unica = criar_chave_unica()
        self.validador = Validador(self.chave_unica)
        self.transacao = Transacao

    def retornar_objeto(self):
        return self.validador.objeto_validador()
        
    '''def validar_transacao(self):
        # Regra 1: Verificar saldo
        if self.validador.saldo_atual < self.transacao.amount + self.transacao.taxa:
            self.validador.atualizar_status_transacao(STATUS_NAO_APROVADA) # Saldo insuficiente
            return False
        
        # Regra 2: Verificar horário da última transação
        if self.transacao.timestamp > datetime.now():
            self.validador.atualizar_status_transacao(STATUS_NAO_APROVADA) # Horário da transação é no futuro
            return False
        
        if self.validador.horario_ultima_trans and self.transacao.timestamp <= self.validador.horario_ultima_trans:
            self.validador.atualizar_status_transacao(STATUS_NAO_APROVADA) # Horário da transação é menor ou igual ao horário da última transação
            return False
        
        # Regra 3: Verificar número de transações no último minuto
        if self.validador.quant_flag > 100:
            self.validador.atualizar_status_transacao(STATUS_NAO_APROVADA) # Mais de 100 transações no último minuto
            return True
        
        # Atualizar status e contador de transações
        self.validador.atualizar_saldo(-(self.transacao.amount + self.transacao.taxa))
        self.validador.atualizar_ultima_transacao(self.transacao.timestamp)
        self.validador.incrementar_total_transacoes()
        self.validador.atualizar_status_transacao(STATUS_TRANSACAO_CONCLUIDA) # Transação válida'''
        