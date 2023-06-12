from flask import render_template, url_for, redirect, flash, request
from loja_de_roupa.forms import FormLogin, FormCadastroUsuario, FormGerenciamentoRoupas , VendaForm,FormRemUsu
from loja_de_roupa import app, database
from loja_de_roupa.models import Usuario, Roupas, Categoria, Promocao, Vendas, Cliente, Cashback
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from flask_login import login_required , login_user , logout_user, current_user
import requests
from twilio.rest import Client
account_sid = 'AC4bf9cd5aca8f16160b0ee9c8a10a6be6'
auth_token = '3745f5e66f7ab8f437adf2db1458ad06'
client = Client(account_sid, auth_token)

@app.route('/excluir/<int:r_id>', methods=['GET','POST'])
def excluir(r_id):
    roupa = Roupas.query.get(r_id)
    flash(f'{roupa.nome_roupa.capitalize()} foi excluida com sucesso', 'alert-success')
    database.session.delete(roupa)
    database.session.commit()

    return redirect(url_for('roupas'))


def generate_codigo():
    last_id = Usuario.query.order_by(Usuario.id.desc()).first()
    if last_id:
        new_id = str(int(last_id.id) + 1).zfill(3)
    else:
        new_id = '001'
    return new_id

@app.route('/editar/<int:r_id>', methods=['GET', 'POST'])
def editar(r_id):
    gerenciamento = FormGerenciamentoRoupas()
    try:

        valor_validado = gerenciamento.valor.data.replace(",", ".")
        nome_roupa_adc_validado = gerenciamento.nome_roupa_adc.data.upper()
        min_estoque_validado = gerenciamento.min_estoque.data
        if int(min_estoque_validado) < 0:
            flash(f'Escreva um estoque positivo', 'alert-danger')
            return redirect(url_for('roupas'))
        if int(min_estoque_validado) == 0:
            flash(f'O Estoque não pode ser zero', 'alert-danger')
            return redirect(url_for('roupas'))
        if int(gerenciamento.estoque.data) < 0:
            flash(f'Escreva um estoque positivo', 'alert-danger')
            return redirect(url_for('roupas'))
        if int(gerenciamento.estoque.data) == 0:
            flash(f'O Estoque não pode ser zero', 'alert-danger')
            return redirect(url_for('roupas'))
        if float(valor_validado) < 0:
            flash(f'Escreva um valor positivo', 'alert-danger')
            return redirect(url_for('roupas'))
        if float(valor_validado) == 0:
            flash(f'O Valor não pode ser zero', 'alert-danger')
            return redirect(url_for('roupas'))
        x = 0
        for char in gerenciamento.tamanho.data:
            if char == " ":
                x += 1
            if x == 1:
                flash(f'Não é Permitido Espaços no campo Tamanho', 'alert-danger')
                return redirect(url_for('roupas'))

        categoria_validado = gerenciamento.categoria.data.upper()
        tamanho_validado = gerenciamento.tamanho.data.upper()
        roupa = Roupas.query.get(r_id)

        if roupa:
            roupa.nome_roupa = nome_roupa_adc_validado
            roupa.categoria = categoria_validado
            roupa.tamanho = tamanho_validado
            roupa.estoque = gerenciamento.estoque.data
            roupa.valor = valor_validado
            roupa.min_estoque = min_estoque_validado
            roupa.descricao = gerenciamento.descricao.data

            database.session.commit()
        flash(f'{gerenciamento.nome_roupa_adc.data} editado com sucesso', 'alert-success')
        return redirect(url_for('roupas'))
    except Exception as e:
        flash(f'Ocorreu um erro ao editar a roupa: {str(e)}', 'alert-danger')
        return redirect(url_for('roupas'))
    return redirect(url_for('roupas'))
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
@app.route("/cashback", methods=['GET', 'POST'])
def cashback():
    categorias = Categoria.query.all()
    roupas = Roupas.query.all()
    if request.method == 'POST':
        return render_template("cashback.html")

    return render_template("cashback.html",categorias=categorias,roupas=roupas)

