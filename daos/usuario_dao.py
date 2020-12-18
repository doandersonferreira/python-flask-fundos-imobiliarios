from models.Usuario import Usuario


SQL_USUARIO_POR_ID = 'SELECT id, nome, email, senha from usuario where id = %s'
SQL_ATUALIZA_USUARIO = 'UPDATE usuario SET nome=%s, email=%s, senha=%s where id = %s'
SQL_CRIA_USUARIO = 'INSERT into usuario (nome, email, senha) values (%s, %s, %s)'


class UsuarioDao:
    def __init__(self, db):
        self.__db = db

    def salvar(self, usuario):
        cursor = self.__db.connection.cursor()

        if (usuario.id):
            cursor.execute(SQL_ATUALIZA_USUARIO, (usuario.nome, usuario.email, usuario.senha, usuario.id))
        else:
            cursor.execute(SQL_CRIA_USUARIO, (usuario.nome, usuario.email, usuario.senha))
            usuario.id = cursor.lastrowid
        self.__db.connection.commit()
        return usuario

    def buscar_por_id(self, id):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_USUARIO_POR_ID, (id,))
        tupla = cursor.fetchone()
        return Usuario(tupla[1], tupla[2], tupla[3], id=tupla[0])

    def traduz_usuarios(usuarios):
        def cria_usuario_com_tupla(tupla):
            return Usuario(tupla[1], tupla[2], tupla[3], id=tupla[0])

        return list(map(cria_usuario_com_tupla, usuarios))