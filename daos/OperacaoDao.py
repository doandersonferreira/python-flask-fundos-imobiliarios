from models.Operacao import Operacao

SQL_OPERACOES = 'SELECT * from operacao order by ticker'
SQL_SALVAR = 'INSERT INTO operacao (tipo, data, valor_cota, quantidade, id_ativo, id_usuario) ' \
             'VALUES (%s, %s, %s, %s, %s, %s )'
SQL_EDITAR = 'UPDATE operacao SET tipo = %s, data = %s, valor_cota = %s, ' \
             'quantidade = %s, id_ativo = %s, id_usuario = %s ' \
             'WHERE id = %s'

class OperacaoDao:

    def __init__(self, db):
        self.__db = db

    def salvar(self, operacao):
        cursor = self.__db.connection.cursor()

        if operacao.id:
            cursor.execute(SQL_EDITAR, (operacao.tipo, operacao.data, operacao.valor, operacao.quantidade,
                                        operacao.ativo, 1, operacao.id))
        else:
            cursor.execute(SQL_SALVAR,(operacao.tipo, operacao.data, operacao.valor, operacao.quantidade,
                                        operacao.ativo, 1))
            operacao.id = cursor.lastrowid
        self.__db.connection.commit()

        return operacao
