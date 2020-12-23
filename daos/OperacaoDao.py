from flask import session
from models.Operacao import Operacao


SQL_OPERACOES = 'SELECT * from operacao order by ticker'

SQL_AGREGADO_USUARIO = 'SELECT ticker, sum(quantidade) as cotas , ' \
                       'sum(valor_cota * quantidade) as "valor_aplicado" from ativo a join operacao o ' \
                       'where a.id = o.id_ativo and id_usuario = %s group by ticker order by ticker;'

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

        id_usuario = session['usuario_logado'][0]

        if operacao.id:
            cursor.execute(SQL_EDITAR, (operacao.tipo, operacao.data, operacao.valor, operacao.quantidade,
                                        operacao.ativo, id_usuario, operacao.id))
        else:
            cursor.execute(SQL_SALVAR,(operacao.tipo, operacao.data, operacao.valor, operacao.quantidade,
                                        operacao.ativo, id_usuario))
            operacao.id = cursor.lastrowid
        self.__db.connection.commit()

        return operacao

    def carteira_sumarizada(self,id_usuario):
        cursor = self.__db.connection.cursor()

        cursor.execute(SQL_AGREGADO_USUARIO, (id_usuario, ))
        dados = cursor.fetchall()

        return dados

