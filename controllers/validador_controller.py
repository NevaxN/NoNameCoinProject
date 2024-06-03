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
        # chave_unica
        self.transacao = Transacao()

    '''def obter_ou_criar_validador(self, chave_unica):
        if chave_unica not in self.validadores:
            self.validadores[chave_unica] = Validador(chave_unica)
        return self.validadores[chave_unica]'''

    def retornar_objeto_json(self, chave_unica):
        validador = Validador(chave_unica)
        validador_details = validador.objeto_validador()
        self.validar_transacao(chave_unica)
        json_object = json.dumps(validador_details, indent=4)
        return json_object

    '''def criar_transacao(self, chave_unica):
        validador = self.obter_ou_criar_validador(chave_unica)
        # Definir o status da transação como "não executada"
        validador.atualizar_status_transacao(STATUS_NAO_EXECUTADA)'''

    def validar_transacao(self, chave_unica):
        validador = Validador(chave_unica)
        t = self.transacao.retornar_objeto_transacao()
        # Regra 1: Verificar saldo
        if validador.saldo_atual < t['amount'] + t['taxa']:
            validador.atualizar_status_transacao(STATUS_NAO_APROVADA)  # Saldo insuficiente
            return False

        # Regra 2: Verificar horário da última transação
        if t['timestamp'] > datetime.now():
            validador.atualizar_status_transacao(
                STATUS_NAO_APROVADA)  # Horário da transação é no futuro
            return False

        if (validador.horario_ultima_trans and t['timestamp'] <=
                validador.horario_ultima_trans):
            validador.atualizar_status_transacao(
                STATUS_NAO_APROVADA)  # Horário da transação é menor ou igual ao horário da
            # última transação
            return False

        # Regra 3: Verificar número de transações no último minuto
        if validador.quant_flag > 100:
            validador.atualizar_status_transacao(
                STATUS_NAO_APROVADA)  # Mais de 100 transações no último minuto
            return False

        # Atualizar status e contador de transações
        validador.atualizar_id()
        validador.atualizar_saldo(-(t['amount'] + t['taxa']))
        validador.atualizar_ultima_transacao(t['timestamp'])
        validador.incrementar_total_transacoes()
        validador.atualizar_status_transacao(STATUS_TRANSACAO_CONCLUIDA)  # Transação válida

        return True
