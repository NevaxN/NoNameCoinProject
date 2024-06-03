import sys
import os

sys.path.append(os.path.dirname(os.getcwd()))

from datetime import datetime
from models.validador import Validador
from models.transacao import Transacao
from util.status_transacao import *
import json

class ValidadorController:
    def __init__(self):
        #chave_unica
        self.transacao = Transacao()
        #self.validadores = {}
        
    '''def obter_ou_criar_validador(self, chave_unica):
        if chave_unica not in self.validadores:
            self.validadores[chave_unica] = Validador(chave_unica)
        return self.validadores[chave_unica]'''
       
    def retornar_objeto_json(self, chave_unica):
        validador = Validador(chave_unica)
        validador_details = validador.objeto_validador()
        json_object = json.dumps(validador_details, indent=4)
        validador.atualizar_id()
        return json_object
    
    '''def criar_transacao(self, chave_unica):
        validador = self.obter_ou_criar_validador(chave_unica)
        # Definir o status da transação como "não executada"
        validador.atualizar_status_transacao(STATUS_NAO_EXECUTADA)'''
        
    def validar_transacao(self, chave_unica):
        validador = Validador(chave_unica)
        # Regra 1: Verificar saldo
        if validador.saldo_atual < self.transacao.amount + self.transacao.taxa:
            validador.atualizar_status_transacao(STATUS_NAO_APROVADA) # Saldo insuficiente
            return False
        
        # Regra 2: Verificar horário da última transação
        if self.transacao.timestamp > datetime.now():
            validador.atualizar_status_transacao(STATUS_NAO_APROVADA) # Horário da transação é no futuro
            return False
        
        if validador.horario_ultima_trans and self.transacao.timestamp <= validador.horario_ultima_trans:
            validador.atualizar_status_transacao(STATUS_NAO_APROVADA) # Horário da transação é menor ou igual ao horário da última transação
            return False
        
        # Regra 3: Verificar número de transações no último minuto
        if validador.quant_flag > 100:
            validador.atualizar_status_transacao(STATUS_NAO_APROVADA) # Mais de 100 transações no último minuto
            return False
        
        # Atualizar status e contador de transações
        validador.atualizar_saldo(-(self.transacao.amount + self.transacao.taxa))
        validador.atualizar_ultima_transacao(self.transacao.timestamp)
        validador.incrementar_total_transacoes()
        validador.atualizar_status_transacao(STATUS_TRANSACAO_CONCLUIDA) # Transação válida
        
        return True