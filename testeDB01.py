from loja_de_roupa import app, database
from loja_de_roupa.models import Usuario
from werkzeug.security import generate_password_hash

with app.app_context():
    database.create_all()

#with app.app_context():
#   senha_criptografada = generate_password_hash('adminadmin')
#   usuario = Usuario(usuario='administrador', email='admin@gmail.com', senha=senha_criptografada)
#   database.session.add(usuario)
 #  database.session.commit()

