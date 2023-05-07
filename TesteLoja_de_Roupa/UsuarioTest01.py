import unittest
from loja_de_roupa import app, database
from loja_de_roupa.models import Usuario, Roupas, Categoria
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

class UsuarioTest(unittest.TestCase):
    def test_cadastrar_usuario(self):
        with app.app_context():
            # /-----------------------------------------------------------/
            senha = "saulGood"
            senha_criptografada = generate_password_hash(senha)
            usuario = Usuario(usuario="Tony Cleriston", email="tony@gmail.com",senha=senha_criptografada)
            database.session.add(usuario)
            database.session.commit()
            usuario_adicionado = Usuario.query.filter_by(usuario='Tony Cleriston').first()
            self.assertNotEqual(senha_criptografada, senha)
            self.assertEqual(usuario_adicionado.email, 'tony@gmail.com')
            # /-----------------------------------------------------------/
            database.session.delete(usuario)
            database.session.commit()

    def test_login_usuario(self):
        with app.app_context():
            # /-----------------------------------------------------------/
            senha = "saulGood"
            senha_criptografada = generate_password_hash(senha)
            usuario = Usuario(usuario="Tony Cleriston", email="tony@gmail.com", senha=senha_criptografada)
            database.session.add(usuario)
            database.session.commit()
            usuario_adicionado = Usuario.query.filter_by(usuario='Tony Cleriston').first()
            self.assertTrue(check_password_hash(usuario_adicionado.senha, "saulGood"))
            self.assertFalse(check_password_hash(usuario_adicionado.senha, "saulgood"))
            # /-----------------------------------------------------------/
            Usuario.query.filter_by(usuario='Tony Cleriston').delete()
            database.session.commit()

if __name__ == '__main__':
    unittest.main()