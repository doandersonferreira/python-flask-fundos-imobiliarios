class Operacao:
    def __init__(self, ativo, tipo,data,quantidade,valor,id=None):
        self.id = id
        self.ativo = ativo
        self.tipo = tipo
        self.data = data
        self.quantidade = quantidade
        self.valor = valor