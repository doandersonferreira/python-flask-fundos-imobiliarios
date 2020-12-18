from flask import Flask, render_template, request
from flask_mysqldb import MySQL
from models.Usuario import Usuario
from daos.usuario_dao import UsuarioDao


app = Flask(__name__)

# Dados de conexao ao banco
app.config['MYSQL_HOST'] = "0.0.0.0"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "Root@2020"
app.config['MYSQL_DB'] = "fii"
app.config['MYSQL_PORT'] = 3306

# Instanciando o Database para acesso ao banco
db = MySQL(app)
usuario_dao = UsuarioDao(db)

@app.route('/')
def home():
    return 'Hello, World!'


@app.route('/usuario/novo')
def novo_usuario():
    return render_template('novo_usuario.html', titulo='Cadastro')


@app.route('/usuario/criar', methods=['post', ])
def criar_usuario():
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']

    usuario = Usuario(nome, email, senha)

    usuario = usuario_dao.salvar(usuario)

    return f"Criado um usuario de id: {usuario.id}"


app.run(debug=True)
