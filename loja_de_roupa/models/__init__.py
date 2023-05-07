from loja_de_roupa import database , login_manager
from flask_login import UserMixin
@login_manager.user_loader
def load_usuario(id):
    return Usuario.query.get(int(id))
class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    usuario = database.Column(database.String, nullable=False, unique=True)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)

class Roupas(database.Model):
    id_roupas = database.Column(database.Integer, primary_key=True)
    nome_roupa = database.Column(database.String, nullable=False, unique=True)
    categoria = database.Column(database.String, nullable=False)
    tamanho = database.Column(database.String, nullable=False)
    estoque = database.Column(database.Integer, nullable=False)
    valor = database.Column(database.Float, nullable=False)

class Categoria(database.Model):
    id_categoria = database.Column(database.Integer, primary_key=True)
    nome_categoria = database.Column(database.String, nullable=False, unique=True)
