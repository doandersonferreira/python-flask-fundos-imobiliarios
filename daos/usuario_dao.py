from models.Usuario import Usuario


SQL_USUARIO_POR_EMAIL = 'SELECT id, nome, email, senha from usuario where email = %s'
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

    def busca_por_email(self, email):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_USUARIO_POR_EMAIL, (email,))
        dados = cursor.fetchone()
        usuario = traduz_usuario(dados) if dados else None
        return usuario

def traduz_usuario(tupla):
    return Usuario(tupla[1], tupla[2], tupla[3], id= tupla[0])