@app.route('/enviar-email', methods=['POST'])
def enviar_email():
    data = request.get_json()
    nome = data['nome']
    email = data['email']
    produtos = data['produtos']
    corpo = data['corpo']

    # Aqui você pode usar a biblioteca de envio de email de sua escolha, como o Mailgun
    # Neste exemplo, usaremos a biblioteca requests para enviar uma solicitação POST para a API do Mailgun

    MAILGUN_API_KEY = '16ce98e653cdc2be15bb22db499f3fb5-6d1c649a-5edb3d37'
    MAILGUN_DOMAIN = 'sandbox45c07b6feda14623893ad74d9bd70151.mailgun.org'

    url = f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages"
    auth = ("api", MAILGUN_API_KEY)
    data = {
        "from": "tonysonic1227@gmail.com",
        "to": email,
        "subject": "Nota fiscal da compra",
        "html": corpo
    }

    response = requests.post(url, auth=auth, data=data)
    if response.status_code == 200:
        return 'Email enviado com sucesso!'
    else:
        return 'Erro ao enviar o email: ' + response.text, 500


@app.route("/roupas",methods=['GET', 'POST'])
@login_required
def roupas():
    gerenciamento = FormGerenciamentoRoupas()
    table = Roupas.query.all()
    roupas = [{'id': r.id_roupas, 'nome_roupa': r.nome_roupa, 'categoria':r.categoria, 'tamanho': r.tamanho,'estoque': r.estoque,'valor': r.valor,'min_estoque': r.min_estoque,'descricao': r.descricao} for r in table]
    categorias = Categoria.query.all()
    categoria = [{'id': c.id_categoria,'categoria': c.nome_categoria} for c in categorias]
    if request.method == 'POST':
        if gerenciamento.submit_adc_roupa.name in request.form:
            if not gerenciamento.validate_on_submit():

                valor_validado = gerenciamento.valor.data.replace(",", ".")
                nome_roupa_adc_validado = gerenciamento.nome_roupa_adc.data.upper()
                min_estoque_validado = gerenciamento.min_estoque.data
                if int(min_estoque_validado) < 0:
                    flash(f'Escreva um estoque positivo', 'alert-danger')
                    return redirect(url_for('roupas'))
                if int(min_estoque_validado) == 0:
                    flash(f'O Estoque não pode ser zero', 'alert-danger')
                    return redirect(url_for('roupas'))
                if int(gerenciamento.estoque.data) < 0:
                    flash(f'Escreva um estoque positivo', 'alert-danger')
                    return redirect(url_for('roupas'))
                if int(gerenciamento.estoque.data) == 0:
                    flash(f'O Estoque não pode ser zero', 'alert-danger')
                    return redirect(url_for('roupas'))
                if float(valor_validado) < 0:
                    flash(f'Escreva um valor positivo', 'alert-danger')
                    return redirect(url_for('roupas'))
                if float(valor_validado) == 0:
                    flash(f'O Valor não pode ser zero', 'alert-danger')
                    return redirect(url_for('roupas'))
                x = 0
                for char in gerenciamento.tamanho.data:
                    if char == " ":
                        x += 1
                    if x == 1:
                        flash(f'Não é Permitido Espaços no campo Tamanho', 'alert-danger')
                        return redirect(url_for('roupas'))


                    categoria_validado = gerenciamento.categoria.data.upper()
                    tamanho_validado = gerenciamento.tamanho.data.upper()
                    roupa = Roupas(nome_roupa=nome_roupa_adc_validado, categoria=categoria_validado,tamanho=tamanho_validado,estoque=gerenciamento.estoque.data,valor=valor_validado,min_estoque=min_estoque_validado,descricao=gerenciamento.descricao.data)
                    database.session.add(roupa)
                    database.session.commit()
                    cliente = Cliente.query.first()  # Assuming you want to retrieve the first customer from the query
                    nome_cliente = cliente.nome_cliente
                    cashback = Cashback.query.first()
                    valor = float(valor_validado)
                    desconto = 0.15 * valor
                    valor_com_desconto = valor - desconto
                    texto_rasurado = ''.join([char + '̷' for char in f'R${valor:.2f} '])
                    if cliente.cashback > cashback.min_cashback:
                        mensagem = f'Oi, {nome_cliente}, tudo bem? 😊 Tenho uma ótima notícia par te dar. Sua cota de cashback foi atingida com sucesso e você tem R${cliente.cashback} para gastar em produtos na nossa loja, válidos até o dia {cliente.data_validade_cashback}. Aproveite e venha para a Dripstyle reinvindicar suas vantagens.'
                        message = client.messages.create(
                            from_='whatsapp:+14155238886',
                            body=mensagem,
                            to='whatsapp:+557599489435'
                        )
                        print(message.sid)
                    mensagem = f'Oi, {nome_cliente}, tudo bem? Estávamos reparando em suas últimas compras em nossa loja e percebemos que podemos ter alguns produtos que possam te atrair. Segue uma lista com as nossas novidades escolhidas especialmente para você:\n- {gerenciamento.nome_roupa_adc.data.capitalize()}: {texto_rasurado}  | R${valor_com_desconto:.2f} (com desconto de 15%)\nTe aguardamos o quanto antes em nossa loja, somos muito gratos por tê-lo(a) como nosso cliente! 😊'

                    message = client.messages.create(
                        from_='whatsapp:+14155238886',
                        body=mensagem,
                        to='whatsapp:+557599489435'
                    )
                    print(message.sid)
                    flash(f'{gerenciamento.nome_roupa_adc.data} cadastrada com sucesso', 'alert-success')
                    return redirect(url_for('roupas'))

        if gerenciamento.submit_add_categoria.name in request.form:
            if not gerenciamento.validate_on_submit():
                try:
                    if any(char.isdigit() for char in gerenciamento.nome_categoria_add.data):
                        flash(f'A categoria não pode conter numeros', 'alert-danger')
                        return redirect(url_for('roupas'))
                    x = 0
                    for char in gerenciamento.nome_categoria_add.data:
                        if char == " ":
                            x += 1
                        if x > 3:
                            flash(f'Muitos espaços em branco na Categoria', 'alert-danger')
                            return redirect(url_for('roupas'))
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
                        flash(f'Somente são aceitos números positivos', 'alert-danger')
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
                        flash(f'Não é possivel remover estoque com numeros negativos', 'alert-danger')
                        return redirect(url_for('roupas'))
                    if int(gerenciamento.qtd_estoque_del.data) == 0:
                        flash(f'Não é possivel remover "0" do estoque', 'alert-danger')
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
                    flash(f'Digite um numero válido em Estoque', 'alert-danger')
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


    return render_template('gerenciamentoRoupas.html',gerenciamento=gerenciamento,roupas=roupas,categoria=categoria)


