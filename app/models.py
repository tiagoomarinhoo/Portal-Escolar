from datetime import date, datetime

from app import db
from flask_login import UserMixin

class Usuario(UserMixin, db.Model):
    __tablename__ = "usuarios"
    
    id = db.Column(db.BigInteger, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    perfil = db.Column(db.String(50), nullable=False)
    ativo = db.Column(db.Boolean, nullable=True, default=True)
    criado_em = db.Column(
        db.DateTime, nullable=True, server_default=db.func.current_timestamp()
    )

    @property
    def is_active(self):
        return bool(self.ativo)

class Item(db.Model):
    __tablename__ = "itens"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)


class Noticia(db.Model):
    __tablename__ = "noticias"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    resumo = db.Column(db.String(500), nullable=True)
    conteudo = db.Column(db.Text, nullable=False)
    categoria = db.Column(db.String(50), nullable=False, default="geral")
    imagem_url = db.Column(db.String(500), nullable=True)
    imagem_alt = db.Column(db.String(200), nullable=True)
    destaque = db.Column(db.Boolean, nullable=False, default=False)
    status = db.Column(db.String(20), nullable=False, default="PUBLICADA")
    autor_id = db.Column(db.Integer, nullable=False, default=1)
    publicado_em = db.Column(db.DateTime, nullable=True)
    atualizado_em = db.Column(db.DateTime, nullable=True, default=db.func.current_timestamp())

    @property
    def data_publicacao(self):
        if self.publicado_em is None:
            return date.today()
        if isinstance(self.publicado_em, datetime):
            return self.publicado_em.date()
        return self.publicado_em

    @data_publicacao.setter
    def data_publicacao(self, value):
        if isinstance(value, datetime):
            self.publicado_em = value
        else:
            self.publicado_em = datetime.combine(value, datetime.min.time())

    @property
    def imagem(self):
        return self.imagem_url

    @imagem.setter
    def imagem(self, value):
        self.imagem_url = value


class Cardapio(db.Model):
    __tablename__ = "cardapios"
    __table_args__ = ( 
        db.UniqueConstraint("data", "refeicao", name="uq_cardapio_data_refeicao"),
     )

    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date, nullable=False)
    refeicao = db.Column(db.String(50), nullable=False)
    # alimentos = db.Column(db.Text, nullable=False)
    # sobremesas = db.Column(db.Text, nullable=True)
    observacoes = db.Column(db.Text, nullable=True)
    
    itens_alimentos = db.relationship("CardapioAlimentos", back_populates="cardapio", cascade="all, delete-orphan")
    
    itens_sobremesas = db.relationship("CardapioSobremesa", back_populates="cardapio", cascade="all, delete-orphan")
    
    
    alegenos = db.relationship("CardapioAlegeno", back_populates="cardapio", cascade="all, delete-orphan")
    
class CardapioAlimentos(db.Model):
    __tablename__ = "cardapio_itens"
    __table_args__ = (
        db.UniqueConstraint("cardapio_id", "nome", name="uq_cardapio_item"),
    )
    
    id = db.Column(db.Integer, primary_key=True)
    cardapio_id = db.Column(db.Integer, db.ForeignKey("cardapios.id"), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    
    cardapio = db.relationship("Cardapio", back_populates="itens_alimentos")
    
class CardapioSobremesa(db.Model):
    __tablename__ = "cardapio_sobremesas"
    __table_args__ = (
        db.UniqueConstraint("cardapio_id", "nome", name="uq_cardapio_sobremesa"),
    )
    
    id = db.Column(db.Integer, primary_key=True)
    cardapio_id = db.Column(db.Integer, db.ForeignKey("cardapios.id"), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    
    cardapio = db.relationship("Cardapio", back_populates="itens_sobremesas")
    
class CardapioAlegeno(db.Model):
    __tablename__ = "cardapio_alergenos"
    __table_args__ = (
        db.UniqueConstraint("cardapio_id", "nome", name="uq_cardapio_alergeno"),
    )
    
    id = db.Column(db.Integer, primary_key=True)
    cardapio_id = db.Column(db.Integer, db.ForeignKey("cardapios.id"), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    
    cardapio = db.relationship("Cardapio", back_populates="alegenos")
