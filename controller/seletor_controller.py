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