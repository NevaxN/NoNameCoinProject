'''Essa camada tem por função cadastrar e verificar a viabilidades de elementos
computacionais serem validadores, assim com selecionar qual ou quais validadores receberam a
transação ativa, além de gerenciar o consenso destes validados;'''

import time
import random
from threading import Timer

# Simulação de banco de dados
validadores = {}
transacoes = []

class Seletor:

    # Calcula o percentual de chance de escolha de um validador com base nas moedas que ele possui e na flag
    def calcular_percentual(self, moedas, flag):
        base = moedas
        if flag == 1:
            base *= 0.5
        elif flag == 2:
            base *= 0.25
        return base

    # Cadastra um novo validador, verificando se já está cadastrado e se possui saldo mínimo
    def cadastrar_validador(self, id_validador, moedas):
        if id_validador in validadores:
            return {"status": "Validador já cadastrado"}
        
        if moedas < 50:
            return {"status": "Saldo mínimo de 50 NoNameCoins necessário"}

        validadores[id_validador] = {
            'moedas': moedas,
            'flag': 0,
            'chave_unica': f'chave_{id_validador}_{int(time.time())}',
            'transacoes_concluidas': 0,
            'expulso': False,
            'em_hold': False,
            'escolhido_count': 0
        }
        return {"status": "Validador cadastrado com sucesso!", "chave_unica": validadores[id_validador]['chave_unica']}

    # Lista todos os validadores cadastrados
    def listar_validadores(self):
        return validadores

    # Seleciona validadores para uma transação, respeitando as condições especificadas
    def selecionar_validadores(self, transacao):
        transacoes.append(transacao)
        validos = {k: v for k, v in validadores.items() if not v['em_hold'] and not v['expulso']}
        
        if len(validos) < 3:
            Timer(60, self.selecionar_validadores, args=[transacao]).start()
            return {"status": "Número insuficiente de validadores, transação em espera"}

        total_moedas = sum([self.calcular_percentual(v['moedas'], v['flag']) for v in validos.values()])
        selecoes = []
        for validador, dados in validos.items():
            chance = self.calcular_percentual(dados['moedas'], dados['flag']) / total_moedas
            if random.random() < chance and len(selecoes) < 3:
                selecoes.append(validador)
                validadores[validador]['escolhido_count'] += 1
                if len(selecoes) == 3:
                    break

        if len(selecoes) < 3:
            Timer(60, self.selecionar_validadores, args=[transacao]).start()
            return {"status": "Não foi possível selecionar 3 validadores, transação em espera"}

        for validador in selecoes:
            if validadores[validador]['escolhido_count'] >= 5:
                validadores[validador]['em_hold'] = True
                validadores[validador]['escolhido_count'] = 0

        return {"validadores_selecionados": selecoes}

    # Gerencia o consenso com base nas respostas dos validadores
    def gerir_consenso(self, transacao_id, validadores_respostas):
        status = sum(validadores_respostas) / len(validadores_respostas) > 0.5
        return {"transacao_id": transacao_id, "status_consenso": status}

    # Adiciona uma flag ao validador e verifica se ele deve ser expulso
    def adicionar_flag(self, id_validador):
        if id_validador in validadores:
            validadores[id_validador]['flag'] += 1
            if validadores[id_validador]['flag'] > 2:
                validadores[id_validador]['expulso'] = True
            return {"status": "Flag adicionada com sucesso"}
        return {"status": "Validador não encontrado"}
