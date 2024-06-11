import sys
import os

sys.path.append(os.path.dirname(os.getcwd()))


class Validador:
    def __init__(self):
        self.nome = ''
        self.senha = ''
        self.qtdMoeda = ''
        self.qtdFlags = 0
        self.horario_ultima_trans = ''

    def set_nome(self, nome):
        self.nome = nome

    def set_senha(self, senha):
        self.senha = senha

    def set_qtdMoeda(self, qtdMoeda):
        self.qtdMoeda = qtdMoeda

    def set_qtdFlags(self, qtdFlags):
        self.qtdFlags = qtdFlags

    def set_horario_ultima_trans(self, horario_ultima_trans):
        self.horario_ultima_trans = horario_ultima_trans
