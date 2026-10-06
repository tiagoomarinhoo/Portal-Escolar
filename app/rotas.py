# from flask import Flask, render_template, url_for

# app = Flask(__name__)

# # 1. Função do menu sem a necessidade do site_id
# def generate_page_list():
#     pages = [
#         {"name": "Home", "url": url_for("home")},
#         {"name": "Eventos", "url": url_for("events")},
#         {"name": "Notícias", "url": url_for("news")}
#     ]
#     return pages

# # 2. Rota limpa apontando para /home
# @app.route('/home', methods=['GET'])
# def home():
#     minhas_paginas = generate_page_list()
#     return render_template('home.html', pages=minhas_paginas)

# from flask import request, redirect, url_for, render_template
# from app import app, db
# from app.models import Item

# @app.route('/')
# def index():
#     itens_ = Item.query.all()
#     return render_template('aqui.html', itens=itens_)


# @app.route ('/create', methons)