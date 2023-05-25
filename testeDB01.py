from loja_de_roupa import app, database
from loja_de_roupa.models import Usuario, Promocao
from werkzeug.security import generate_password_hash

with app.app_context():
    database.create_all()

with app.app_context():
  porcentagem1 = Promocao(porcentagem='0.1', tipo_pagamento='Dinheiro')
  porcentagem2 = Promocao(porcentagem='0.05', tipo_pagamento='Débito')
  database.session.add(porcentagem1)
  database.session.commit()
  database.session.add(porcentagem2)
  database.session.commit()

