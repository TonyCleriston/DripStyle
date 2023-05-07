import unittest
from loja_de_roupa import app, database
from loja_de_roupa.models import Usuario, Roupas, Categoria

class CategoriaTest(unittest.TestCase):
    def test_adicionar_categoria(self):
        with app.app_context():
            input_do_usuario = "calÇADO"
            categoria = Categoria(nome_categoria=input_do_usuario.upper())
            database.session.add(categoria)
            database.session.commit()
            categoria_adicionada = Categoria.query.filter_by(nome_categoria="CALÇADO").first()
            self.assertTrue(categoria_adicionada.nome_categoria == "CALÇADO", "Não pode trazer outra categoria")
            # /-----------------------------------------------------------/
            Categoria.query.filter_by(nome_categoria="CALÇADO").delete()
            database.session.commit()
    def test_remover_categoria(self):
        with app.app_context():
            categoria = Categoria(nome_categoria="CALÇADO")
            database.session.add(categoria)
            database.session.commit()
            input_do_usuario = "CalçadO"
            Categoria.query.filter_by(nome_categoria=input_do_usuario.upper()).delete()
            database.session.commit()
            categoria_removida = Categoria.query.filter_by(nome_categoria="CALÇADO").all()
            self.assertFalse(len(categoria_removida) != 0, "Ao procurar pelo CALÇADO não pode trazer nenhuma lista")

if __name__ == '__main__':
    unittest.main()