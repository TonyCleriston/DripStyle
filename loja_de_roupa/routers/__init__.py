from flask import render_template, url_for, redirect, flash, request
from loja_de_roupa.forms import FormLogin, FormCadastroUsuario, FormGerenciamentoRoupas , VendaForm
from loja_de_roupa import app, database
from loja_de_roupa.models import Usuario, Roupas, Categoria
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from flask_login import login_required , login_user , logout_user


@app.route('/logout')
def logout():
    logout_user()
    flash('Sessão Encerrada!','alert-success')
    return redirect(url_for('login'))
@app.route("/", methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    if request.method == 'POST':
        if not form_login.validate_on_submit():

            usuario_login_validado = form_login.usuario.data.upper()
            user = Usuario.query.filter_by(usuario=usuario_login_validado).first()
            if user and check_password_hash(user.senha, form_login.senha.data):
                login_user(user)
                flash(f'login feito com sucesso pelo usuário: {form_login.usuario.data.lower()}', 'alert-success')
                return redirect(url_for('roupas'))
            else:
                flash('Usuário ou senha incorretos!', 'alert-danger')
                return redirect(url_for('login'))
    return render_template("login.html", form_login=form_login) #constrói um código em html


@app.route("/roupas",methods=['GET', 'POST'])
@login_required
def roupas():
    gerenciamento = FormGerenciamentoRoupas()
    table = Roupas.query.all()
    roupas = [{'id': r.id_roupas, 'nome_roupa': r.nome_roupa, 'categoria':r.categoria, 'tamanho': r.tamanho,'estoque': r.estoque,'valor': r.valor} for r in table]
    categorias = Categoria.query.all()
    categoria = [{'id': c.id_categoria,'categoria': c.nome_categoria} for c in categorias]
    if request.method == 'POST':
        if gerenciamento.submit_adc_roupa.name in request.form:
            if not gerenciamento.validate_on_submit():
                try:
                    nome_roupa_adc_validado = gerenciamento.nome_roupa_adc.data.upper()
                    valor_validado = gerenciamento.valor.data.replace(",",".")
                    categoria_validado = gerenciamento.categoria.data.upper()
                    tamanho_validado = gerenciamento.tamanho.data.upper()
                    roupa = Roupas(nome_roupa=nome_roupa_adc_validado, categoria=categoria_validado,tamanho=tamanho_validado,estoque=gerenciamento.estoque.data,valor=valor_validado)
                    database.session.add(roupa)
                    database.session.commit()
                    flash(f'{gerenciamento.nome_roupa_adc.data} cadastrada com sucesso', 'alert-success')
                    return redirect(url_for('roupas'))
                except:
                    flash(f'Erro ao cadastrar Roupa', 'alert-danger')
                    return redirect(url_for('roupas'))
        if gerenciamento.submit_add_categoria.name in request.form:
            if not gerenciamento.validate_on_submit():
                try:
                    nome_categoria_add_validado = gerenciamento.nome_categoria_add.data.upper()
                    categoria = Categoria(nome_categoria=nome_categoria_add_validado)
                    database.session.add(categoria)
                    database.session.commit()
                    flash(f'{gerenciamento.nome_categoria_add.data} cadastrada com sucesso', 'alert-success')
                    return redirect(url_for('roupas'))
                except:
                    flash(f'Erro ao cadastrar Categoria', 'alert-danger')
                    return redirect(url_for('roupas'))
        if gerenciamento.submit_add_estoque.name in request.form:
            if not gerenciamento.validate_on_submit():
                try:
                    estoque = Roupas.query.filter_by(nome_roupa=gerenciamento.nome_estoque_add.data.upper()).first()
                    if int(gerenciamento.qtd_estoque_add.data) < 0:
                        flash(f'Erro ao Aumentar Estoque', 'alert-danger')
                        return redirect(url_for('roupas'))
                    if estoque:
                        estoque.estoque += int(gerenciamento.qtd_estoque_add.data)
                    else:
                        flash(f'Roupa Não Encontrada', 'alert-danger')
                        return redirect(url_for('roupas'))
                    database.session.commit()
                    flash(f'{gerenciamento.nome_estoque_add.data} teve o estoque aumentado com sucesso', 'alert-success')
                    return redirect(url_for('roupas'))
                except:
                    flash(f'Erro ao Adicionar Estoque', 'alert-danger')
                    return redirect(url_for('roupas'))
        if gerenciamento.submit_del_estoque.name in request.form:
            if not gerenciamento.validate_on_submit():
                try:
                    estoque = Roupas.query.filter_by(nome_roupa=gerenciamento.nome_estoque_del.data.upper()).first()
                    if int(gerenciamento.qtd_estoque_del.data) < 0:
                        flash(f'Erro ao Diminuir Estoque', 'alert-danger')
                        return redirect(url_for('roupas'))
                    if estoque:
                        estoque.estoque -= int(gerenciamento.qtd_estoque_del.data)
                    else:
                        flash(f'Erro ao Diminuir Estoque', 'alert-danger')
                        return redirect(url_for('roupas'))
                    if estoque.estoque < 0:
                        flash(f'Erro ao Diminuir Estoque', 'alert-danger')
                        return redirect(url_for('roupas'))
                    database.session.commit()
                    flash(f'{gerenciamento.nome_estoque_del.data} teve o estoque removido com sucesso', 'alert-success')
                    return redirect(url_for('roupas'))
                except:
                    flash(f'Erro ao Diminuir Estoque', 'alert-danger')
                    return redirect(url_for('roupas'))
        if gerenciamento.submit_del_roupa.name in request.form:
            if not gerenciamento.validate_on_submit():
                roupa = Roupas.query.filter_by(nome_roupa=gerenciamento.nome_roupa_del.data.upper()).all()
                try:
                    if not roupa:
                        flash(f'Essa roupa não existe', 'alert-danger')
                        return redirect(url_for('roupas'))
                    for r in roupa:
                        database.session.delete(r)
                        database.session.commit()
                        flash(f'{gerenciamento.nome_roupa_del.data} apagada com sucesso', 'alert-success')
                    return redirect(url_for('roupas'))
                except:
                    flash(f'Erro ao deletar Roupa', 'alert-danger')
                    return redirect(url_for('roupas'))
        if gerenciamento.submit_del_categoria.name in request.form:
            if not gerenciamento.validate_on_submit():
                categoria = Categoria.query.filter_by(nome_categoria=gerenciamento.nome_categoria_del.data.upper()).all()
                try:
                    if not categoria:
                        flash(f'Não existe essa categoria', 'alert-danger')
                        return redirect(url_for('roupas'))
                    for c in categoria:
                        database.session.delete(c)
                        database.session.commit()
                        flash(f'{gerenciamento.nome_categoria_del.data} apagada com sucesso', 'alert-success')
                    return redirect(url_for('roupas'))
                except:
                    flash(f'Erro ao deletar Categoria', 'alert-danger')
                    return redirect(url_for('roupas'))
        if gerenciamento.submit_del_usuario.name in request.form:
            if not gerenciamento.validate_on_submit():
                usuario_deletado_validado = gerenciamento.nome_usuario_del.data.upper()
                user = Usuario.query.filter_by(usuario=usuario_deletado_validado).all()
                try:
                    if not user:
                        flash(f'Erro ao deletar Usuário', 'alert-danger')
                        return redirect(url_for('roupas'))
                    for u in user:
                        database.session.delete(u)
                        database.session.commit()
                        flash(f'{gerenciamento.nome_usuario_del.data} apagado(a) com sucesso', 'alert-success')
                    return redirect(url_for('roupas'))
                except:
                    flash(f'Erro ao deletar Usuário', 'alert-danger')
                    return redirect(url_for('roupas'))


    return render_template('gerenciamentoRoupas.html',gerenciamento=gerenciamento,data=[{'name':'Blusa'}],roupas=roupas,categoria=categoria)


@app.route("/cadastro", methods=['GET', 'POST'])
@login_required
def cadastro():
    form_cadastro_usuario = FormCadastroUsuario()
    if request.method == 'POST':
        if not form_cadastro_usuario.validate_on_submit():
            try:
                usuario_cadastro_validado = form_cadastro_usuario.usuario.data.upper()
                senha = form_cadastro_usuario.senha.data
                senha_criptografada = generate_password_hash(senha)
                usuario = Usuario(usuario=usuario_cadastro_validado, email=form_cadastro_usuario.email.data, senha=senha_criptografada)
                database.session.add(usuario)
                database.session.commit()
                flash(f'{form_cadastro_usuario.usuario.data.lower()} cadastrado com sucesso', 'alert-success')
                return redirect(url_for('login'))
            except:
                flash(f'Erro ao cadastrar usuário, usuário ou email já existentes!', 'alert-danger')
                return redirect(url_for('cadastro'))
    return render_template('cadastro.html', form_cadastro_usuario=form_cadastro_usuario)

@app.route("/vendas", methods=['GET', 'POST'])
@login_required
def vendas():
    venda_form = VendaForm()
    table = Roupas.query.all()
    roupas = [{'id': r.id_roupas, 'nome_roupa': r.nome_roupa, 'categoria': r.categoria, 'tamanho': r.tamanho,
               'estoque': r.estoque, 'valor': r.valor} for r in table]
    if request.method == 'POST':
        if venda_form.submit_venda.name in request.form:
            if not venda_form.validate_on_submit():
                try:
                    valor_roupa_venda = venda_form.roupa_vendida.data
                    estoque = Roupas.query.filter_by(nome_roupa=valor_roupa_venda.upper()).first()
                    if int(venda_form.qtd_estoque_venda.data) < 0:
                        flash(f'Erro ao Vender a Roupa', 'alert-danger')
                        return redirect(url_for('roupas'))
                    print(estoque)
                    if estoque:
                        estoque.estoque -= int(venda_form.qtd_estoque_venda.data)
                    else:
                        flash(f'Erro ao Vender a Roupa', 'alert-danger')
                        return redirect(url_for('roupas'))
                    if estoque.estoque < 0:
                        flash(f'Erro ao Vender a Roupa', 'alert-danger')
                        return redirect(url_for('roupas'))
                    database.session.commit()
                    flash(f'{valor_roupa_venda} teve sua venda concluída com sucesso', 'alert-success')
                    return redirect(url_for('roupas'))
                except:
                    flash(f'Erro ao deletar Categoria', 'alert-danger')
                    return redirect(url_for('roupas'))



    return render_template('venda.html', venda_form=venda_form, roupas=roupas)
