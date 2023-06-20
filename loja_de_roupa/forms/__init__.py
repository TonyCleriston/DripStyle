from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, length, Email,equal_to
from wtforms.widgets import TextArea


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
    min_estoque = StringField('Estoque Desejado', validators=[DataRequired(), length(1, 5)])
    tamanho = StringField('Tamanho', validators=[DataRequired(), length(1,10)])
    nome_roupa_del = StringField('Nome da Roupa', validators=[DataRequired(), length(1,70)])
    descricao = StringField('Descrição',widget=TextArea(), validators=[DataRequired(), length(1, 300)])
    nome_usuario_del = StringField('Nome da Usuário', validators=[DataRequired(), length(7,30)])
    nome_categoria_add = StringField('Adicionar Categoria', validators=[length(1, 30)])
    nome_categoria_del = StringField('Remover Categoria', validators=[length(1, 30)])
    nome_estoque_add = StringField('Nome da Roupa', validators=[length(1,70)])
    nome_estoque_del = StringField('Nome da Roupa', validators=[length(1,70)])
    qtd_estoque_add = StringField('Quantidade Adicionada',validators=[length(1,10)])
    qtd_estoque_del = StringField('Quantidade Removida',validators=[length(1,10)])
    enviar_novidades = BooleanField('Enviar Novidades', render_kw={'class': 'checkbox-container','style': 'font-size:21px;font-weight:bold;'})
    submit_add_categoria = SubmitField('Adicionar')
    submit_del_categoria = SubmitField('Remover')
    submit_add_estoque = SubmitField('Adicionar')
    submit_del_estoque = SubmitField('Remover')
    submit_adc_roupa = SubmitField('Adicionar')
    submit_del_roupa = SubmitField('Remover')
    submit_del_usuario = SubmitField('Remover')

class VendaForm(FlaskForm):
    cashback_checkbox = BooleanField('Usar CashBack')
    roupa_venda = StringField('Produtos: ')
    email_cliente = StringField('Email')
    telefone_cliente = StringField('Telefone')
    roupa_vendida = StringField()
    qtd_estoque_venda = StringField('Quantidade: ', validators=[DataRequired(), length(1,1000)])
    valor_total = StringField('Valor Total da Venda: R$0', validators=[length(1,1000)])
    valor_unitario = StringField()
    nome_cliente = StringField('Nome do Cliente', validators=[length(1,70)])
    cpf = StringField('CPF', validators=[length(1,11)])
    tipo_pagamento = StringField('Forma de Pagamento')
    submit_venda = SubmitField('Vender')
