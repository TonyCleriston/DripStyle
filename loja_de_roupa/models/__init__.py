from loja_de_roupa import database, login_manager
from flask_login import UserMixin
import datetime
import pytz
@login_manager.user_loader
def load_usuario(id):
    return Usuario.query.get(id)
class Usuario(database.Model, UserMixin):
    id = database.Column(database.String(3), nullable=False, primary_key=True)
    usuario = database.Column(database.String, nullable=False, unique=True)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)

class Roupas(database.Model):
    id_roupas = database.Column(database.Integer, primary_key=True)
    nome_roupa = database.Column(database.String, nullable=False, unique=True)
    categoria = database.Column(database.String, nullable=False)
    tamanho = database.Column(database.String, nullable=False)
    estoque = database.Column(database.Integer, nullable=False)
    min_estoque = database.Column(database.Integer)
    valor = database.Column(database.Float, nullable=False)
    descricao = database.Column(database.String)

class Categoria(database.Model):
    id_categoria = database.Column(database.Integer, primary_key=True)
    nome_categoria = database.Column(database.String, nullable=False, unique=True)

class Cliente(database.Model):
    id_cliente = database.Column(database.Integer, primary_key=True)
    nome_cliente = database.Column(database.String, nullable=False)
    cpf = database.Column(database.String, nullable=False, unique=True)
    cashback = database.Column(database.Float)
    data_validade_cashback = database.Column(database.String)
class Promocao(database.Model):
    id_promo = database.Column(database.Integer, primary_key=True)
    porcentagem = database.Column(database.String, nullable=False)
    tipo_pagamento = database.Column(database.String, nullable=False)
class Cashback(database.Model):
    id_cash = database.Column(database.Integer, primary_key=True)
    min_cashback = database.Column(database.String, nullable=False)
    validade_adicionada = database.Column(database.String, nullable=False)

class Vendas(database.Model):
    id_venda = database.Column(database.Integer, primary_key=True)
    codigo_pedido = database.Column(database.Integer)
    roupas_fk = database.Column(database.String, nullable=False)
    valor_unitario = database.Column(database.Float)
    valor_total = database.Column(database.Float)
    qtd = database.Column(database.Integer)
    nome_cliente = database.Column(database.String, nullable=False)
    total_da_venda = database.Column(database.Float, nullable=False)
    tipo_pagamento_fk = database.Column(database.String)
    vendedor = database.Column(database.String)
    fuso_horario = pytz.timezone('America/Sao_Paulo')
    data_hora_atual = datetime.datetime.now(fuso_horario)
    data_da_venda = database.Column(database.DateTime, default=data_hora_atual)



