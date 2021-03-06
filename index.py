from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from models.Usuario import Usuario
from models.Operacao import Operacao
from daos.UsuarioDao import UsuarioDao
from daos.AtivoDao import AtivoDao
from daos.OperacaoDao import OperacaoDao
import requests


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
ativo_dao = AtivoDao(db)
operacao_dao = OperacaoDao(db)


def usuario_logado():
    if ('usuario_logado' not in session or session['usuario_logado'] == None):
        return False
    else:
        return True

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
            session['usuario_logado'] = [usuario.id, usuario.nome]
            flash('Bem vindo, ' + usuario.nome + ' !')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    flash('Usuário ou senha incorretos. Tente novamente!')
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Nenhum usuário logado!')
    return redirect(url_for('home'))

@app.route('/')
def home():
    ativos=None
    if session['usuario_logado']:
        id_usuario_logado = session['usuario_logado'][0]
        dados = operacao_dao.carteira_sumarizada(id_usuario_logado)
        ativos = transforma_sumarizado(dados)
    return render_template('index.html', ativos=ativos)


@app.route('/usuario/novo')
def novo_usuario():
    return render_template('novo_usuario.html', titulo='Cadastro')




@app.route('/usuario/criar', methods=['post', ])
def criar_usuario():
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']

    usuario_cadastrado = usuario_dao.busca_por_email(email)

    if usuario_cadastrado:
        flash('E-mail ' + email + ' já cadastrado!')
        return redirect(url_for('novo_usuario'))

    usuario = Usuario(nome, email, senha)
    usuario_dao.salvar(usuario)
    flash('Usuário cadastrado com sucesso!')
    return redirect(url_for('home'))


@app.route('/operacao/novo')
def nova_operacao():

    if usuario_logado():
        ativos = ativo_dao.buscar()
        return render_template('nova_operacao.html', titulo='Registro de Operações', ativos = ativos)
    else:
        return redirect(url_for('login', proxima=url_for('nova_operacao')))


@app.route('/operacao/criar', methods=['post', ])
def criar_operacao():
    ativo = int(request.form['ativo'])
    tipo = request.form['tipo']
    data = request.form['data']
    quantidade = int(request.form['quantidade'])
    valor = request.form['valor']

    operacao = Operacao(ativo, tipo, data, quantidade, valor)

    operacao_dao.salvar(operacao)

    return redirect(url_for('home'))

def transforma_sumarizado(dados):
    ativos = []

    for dado in dados:
        ativo = dado[0]
        quantidade = int(dado[1])
        valor_aplicado = dado[2]
        preco_medio_cota = valor_aplicado / quantidade
        # valor_atual_cota = obter_quote(ativo)
        # valor_total_atual = quantidade * valor_atual_cota
        # valorizacao = ((valor_total_atual*100)/valor_aplicado)-100

        ativos.append({
            'ativo':ativo,
            'quantidade':quantidade,
            'valor_aplicado':"{:.2f}".format(valor_aplicado),
            'preco_medio_cota':"{:.2f}".format(preco_medio_cota)
            # 'valor_atual_cota': "{:.2f}".format(valor_atual_cota),
            # 'valor_total_atual': "{:.2f}".format(valor_total_atual),
            # 'valorizacao':"{:.2f}".format(valorizacao)
        })

    return ativos

def obter_quote(ativo):
    ativo = ativo + '.SA'
    request = requests.get(f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ativo}&apikey=TY0JZ9D31XLVDW4B')
    dados = request.json()
    preco_atual = dados['Global Quote']['05. price']
    return float(preco_atual)

app.run(debug=True)
