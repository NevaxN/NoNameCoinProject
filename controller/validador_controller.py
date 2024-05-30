'''Regras de validação
1- O remetente deve ter um valor em saldo igual ou maior que o valor da transação, acrescido das
taxas para a mesma ser válida;(precisa do banco para o valor da transação)

2- O horário da transação deve ser menor ou igual ao horário atual do sistema e deve ser maior que
o horário da última transação para ser válida;(precisa do banco para o horário)

3- Caso o remetente tenha feito mais que 100 transações no último minuto, as transações no
próximo minuto devem ser invalidas;(precisa do banco para o horário)

o Opcional: Aumentar o tempo de recusa, caso o problema persista;

4- Na hora do cadastro o validador recebe uma chave única do seletor. Em toda transação, o validador deve retornar a chave única que recebeu no cadastro. Caso as chaves sejam iguais, a
transação é concluída, caso contrário, a transação não é concluída; (criar a chave)

5-  Status da Transação (Servem da camada “Validador” para a camada “Seletor”, assim como da
camada “Seletor” para a camada “Banco”):
o 1 = Concluída com Sucesso
o 2 = Não aprovada (erro)
o 0 = Não executada
▪ Códigos opcionais podem existir, mas devem ser descritos para implementação
na camada “Banco”;'''
