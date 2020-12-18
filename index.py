from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from models.Usuario import Usuario
from daos.usuario_dao import UsuarioDao


app = Flask(__name__)

# Utilizado pela Session para armazenamento de atributos na sessao.
app.secret_key = 'fii'

# Dados de conexao ao banco
app.config['MYSQL_HOST'] = "0.0.0.0"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "Root@2020"
app.config['MYSQL_DB'] = "fii"
app.config['MYSQL_PORT'] = 3306

# Instanciando o Database para acesso ao banco
db = MySQL(app)
usuario_dao = UsuarioDao(db)

def usuario_logado():
    if ('usuario_logado' not in session or session['usuario_logado'] == None):
        return False
    else:
        return True

@app.route('/')
def home():
    return 'Hello, World!'


@app.route('/usuario/novo')
def novo_usuario():
    if usuario_logado():
        return render_template('novo_usuario.html', titulo='Cadastro')
    else:
        return redirect(url_for('login', proxima=url_for('novo_usuario')))


@app.route('/usuario/criar', methods=['post', ])
def criar_usuario():
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']

    usuario = Usuario(nome, email, senha)

    usuario = usuario_dao.salvar(usuario)

    return redirect(url_for('home'))

@app.route('/login')
def login():
    # obter um query param da url
    proxima = request.args.get('proxima')
    return render_template('/login.html', proxima=proxima)


@app.route('/autenticar', methods=['post', ])
def autenticar():
    email = request.form['email']
    senha = request.form['senha']
    usuario = usuario_dao.busca_por_email(email)

    if usuario:
        if usuario.senha == senha:
            session['usuario_logado'] = usuario.id
            flash('Bem vindo, ' + usuario.nome + ' !')
            proxima_pagina = request.form['proxima']

            return redirect(proxima_pagina)
        else:
            flash('Usuário ou senha incorretos. Tente novamente!')
            return redirect(url_for('login'))
    return usuario.senha

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Nenhum usuário logado!')
    return redirect(url_for('login'))

app.run(debug=True)