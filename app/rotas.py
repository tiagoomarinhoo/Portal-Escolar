from flask import Flask, render_template, url_for

app = Flask(__name__)

# 1. Função do menu sem a necessidade do site_id
def generate_page_list():
    pages = [
        {"name": "Home", "url": url_for("home")},
        {"name": "Eventos", "url": url_for("events")},
        {"name": "Notícias", "url": url_for("news")}
    ]
    return pages

# 2. Rota limpa apontando para /home
@app.route('/home', methods=['GET'])
def home():
    minhas_paginas = generate_page_list()
    return render_template('home.html', pages=minhas_paginas)