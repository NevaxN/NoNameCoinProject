from time import time

import sys
import os

sys.path.append(os.path.dirname(os.getcwd()))

class Transacao:
    def __init__(self):
        self.sender = ''
        self.receiver = ''
        self.amount = 0.0
        self.taxa = 0.0
        self.timestamp = time()
        self.chave_validador = ''
'''
Ideia de atualizaçao do transaçao

# Importando os módulos necessários
from datetime import datetime
from ..services.instance.site.db import db  # Importando o objeto db do SQLAlchemy

# Definindo a classe Transacao
class Transacao(db.Model):
    # Definindo os atributos da classe Transacao e mapeando-os para colunas no banco de dados
    id = db.Column(db.Integer, primary_key=True)
    remetente = db.Column(db.Integer, nullable=False)
    recebedor = db.Column(db.Integer, nullable=False)
    valor = db.Column(db.Float, nullable=False)
    status = db.Column(db.Integer, nullable=False, default=0)
    horario = db.Column(db.DateTime, nullable=False, default=datetime.now)

    # Método construtor da classe Transacao
    def _init_(self, remetente, recebedor, valor):
        self.remetente = remetente
        self.recebedor = recebedor
        self.valor = valor

    # Método para representar a instância da classe como uma string
    def _repr_(self):
        return f"Transacao(id={self.id}, remetente={self.remetente}, recebedor={self.recebedor}, 
        valor={self.valor}, status={self.status}, horario={self.horario})"
'''