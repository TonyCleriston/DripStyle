from loja_de_roupa import app, database
from loja_de_roupa.models import Usuario, Promocao , Cliente , Cashback
from werkzeug.security import generate_password_hash

with app.app_context():
    database.create_all()

with app.app_context():
  porcentagem1 = Promocao(porcentagem='0.1', tipo_pagamento='Dinheiro')
  porcentagem2 = Promocao(porcentagem='0.05', tipo_pagamento='Débito')
  cliente1 = Cliente(nome_cliente = 'Tiago Lima', cpf = '123456789',cashback = '50',data_validade_cashback = '05/03/2020')
  cashback1 = Cashback(min_cashback='50', validade_adicionada='90')
  database.session.add(porcentagem1)
  database.session.commit()
  database.session.add(cashback1)
  database.session.commit()
  database.session.add(cliente1)
  database.session.commit()
  database.session.add(porcentagem2)
  database.session.commit()

