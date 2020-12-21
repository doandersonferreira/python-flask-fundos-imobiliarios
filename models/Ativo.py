class Ativo:
    def __init__(self, ticker, nome, cnpj, id=None):
        self.id = id
        self.ticker = ticker
        self.nome = nome
        self.cnpj = cnpj
