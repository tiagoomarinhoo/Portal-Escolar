from datetime import date, datetime, timedelta
import os
import uuid
from flask import Flask, current_app, render_template, request, url_for, redirect
import requests
from flask_sqlalchemy import SQLAlchemy
from app import app, db
from app.models import Noticia , Cardapio , CardapioAlimentos, CardapioSobremesa, CardapioAlegeno ,  Usuario
from flask_admin import Admin
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
from flask_login import LoginManager, login_user , logout_user, login_required, current_user , UserMixin
import hashlib


lm = LoginManager()
lm.init_app(app)

lm.login_view = 'login'


def hash_password(txt):
    hash_object = hashlib.sha256(txt.encode('utf-8'))
    return hash_object.hexdigest()


@lm.user_loader
def user_loader(user_id):
    usuario = db.session.query(Usuario).filter_by(id=user_id).first()
    return usuario




#Pagina inicial do sistema
@app.route("/", methods=['GET'])
def index():
    return render_template("index.html")

# pagina de login do sistema
@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        email = request.form.get('email', '').strip()
        senha = request.form.get('senha', '')
        
        user = db.session.query(Usuario).filter_by(email=email).first()
        if not user or not user.is_active or not check_password_hash(user.senha_hash, senha):
            return render_template('login.html', error='Usuário ou senha inválidos.')
        login_user(user)
        return redirect(url_for('home'))
        
        
    
# processamento do login do sistema


# @app.route("/processar_login", methods=['POST'])
# def processar_login():
#     user = request.form.get('user')
#     senha = request.form.get('senha')

#     if user == "admin" and senha == "admin":
#         return redirect(url_for('home'))
#     else:
#         return redirect(url_for('login'))
    

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
@login_required
def home():
    minhas_paginas = generate_page_list()
    return render_template('home.html', pages=minhas_paginas)

# rota para a página de notícias, que exibe a lista de páginas no menu

@app.route('/noticias', methods=['GET'])
def noticias():
    minhas_paginas = generate_page_list()
    noticias_publicadas = Noticia.query.order_by(
        Noticia.publicado_em.desc(), Noticia.id.desc()
    ).all()
    return render_template(
        'noticias.html', pages=minhas_paginas, noticias=noticias_publicadas
    )

@app.route('/noticias/<int:noticia_id>')
def detalhe_noticia(noticia_id):
    noticia = Noticia.query.get_or_404(noticia_id)
    return render_template(
        'detalhe_noticia.html', pages=generate_page_list(), noticia=noticia
    )

def tamanho_upload(arquivo):
    posicao = arquivo.stream.tell()
    arquivo.stream.seek(0, os.SEEK_END)
    tamanho = arquivo.stream.tell()
    arquivo.stream.seek(posicao)
    return tamanho

@app.route('/noticias/nova', methods=['POST', 'GET'])
def nova_noticia():
    minhas_paginas = generate_page_list()
    mensagem = None

    if request.method == 'POST':
        titulo = request.form.get('titulo', '').strip()
        categoria = request.form.get('categoria', '').strip()
        resumo = request.form.get('resumo', '').strip()
        conteudo = request.form.get('conteudo', '').strip()
        status = request.form.get('status', '').strip()
        destaque = request.form.get('destaque') == 'on'
        data_texto = request.form.get('data_publicacao', '').strip()
        imagem = request.files.get('imagem')
        anexos_enviados = request.files.getlist('anexos')
        titulos_prazo = request.form.getlist('prazo_titulo')
        datas_prazo = request.form.getlist('prazo_data')

        try:
            data_publicacao = date.fromisoformat(data_texto)
        except ValueError:
            data_publicacao = None

        categorias_validas = {'geral', 'aviso', 'conquista'}
        status_validos = {'rascunho', 'publicado', 'agendado', 'PUBLICADA'}
        extensoes_imagem = {'.jpg', '.jpeg', '.png'}
        imagem_nome = secure_filename(imagem.filename) if imagem and imagem.filename else ''

        if imagem_nome and os.path.splitext(imagem_nome)[1].lower() not in extensoes_imagem:
            mensagem = 'A imagem deve estar no formato JPG ou PNG.'
        elif imagem_nome and tamanho_upload(imagem) > 5 * 1024 * 1024:
            mensagem = 'A imagem deve ter no máximo 5 MB.'
        elif not titulo or not resumo or not conteudo or categoria not in categorias_validas or status not in status_validos or data_publicacao is None:
            mensagem = 'Preencha título, resumo, categoria, status, data e conteúdo corretamente.'
        else:
            noticia = Noticia(
                titulo=titulo,
                categoria=categoria,
                resumo=resumo,
                destaque=destaque,
                status=status,
                conteudo=conteudo,
                autor_id=1,
                publicado_em=datetime.combine(data_publicacao, datetime.min.time()),
            )

            pasta_upload = os.path.join(current_app.static_folder, 'uploads', 'noticias')
            os.makedirs(pasta_upload, exist_ok=True)
            arquivos_salvos = []
            try:
                if imagem_nome:
                    nome_unico = f'{uuid.uuid4().hex}_{imagem_nome}'
                    imagem.save(os.path.join(pasta_upload, nome_unico))
                    noticia.imagem = f'uploads/noticias/{nome_unico}'
                    arquivos_salvos.append(os.path.join(pasta_upload, nome_unico))

                db.session.add(noticia)
                db.session.commit()
            except Exception:
                db.session.rollback()
                for caminho in arquivos_salvos:
                    if os.path.exists(caminho):
                        os.remove(caminho)
                raise
            return redirect(url_for('noticias'))

    return render_template(
        'cad_noticia.html',
        pages=minhas_paginas,
        mensagem=mensagem,
        form_data=request.form,
        hoje=date.today().isoformat(),
    )