@app.route("/cadastro", methods=['GET', 'POST'])

def cadastro():
    form_cadastro_usuario = FormCadastroUsuario()
    if request.method == 'POST':
        if not form_cadastro_usuario.validate_on_submit():
            try:
                if form_cadastro_usuario.senha.data != form_cadastro_usuario.confirmacao.data:
                    flash(f'Os campos de senhas estão diferentes', 'alert-danger')
                    return redirect(url_for('cadastro'))
                x = 0
                for char in form_cadastro_usuario.usuario.data:
                    if char == " ":
                        x += 1
                    if x > 3:
                        flash(f'Muitos espaços em branco no usuario', 'alert-danger')
                        return redirect(url_for('cadastro'))
                x = 0
                for char in form_cadastro_usuario.senha.data:
                    if char == " ":
                        x += 1
                    if x > 3:
                        flash(f'Muitos espaços em branco na senha', 'alert-danger')
                        return redirect(url_for('cadastro'))
                x = 0
                for char in form_cadastro_usuario.email.data:
                    if char == " ":
                        x += 1
                    if x > 3:
                        flash(f'Muitos espaços em branco no email', 'alert-danger')
                        return redirect(url_for('cadastro'))
                if "gmail." in form_cadastro_usuario.email.data or "hotmail." in form_cadastro_usuario.email.data or "outlook." in form_cadastro_usuario.email.data:
                    print("cavalo")
                else:
                    flash(f'Digite um domínio válido Ex: gmail,hotmail,outlook', 'alert-danger')
                    return redirect(url_for('cadastro'))

                codigo = generate_codigo()
                usuario_cadastro_validado = form_cadastro_usuario.usuario.data.upper()
                senha = form_cadastro_usuario.senha.data
                senha_criptografada = generate_password_hash(senha)
                usuario = Usuario(id=codigo, usuario=usuario_cadastro_validado, email=form_cadastro_usuario.email.data, senha=senha_criptografada)
                database.session.add(usuario)
                database.session.commit()
                flash(f'{form_cadastro_usuario.usuario.data.lower()} cadastrado com sucesso', 'alert-success')
                return redirect(url_for('login'))
            except:
                flash(f'Erro ao cadastrar usuário, usuário ou email já existentes!', 'alert-danger')
                return redirect(url_for('cadastro'))
    return render_template('cadastro.html', form_cadastro_usuario=form_cadastro_usuario)
