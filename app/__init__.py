from functools import wraps
import unicodedata

from flask import Flask, abort
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, login_required

from config import Config

app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.config.from_object(Config)
app.secret_key = 'androiiid'  # Replace with a secure secret key

db = SQLAlchemy(app)


def _normalizar_perfil(perfil):
    return "".join(
        caractere
        for caractere in unicodedata.normalize("NFKD", perfil.strip().casefold())
        if not unicodedata.combining(caractere)
    )


def usuario_tem_perfil(*perfis):
    if not current_user.is_authenticated:
        return False
    perfil_usuario = _normalizar_perfil(current_user.perfil)
    return perfil_usuario in {_normalizar_perfil(perfil) for perfil in perfis}

@app.context_processor
def disponibilizar_permissoes():
    return {"usuario_tem_perfil": usuario_tem_perfil}


def requer_perfil(*perfis):
    if not perfis:
        raise ValueError("Informe pelo menos um perfil permitido.")

    def decorador(view):
        @wraps(view)
        @login_required
        def protegido(*args, **kwargs):
            if not usuario_tem_perfil(*perfis):
                abort(403)
            return view(*args, **kwargs)

        return protegido

    return decorador


from app.models import Item, Noticia

admin = Admin(
    app,
    name="Portal Escolar",
    url="/admin",
)


class PerfilAdminView(ModelView):
    def is_accessible(self):
        return usuario_tem_perfil("admin", "direção")


class ItemAdmin(PerfilAdminView):
    column_list = ["id", "name", "description"]
    column_searchable_list = ["name"]


class NoticiaAdmin(PerfilAdminView):
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