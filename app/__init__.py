from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from config import Config

app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.config.from_object(Config)
app.secret_key = 'androiiid'  # Replace with a secure secret key

db = SQLAlchemy(app)

from app.models import Item, Noticia

admin = Admin(
    app,
    name="Portal Escolar",
    url="/admin",
)


class ItemAdmin(ModelView):
    column_list = ["id", "name", "description"]
    column_searchable_list = ["name"]


class NoticiaAdmin(ModelView):
    column_list = [
        "id", "titulo", "categoria", "status", "destaque", "publicado_em"
    ]
    column_labels = {
        "titulo": "Título",
        "categoria": "Categoria",
        "resumo": "Resumo",
        "imagem_url": "Imagem principal",
        "imagem_alt": "Texto alternativo da imagem",
        "destaque": "Destaque",
        "status": "Status",
        "publicado_em": "Data de publicação",
        "conteudo": "Conteúdo",
        "autor_id": "Autor",
    }
    column_searchable_list = ["titulo", "conteudo"]
    column_filters = ["categoria", "publicado_em"]
    form_choices = {
        "categoria": [
            ("geral", "Geral"),
            ("aviso", "Aviso urgente"),
            ("conquista", "Conquista"),
        ]
    }


admin.add_view(ItemAdmin(Item, db.session))
admin.add_view(NoticiaAdmin(Noticia, db.session))