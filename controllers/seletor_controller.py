'''
1- O seletor deve escolher pelo menos três Validados para a transação ser concluída. Caso a
quantidade mínima não esteja disponível, colocar a transação em espera, por no máximo, um
minuto;

2- O consenso é gerado com mais de 50% de um status (Aprovada ou Não Aprovada);

3- O percentual de chance de escolha do validador é dinâmico, a depender da quantidade de
moedas que o mesmo irá disponibilizar, tendo 50% de redução para Flag=1 e 75% de redução
para Flag=2;

4- A percentual mínimo de escolha de um validador não é limitado e o percentual máximo de
escolha deve ser de 20%;

5- Validadores inconsistentes ou mal intencionados serão identificados por uma FLAG de alerta.
Caso o Validador receba mais que duas FLAGs, o mesmo deve ser eliminado da rede, perdendo
seu saldo. Uma FLAG é retirada a cada 10.000 transações coerentes;

6- Caso o mesmo validador seja escolhido por cinco vezes seguidas, o mesmo deve ficar em HOLD
pelas próximas 5 trasações;

7- Após a expulsão, um validador pode retorna a rede até duas vezes, sendo obrigatório o dobro do
saldo travado anteriormente para o retorno;

8- É obrigatório que o Validador se cadastre no Seletor, travando um saldo mínimo de 50
NoNameCoins;

9- Para cada validação bem sucedida o seletor recebera 1,5% da quantidade de NoNameCoins
transacionadas, ficando 0,5% travado para o validador e o restante distribuído igualitariamente
entre os validadores;'''
import sys
import os
import json
import time
from threading import Timer
from random import choices

sys.path.append(os.path.dirname(os.getcwd()))

from models.seletor import Seletor
from controllers.validador_controller import ValidadorController

class Seletor_Controller():

    def _init_(self):
        self.vc = ValidadorController()
        self.seletor = Seletor()

    def criar_chave_unica(self):
        from random import randint
        from string import ascii_letters

        chave_unica = ''.join(choices(ascii_letters, k=10))
        return chave_unica

    def cadastrar_validador(self):
        if len(self.seletor.validadores) >= 3:
            return {"status": "Já existem 3 validadores cadastrados"}

        self.seletor.validadores[str(self.seletor.id_seletor)] = self.vc.retornar_objeto_json(self.criar_chave_unica())
        print('Cadastrado')

    def listar_validadores(self):
        if len(self.seletor.validadores) < 3:
            return {"status": "Número insuficiente de validadores. Cadastre pelo menos 3 validadores."}
        
        json_object = json.dumps(self.seletor.validadores, indent=4)
        return json_object

    # Rota para adicionar flag a um validador
    '''def adicionar_flag(self, id_validador):
        if id_validador in self.seletor.validadores:
            self.seletor.validadores[id_validador]['flag'] += 1
            if self.seletor.validadores[id_validador]['flag'] > 2:
                self.seletor.validadores[id_validador]['expulso'] = True
                return {"status": "Validador expulso"}
            return {"status": "Flag adicionada com sucesso"}
        return {"status": "Validador não encontrado"}'''

    # Rota para expulsar um validador
    '''def expulsar_validador(self, id_validador):
        if id_validador in self.seletor.validadores:
            self.seletor.validadores[id_validador]['expulso'] = True
            return {"status": "Validador expulso com sucesso"}
        return {"status": "Validador não encontrado"}'''

    # Rota para selecionar validadores
    '''def selecionar_validadores(self, transacao):
        if len(self.seletor.validadores) < 3:
            return {"status": "Número insuficiente de validadores. A transação será colocada em espera."}

        validadores_disponiveis = [v for v in self.seletor.validadores.values() if not v['expulso']]
        
        if len(validadores_disponiveis) < 3:
            return {"status": "Número insuficiente de validadores disponíveis. A transação será colocada em espera."}

        # Simulação da escolha dos validadores
        escolhidos = self.escolher_validadores(validadores_disponiveis, 3)
        
        resultado_consenso = self.gerar_consenso(escolhidos)
        
        if resultado_consenso['status'] == "Aprovada":
            self.atualizar_saldo(transacao, escolhidos)
        
        return resultado_consenso'''

    '''def escolher_validadores(self, validadores, num_escolhidos):
        pesos = [self.calcular_percentual(v['moedas'], v['flag']) for v in validadores]
        total_peso = sum(pesos)
        
        if total_peso == 0:
            return []

        percentuais = [min(p / total_peso, 0.2) for p in pesos]
        escolhidos = choices(validadores, percentuais, k=num_escolhidos)

        return escolhidos'''

    '''def calcular_percentual(self, moedas, flag):
        base = moedas
        if flag == 1:
            base *= 0.5
        elif flag == 2:
            base *= 0.25
        return base'''

    '''def gerar_consenso(self, validadores):
        votos = [random.choice(["Aprovada", "Não Aprovada"]) for _ in validadores]
        consenso = "Aprovada" if votos.count("Aprovada") > len(votos) / 2 else "Não Aprovada"
        
        return {"status": consenso, "validadores": validadores, "votos": votos}'''

    '''def atualizar_saldo(self, transacao, validadores):
        taxa = transacao['quantidade'] * 0.015
        taxa_validador = transacao['quantidade'] * 0.005
        taxa_distribuicao = (transacao['quantidade'] - taxa - taxa_validador) / len(validadores)

        for validador in validadores:
            validador['moedas'] += taxa_distribuicao
            validador['transacoes_concluidas'] += 1

        self.seletor.saldo += taxa
        validadores[0]['moedas'] += taxa_validador  # Assumindo que o primeiro validador é o principal

        return'''