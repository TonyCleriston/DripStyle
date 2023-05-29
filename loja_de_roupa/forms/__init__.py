from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, length, Email,equal_to


class FormLogin(FlaskForm):
    usuario = StringField('Usuário', validators=[DataRequired(), length(7,30)])
    senha = PasswordField('Senha', validators=[DataRequired(), length(7,17)])
    submit_entrar = SubmitField('Entrar')

class FormRemUsu(FlaskForm):
    nome_usuario_del = StringField('Nome do Usuário', validators=[DataRequired(), length(7,30)])
    submit_del_usuario = SubmitField('Remover')


class FormCadastroUsuario(FlaskForm):
    usuario = StringField('Usuário', validators=[DataRequired(), length(7,30)]) #Mínimo de caracteres
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), length(7,17)])
    confirmacao = PasswordField('Confirmar senha', validators=[DataRequired(), equal_to('senha', message='As senhas devem ser iguais')])
    submit_cadastro_usuario = SubmitField('Cadastrar')

class FormGerenciamentoRoupas(FlaskForm):
    nome_roupa_adc = StringField('Nome da Roupa', validators=[DataRequired(), length(1,70)])
    valor = StringField('Valor', validators=[DataRequired(), length(1,10)])
    categoria = StringField('Categoria', validators=[DataRequired(), length(1,30)])
    estoque = StringField('Estoque', validators=[DataRequired(), length(1,5)])
    tamanho = StringField('Tamanho', validators=[DataRequired(), length(1,10)])
    nome_roupa_del = StringField('Nome da Roupa', validators=[DataRequired(), length(1,70)])
    nome_usuario_del = StringField('Nome da Usuário', validators=[DataRequired(), length(7,30)])
    nome_categoria_add = StringField('Adicionar Categoria', validators=[length(1, 30)])
    nome_categoria_del = StringField('Remover Categoria', validators=[length(1, 30)])
    nome_estoque_add = StringField('Nome da Roupa', validators=[length(1,70)])
    nome_estoque_del = StringField('Nome da Roupa', validators=[length(1,70)])
    qtd_estoque_add = StringField('Quantidade Adicionada',validators=[length(1,10)])
    qtd_estoque_del = StringField('Quantidade Removida',validators=[length(1,10)])
    submit_add_categoria = SubmitField('Adicionar')
    submit_del_categoria = SubmitField('Remover')
    submit_add_estoque = SubmitField('Adicionar')
    submit_del_estoque = SubmitField('Remover')
    submit_adc_roupa = SubmitField('Adicionar')
    submit_del_roupa = SubmitField('Remover')
    submit_del_usuario = SubmitField('Remover')

class VendaForm(FlaskForm):
    roupa_venda = StringField('Produtos')
    roupa_vendida = StringField()
    qtd_estoque_venda = StringField('Quantidade do Produto', validators=[DataRequired(), length(1,1000)])
    valor_total = StringField('Valor Total:', validators=[length(1,1000)])
    valor_unitario = StringField()
    nome_cliente = StringField('Nome do Cliente', validators=[length(1,70)])
    endereco = StringField('Endereço', validators=[length(1,70)])
    tipo_pagamento = StringField('Forma de Pagamento')
    submit_venda = SubmitField('Vender')