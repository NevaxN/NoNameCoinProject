class Transacao:
    def __init__(self, sender, receiver, amount, taxa, timestamp, chave_validador):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.taxa = taxa
        self.timestamp = timestamp
        self.chave_validador = chave_validador