@app.route('/cardapio', methods=['GET'])
def cardapio():
    minhas_paginas = generate_page_list()
    data_texto = request.args.get('data', date.today().isoformat()).strip()
    modo = request.args.get('modo', 'dia')
    if modo not in {'dia', 'semana'}:
        modo = 'dia'

    try:
        data_selecionada = date.fromisoformat(data_texto)
    except ValueError:
        data_selecionada = date.today()

    nomes_dias = (
        'Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira',
        'Sexta-feira', 'Sábado', 'Domingo',
    )
    abreviacoes_dias = ('Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom')

    if modo == 'semana':
        inicio_semana = data_selecionada - timedelta(days=data_selecionada.weekday())
        dias = [inicio_semana + timedelta(days=offset) for offset in range(5)]
        fim_semana = dias[-1]
        semana_anterior = (inicio_semana - timedelta(days=7)).isoformat()
        semana_seguinte = (inicio_semana + timedelta(days=7)).isoformat()
        cardapios_semana = Cardapio.query.filter(
            Cardapio.data >= dias[0],
            Cardapio.data <= fim_semana,
        ).order_by(Cardapio.data, Cardapio.refeicao).all()
        cardapios_por_dia = {dia: [] for dia in dias}
        for menu in cardapios_semana:
            cardapios_por_dia[menu.data].append(menu)

        alergenos_semana = sorted(
            {
                alergeno.nome
                for menu in cardapios_semana
                for alergeno in menu.alegenos
            },
            key=lambda nome: nome.casefold(),
        )

        dias_exibidos = [
            {
                'data': dia,
                'nome': nomes_dias[dia.weekday()],
                'abreviacao': abreviacoes_dias[dia.weekday()],
                'cardapios': cardapios_por_dia[dia],
            }
            for dia in dias
        ]
    else:
        inicio_semana = None
        fim_semana = None
        semana_anterior = None
        semana_seguinte = None
        alergenos_semana = []
        cardapios_do_dia = Cardapio.query.filter_by(
            data=data_selecionada
        ).order_by(Cardapio.refeicao).all()
        dias_exibidos = [{
            'data': data_selecionada,
            'nome': nomes_dias[data_selecionada.weekday()],
            'abreviacao': abreviacoes_dias[data_selecionada.weekday()],
            'cardapios': cardapios_do_dia,
        }]

    data_formatada = data_selecionada.strftime('%d/%m/%Y')
    
    return render_template(
        'cardapio.html',
        pages=minhas_paginas,
        dias_exibidos=dias_exibidos,
        modo=modo,
        inicio_semana=inicio_semana,
        fim_semana=fim_semana,
        semana_anterior=semana_anterior,
        semana_seguinte=semana_seguinte,
        alergenos_semana=alergenos_semana,
        data_selecionada=data_selecionada.isoformat(),
        data_formatada=data_formatada,
    )
    
    
        

@app.route('/cardapio/nova', methods=['POST', 'GET'])
def nova_cardapio():
    minhas_paginas = generate_page_list()
    mensagem = None
    
    if request.method == 'POST':
        data_texto = request.form.get('data', '').strip()
        refeicao = request.form.get('refeicao', '').strip()
        alimentos = [
            item.strip()
            for item in request.form.get('alimentos', '').split(';')
            if item.strip()
        ]
        sobremesas = [
            item.strip()
            for item in request.form.get('sobremesa', '').split(';')
            if item.strip()
        ]
        alergenos = request.form.getlist('alergenos')
 

        try:
            data_cardapio = date.fromisoformat(data_texto)
        except ValueError:
            data_cardapio = None

        if not data_cardapio or refeicao not in {'Almoço', 'Jantar'}:
            mensagem = 'Preencha uma data válida e selecione a refeição.'
        elif Cardapio.query.filter_by(
            data=data_cardapio, refeicao=refeicao
        ).first():
            mensagem = 'Já existe um cardápio para esta data e refeição.'
        else:
            novo_cardapio = Cardapio(
                data=datetime.combine(data_cardapio, datetime.min.time()),
                refeicao=refeicao,
                observacoes=request.form.get('observacoes', '').strip() or None,
            )
            novo_cardapio.itens_alimentos = [
                CardapioAlimentos(nome=item) for item in alimentos
            ]
            novo_cardapio.itens_sobremesas = [
                CardapioSobremesa(nome=item) for item in sobremesas
            ]
            novo_cardapio.alegenos = [
                CardapioAlegeno(nome=item) for item in alergenos
            ]

            db.session.add(novo_cardapio)
            db.session.commit()
            return redirect(url_for('cardapio'))
    return render_template('cad_cardapio.html', pages=minhas_paginas, mensagem=mensagem,)

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

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)



