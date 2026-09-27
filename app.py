from flask import Flask, render_template, request,url_for,redirect
import requests


app = Flask(__name__)


# @app.route("/contatos", methods=['GET'])
# def contatos():
#     return "<h1> Página Contatos </h1>"

# # aluno = ["Fulano","Cicrano","Beltrano"]

# nome = "tiago"
# sobrenome = "marinho"
# curso = "ADS"
# data_nasc = "02-09-1994"

# alunos = {
#     "nome": nome,
#     "sobrenome": sobrenome,
#     "curso": curso,
#     "data_nascimento": data_nasc

# }

# @app.route("/cadastro", methods=['GET', 'POST'])
# def cadastro():
#     if request.method == 'POST':

#         nome = request.form.get('nome')
#         sobrenome = request.form.get('sobrenome')
#         curso = request.form.get('curso')
#         data_nasc = request.form.get('datanascimento')

#         alunos = {
#             "nome": nome,
#             "sobrenome": sobrenome,
#             "curso": curso,
#             "data_nascimento": data_nasc

#         }

#         return render_template("alunos.html", alunos=alunos)

#     return render_template("cadastro.html")



# @app.route("/aluno", methods=['GET'])
# def aluno():
#     return render_template("alunos.html", alunos=alunos)

# @app.route("/produtos_api" , methods=['GET', 'POST'])
# def produtos_api():
#     response = requests.get('https://fakestoreapi.com/products')
#     dados = response.json()

#     return render_template("produtos.html", dados=dados)


# Pagina inicial do sistema
@app.route("/", methods=['GET'])
def index():
    return render_template("index.html")
# pagina de login do sistema
@app.route('/login')
def login():
    return render_template('login.html')
# processamento do login do sistema
@app.route("/processar_login", methods=['POST'])
def processar_login():
    user = request.form.get('user')
    senha = request.form.get('senha')

    if user == "admin" and senha == "admin":
        return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))
    

# Gerar a lista de páginas para o menu
def generate_page_list():
    pages = [
        {"name": "Home", "url": url_for("home")},
        {"name": "Notícias", "url": url_for("noticias")},
        # {"name": "Noticias", "url": url_for("nova_noticia")},
        {"name": "Cardápio", "url": url_for("cardapio")},
        {"name": "Eventos", "url": url_for("eventos")},
        {"name": "Confirmações", "url": url_for("confirmacao")},
        {"name": "Configurações", "url": url_for("configuracao")},
        {"name": "Sair", "url": url_for("sair")}
    ]
    return pages

# Rotas para as páginas do sistema
@app.route('/home', methods=['GET'])
def home():
    minhas_paginas = generate_page_list()
    return render_template('home.html', pages=minhas_paginas)

# rota para a página de notícias, que exibe a lista de páginas no menu

@app.route('/noticias', methods=['GET'])
def noticias():
    minhas_paginas = generate_page_list()
    return render_template('noticias.html', pages=minhas_paginas)

@app.route('/noticias/nova', methods=['POST', 'GET'])
def nova_noticia():
    minhas_paginas = generate_page_list()
    mensagem = None
    if request.method == 'POST':
        mensagem = 'Formulário recebido, mas as notícias ainda não são salvas.' 
    return render_template('cad_noticia.html', pages=minhas_paginas, mensagem=mensagem)

@app.route('/cardapio', methods=['GET'])
def cardapio():
        minhas_paginas = generate_page_list()
        return render_template('cardapio.html', pages=minhas_paginas)

@app.route('/cardapio/nova', methods=['POST', 'GET'])
def nova_cardapio():
    minhas_paginas = generate_page_list()
    mensagem = None
    if request.method == 'POST':
        mensagem = 'Formulário recebido, mas os cardápios ainda não são salvos.' 
    return render_template('cad_cardapio.html', pages=minhas_paginas, mensagem=mensagem)

@app.route('/eventos', methods=['GET'])
def eventos():
    minhas_paginas = generate_page_list()
    return render_template('agenda.html', pages=minhas_paginas)

@app.route('/eventos/novo', methods=['POST', 'GET'])
def novo_evento():
    minhas_paginas = generate_page_list()
    mensagem = None
    if request.method == 'POST':
        mensagem = 'Formulário recebido, mas os eventos ainda não são salvos.' 
    return render_template('cad_eventos.html', pages=minhas_paginas, mensagem=mensagem)

@app.route('/confirmacoes', methods=['GET'])
def confirmacao():
    return "<h1>Confirmações</h1>"

@app.route('/configuracoes', methods=['GET'])
def configuracao():
    return "<h1>Configurações</h1>"

@app.route('/sair', methods=['GET'])
def sair():
    return "<h1>Sair (sair)</h1>"

if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port=5000, debug=True)




