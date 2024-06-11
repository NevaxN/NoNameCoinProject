import random
import sys
import os

sys.path.append(os.path.dirname(os.getcwd()))

from time import time
from models.validador import Validador
from models.transacao import Transacao
from controllers.seletor_controller import Seletor_Controller
from util.status_transacao import STATUS_NAO_APROVADA, STATUS_TRANSACAO_CONCLUIDA, STATUS_NAO_EXECUTADA

class ValidadorController:
    def __init__(self):
        # chave_unica
        self.transacao = Transacao()
        self.validador = Validador()
        self.sc = Seletor_Controller()

    '''def obter_ou_criar_validador(self, chave_unica):
        if chave_unica not in self.validadores:
            self.validadores[chave_unica] = Validador(chave_unica)
        return self.validadores[chave_unica]'''

    '''def criar_transacao(self, chave_unica):
            validador = self.obter_ou_criar_validador(chave_unica)
            # Definir o status da transação como "não executada"
            validador.atualizar_status_transacao(STATUS_NAO_EXECUTADA)'''



    def validar_transacao(self):
        t = self.transacao.retornar_objeto_transacao()
        # Regra 1: Verificar saldo
        if self.validador.saldo_atual < t['amount'] + t['taxa']:
            return STATUS_NAO_APROVADA  # Saldo insuficiente

        # Regra 2: Verificar horário da última transação
        if t['timestamp'] > time():
            return STATUS_NAO_APROVADA  # Horário da transação é no futuro

        if (self.validador.horario_ultima_trans and t['timestamp'] <=
                self.validador.horario_ultima_trans):
            return STATUS_NAO_APROVADA  # Horário da transação é menor ou igual ao horário da
            # última transação

        # Regra 3: Verificar número de transações no último minuto
        if self.validador.quant_flag > 100:
            return STATUS_NAO_APROVADA  # Mais de 100 transações no último minuto

        # Atualizar status e contador de transações
        return STATUS_TRANSACAO_CONCLUIDA  # Transação válida
