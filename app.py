from flask import Flask, render_template, request,url_for
import requests
from livereload import Server  # Importe o Server


app = Flask(__name__)

# @app.route("/", methods=['GET'])
# def index():
#     return "<h1> Olá Programação com Flask</h1>"
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



# 1. Função do menu sem a necessidade do site_id
def generate_page_list():
    pages = [
        {"name": "Home", "url": url_for("home")},
        {"name": "Notícias", "url": url_for("noticias")},
        {"name": "Cardápio", "url": url_for("cardapio")},
        {"name": "Eventos", "url": url_for("eventos")},
        {"name": "Confirmações", "url": url_for("confirmacao")},
        {"name": "Configurações", "url": url_for("configuracao")},
        {"name": "Sair", "url": url_for("sair")}
    ]
    return pages

# 2. Rota limpa apontando para /home
@app.route('/home', methods=['GET'])
def home():
    minhas_paginas = generate_page_list()
    return render_template('home.html', pages=minhas_paginas)

@app.route('/noticias', methods=['GET'])
def noticias():
    minhas_paginas = generate_page_list()
    return render_template('noticias.html', pages=minhas_paginas)
    

@app.route('/cardapio', methods=['GET'])
def cardapio():
    return "<h1>Cardápio</h1>"

@app.route('/eventos', methods=['GET'])
def eventos():
    return "<h1>Eventos</h1>"

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




