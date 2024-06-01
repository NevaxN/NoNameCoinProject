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
        

    def retornar_objeto_json(self, chave_unica):
        validador = Validador(chave_unica)
        validador_details = validador.objeto_validador()
        json_object = json.dumps(validador_details, indent=4)
        validador.atualizar_id()
        return json_object
        
    def validar_transacao(self, chave_unica):
        validador = Validador(chave_unica)
        # Regra 1: Verificar saldo
        if validador.saldo_atual < self.transacao.amount + self.transacao.taxa:
            validador.atualizar_status_transacao(STATUS_NAO_APROVADA) # Saldo insuficiente
        
        # Regra 2: Verificar horário da última transação
        if self.transacao.timestamp > datetime.now():
            validador.atualizar_status_transacao(STATUS_NAO_APROVADA) # Horário da transação é no futuro
        
        if validador.horario_ultima_trans and self.transacao.timestamp <= self.validador.horario_ultima_trans:
            validador.atualizar_status_transacao(STATUS_NAO_APROVADA) # Horário da transação é menor ou igual ao horário da última transação
        
        # Regra 3: Verificar número de transações no último minuto
        if validador.quant_flag > 100:
            validador.atualizar_status_transacao(STATUS_NAO_APROVADA) # Mais de 100 transações no último minuto
        
        # Atualizar status e contador de transações
        validador.atualizar_saldo(-(self.transacao.amount + self.transacao.taxa))
        validador.atualizar_ultima_transacao(self.transacao.timestamp)
        validador.incrementar_total_transacoes()
        validador.atualizar_status_transacao(STATUS_TRANSACAO_CONCLUIDA) # Transação válida
        