from models.Ativo import Ativo

SQL_ATIVOS = 'SELECT * from ativo order by ticker'

class AtivoDao:

    def __init__(self, db):
        self.__db = db

    def buscar(self):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_ATIVOS)
        dados = cursor.fetchall()
        ativos = self.traduz_ativos(dados) if dados else None
        return ativos

    def traduz_ativos(self, dados):
        ativos = []
        for dado in dados:
            ativo = Ativo(dado[1], dado[2], dado[3], dado[0])
            ativos.append(ativo)
        return ativos


