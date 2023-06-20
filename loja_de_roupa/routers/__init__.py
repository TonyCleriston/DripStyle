from flask import render_template, url_for, redirect, flash, request, jsonify
from loja_de_roupa.forms import FormLogin, FormCadastroUsuario, FormGerenciamentoRoupas , VendaForm,FormRemUsu
from loja_de_roupa import app, database
from loja_de_roupa.models import Usuario, Roupas, Categoria, Promocao, Vendas, Cliente, Cashback, Itens_Venda
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from flask_login import login_required , login_user , logout_user, current_user
import requests
import pywhatkit
from twilio.rest import Client
account_sid = 'AC4bf9cd5aca8f16160b0ee9c8a10a6be6'
auth_token = '8c0cad44b7fd609dead11fc7297b49f7'
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

    MAILGUN_API_KEY = '2d6a1a2162d2c8d2b604709f41c59205-af778b4b-e619083c'
    MAILGUN_DOMAIN = 'sandbox532ae69924e6413c9848da9d5ec8c7c5.mailgun.org'

    url = f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages"
    auth = ("api", MAILGUN_API_KEY)
    data = {
        "from": "tony.junior@ba.senai.estudante.br",
        "to": email,
        "subject": "Nota fiscal da compra",
        "html": corpo
    }

    response = requests.post(url, auth=auth, data=data)
    if response.status_code == 200:
        print("Email enviado com sucesso!")
        return 'Email enviado com sucesso!'
    else:
        print('Erro ao enviar o email:', response.text)
        return 'Erro ao enviar o email', response.status_code

@app.route("/relatorios",methods=['GET', 'POST'])
@login_required
def relatorios():

    return render_template('relatorios.html')

@app.route("/clientes",methods=['GET', 'POST'])
@login_required
def clientes():

    return render_template('clientes.html')


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
                clientes = Cliente.query.all()
                print(request.form)
                if request.form.get("enviar_novidades") == "y":
                    for cliente in clientes:
                        mensagem = f'Oi, {cliente.nome_cliente}, tudo bem? Estávamos reparando em suas últimas compras em nossa loja e percebemos que podemos ter alguns produtos que possam te atrair. Segue uma lista com as nossas novidades escolhidas especialmente para você:\n- {gerenciamento.nome_roupa_adc.data.capitalize()}: R${gerenciamento.valor.data}  | \nTe aguardamos o quanto antes em nossa loja, somos muito gratos por tê-lo(a) como nosso cliente! 😊'
                        pywhatkit.sendwhats_image("+557591957920","C:\\Users\\tonys\\Downloads\\10cc61364c647819c56283fb377dba4f.jpg", mensagem)


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
@login_required
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
@app.route("/atualizar_estoque", methods=['GET', 'POST'])
def atualizar_estoque():
    data = request.get_json()

    vendas = data['venda']
    print(current_user.usuario)

    # Criar a venda no banco de dados
    venda_db = Vendas(nome_cliente=data['nome_cliente'],
                      # Supondo que você deseja pegar o nome do cliente da primeira venda
                      total_da_venda=0.0,
                      tipo_pagamento_fk=data['tipo_pagamento'],
                      # Supondo que o tipo de pagamento é o mesmo para todas as vendas
                      vendedor=current_user.usuario)
    print(venda_db)
    database.session.add(venda_db)
    database.session.commit()

    for venda in vendas:

        nome = venda['nome']
        quantidade = venda['quantidade']

        # Atualizar o estoque no banco de dados
        roupa_est = Roupas.query.filter_by(nome_roupa=nome).first()
        if roupa_est is None:
            return jsonify({'success': False, 'message': 'Roupa não encontrada'})
        if roupa_est.estoque < quantidade:
            return jsonify({'success': False, 'message': 'Quantidade maior que o estoque'})

        roupa_est.estoque -= quantidade
        print(venda)

        # Calcular o total da venda
        subtotal = venda['quantidade'] * venda['valorUnitario']
        venda_db.total_da_venda += subtotal
        print(venda_db.total_da_venda)
        print(subtotal)
        print(venda_db.id_venda)
        print(venda['nome'])
        print(venda['valorUnitario'])
        print(venda['quantidade'])

        # Criar os itens de venda relacionados à venda
        item_venda = Itens_Venda(codigo_venda=venda_db.id_venda,
                                 roupas_fk=venda['nome'],
                                 valor_unitario=venda['valorUnitario'],
                                 subtotal=subtotal,
                                 qtd=venda['quantidade'])

        database.session.add(item_venda)
        database.session.commit()




    return jsonify({'success': True, 'message': 'Venda(s) criada(s) com sucesso'})


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
        cpf = venda_form.cpf.data
        cliente_existente = Cliente.query.filter_by(cpf=cpf).first()
        if not cliente_existente:
            cliente = Cliente(nome_cliente=venda_form.nome_cliente.data, cpf=venda_form.cpf.data, cashback='55', telefone=venda_form.telefone_cliente.data,data_validade_cashback='07/09/2023')
            database.session.add(cliente)
            database.session.commit()
        # Verifica se o campo cashback-checkbox está marcado
        print(request.form)
        if not request.form.get("cashback_checkbox") == "y":
            clientes = Cliente.query.all()
            cashback = Cashback.query.first()
            for cliente in clientes:
                if float(cliente.cashback) > float(cashback.min_cashback):
                    mensagem = f'Olá, {cliente.nome_cliente}, tudo bem? Tenho uma ótima notícia para te dar. Sua cota de cashback foi atingida com sucesso e você tem R${cliente.cashback} para gastar em produtos na nossa loja, válidos até o dia {cliente.data_validade_cashback}. Aproveite e venha para a Dripstyle reivindicar suas vantagens.'
                    pywhatkit.sendwhatmsg_instantly(venda_form.telefone_cliente.data, mensagem)  # Substitua o número de telefone pelo número correto
        flash('Sua foi venda concluída com sucesso', 'alert-success')
        return redirect(url_for('vendas'))





    return render_template('venda.html', venda_form=venda_form, roupas=roupas,tipo=tipo)
@app.route("/historico", methods=['GET', 'POST'])
@login_required
def historico():
    vendas = Vendas.query.all()
    itens_venda = Itens_Venda.query.all()

    vendas_data = [{'id_venda': venda.id_venda,
                    'nome_cliente': venda.nome_cliente,
                    'total_da_venda': venda.total_da_venda,
                    'tipo_pagamento_fk': venda.tipo_pagamento_fk,
                    'vendedor': venda.vendedor,
                    'data_da_venda': venda.data_da_venda} for venda in vendas]

    itens_venda_data = [{'id_itens_venda': item.id_itens_venda,
                         'codigo_venda': item.codigo_venda,
                         'roupas_fk': item.roupas_fk,
                         'valor_unitario': item.valor_unitario,
                         'subtotal': item.subtotal,
                         'qtd': item.qtd} for item in itens_venda]
    return render_template('historicoVendas.html', vendas=vendas_data,itens_venda=itens_venda_data)