@app.route("/RemoverUsuario", methods=['GET', 'POST'])
@login_required
def RemoverUsuario():
    table = Usuario.query.all()
    form_rem_usu = FormRemUsu()
    usuario = [{'id': u.id, 'usuario': u.usuario } for u in table]
    if form_rem_usu.submit_del_usuario.name in request.form:
        if not form_rem_usu.validate_on_submit():
            if form_rem_usu.nome_usuario_del.data.upper() == "ADMINISTRADOR":
                flash(f'Erro ao deletar Usuário', 'alert-danger')
                return redirect(url_for('RemoverUsuario'))
            usuario_deletado_validado = form_rem_usu.nome_usuario_del.data.upper()
            user = Usuario.query.filter_by(usuario=usuario_deletado_validado).all()
            try:
                if not user:
                    flash(f'Erro ao deletar Usuário', 'alert-danger')
                    return redirect(url_for('RemoverUsuario'))
                for u in user:
                    database.session.delete(u)
                    database.session.commit()
                    flash(f'{form_rem_usu.nome_usuario_del.data} apagado(a) com sucesso', 'alert-success')
                return redirect(url_for('RemoverUsuario'))
            except:
                flash(f'Erro ao deletar Usuário', 'alert-danger')
                return redirect(url_for('RemoverUsuario'))
    return render_template('removerUsuario.html', form_rem_usu=form_rem_usu, usuario=usuario)

@app.route("/vendas", methods=['GET', 'POST'])
@login_required
def vendas():
    venda_form = VendaForm()
    table = Roupas.query.all()
    roupas = [{'id': r.id_roupas, 'nome_roupa': r.nome_roupa, 'categoria': r.categoria, 'tamanho': r.tamanho,
               'estoque': r.estoque, 'valor': r.valor} for r in table]
    table2 = Promocao.query.all()
    tipo = [{'id_promo': t.id_promo, 'tipo_pagamento': t.tipo_pagamento , 'porcentagem': t.porcentagem} for t in table2]
    if request.method == 'POST':
        if venda_form.submit_venda.name in request.form:
            if not venda_form.validate_on_submit():
                try:

                    roupa_venda = venda_form.roupa_vendida.data
                    estoque = Roupas.query.filter_by(nome_roupa=roupa_venda.upper()).first()
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
                        flash(f'Não é permitido Estoque negativo', 'alert-danger')
                        return redirect(url_for('roupas'))
                    venda = Vendas(roupas_fk=venda_form.roupa_vendida.data,
                                   nome_cliente=venda_form.nome_cliente.data.capitalize(),
                                 valor_venda=venda_form.valor_total.data,vendedor=current_user.usuario)
                    database.session.add(venda)
                    database.session.commit()
                    flash(f'{roupa_venda} teve sua venda concluída com sucesso', 'alert-success')
                    return redirect(url_for('roupas'))
                except:
                    flash(f'Erro ao Vender', 'alert-danger')
                    return redirect(url_for('vendas'))




    return render_template('venda.html', venda_form=venda_form, roupas=roupas,tipo=tipo)
@app.route("/historico", methods=['GET', 'POST'])
@login_required
def historico():
    table = Vendas.query.all()
    vendas = [{'id_venda': r.id_venda, 'roupas_fk': r.roupas_fk, 'nome_cliente': r.nome_cliente,
               'valor_venda': r.valor_venda, 'vendedor': r.vendedor, 'data_da_venda': r.data_da_venda} for r in table]
    return render_template('historicoVendas.html', vendas=vendas)
