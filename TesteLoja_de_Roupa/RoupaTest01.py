import unittest
from loja_de_roupa import app, database
from loja_de_roupa.models import Usuario, Roupas, Categoria

class RoupaTest(unittest.TestCase):
    def test_adicionar_roupa(self):
        with app.app_context():
            # /-----------------------------------------------------------/
            gerenciamento = Roupas(nome_roupa='CAMISETA VERDE',  categoria='CAMISETA', tamanho='M', estoque='10', valor='30.00')

            database.session.add(gerenciamento)
            database.session.commit()

            roupa_adicionada = Roupas.query.filter_by(nome_roupa='CAMISETA VERDE').all()

            roupa = roupa_adicionada[0].__dict__
            esperado = {'nome_roupa': 'CAMISETA VERDE', 'valor': 30.00, 'categoria': 'CAMISETA', 'tamanho': 'M','estoque': 10}
            for chave, valor in esperado.items():
                self.assertEqual(roupa[chave], valor)

            # self.assertEqual(roupa_adicionada[0].nome_roupa, 'CAMISETA VERDE')
            # self.assertEqual(roupa_adicionada[0].valor, 30.00)
            # self.assertEqual(roupa_adicionada[0].categoria, 'CAMISETA')
            # self.assertEqual(roupa_adicionada[0].tamanho, 'M')
            # self.assertEqual(roupa_adicionada[0].estoque, 10)
            # /-----------------------------------------------------------/
            Roupas.query.filter_by(nome_roupa="CAMISETA VERDE").delete()
            database.session.commit()
    def test_remover_roupa(self):
        with app.app_context():
            gerenciamento = Roupas(nome_roupa='SHORT DE PRAIA',  categoria='SHORT', tamanho='P', estoque='30', valor='45.00')
            database.session.add(gerenciamento)
            database.session.commit()
            # /-----------------------------------------------------------/
            Roupas.query.filter_by(nome_roupa='SHORT DE PRAIA').delete()
            database.session.commit()
            roupa_removida = Roupas.query.filter_by(nome_roupa='SHORT DE PRAIA').all()
            self.assertEqual(len(roupa_removida),0)
    def test_adicionar_estoque(self):
        with app.app_context():
            gerenciamento = Roupas(nome_roupa='SHORT DE PRAIA',  categoria='SHORT', tamanho='P', estoque='30', valor='45.00')
            database.session.add(gerenciamento)
            database.session.commit()
            # /-----------------------------------------------------------/
            roupa_estoque = Roupas.query.filter_by(nome_roupa='SHORT DE PRAIA').all()
            roupa_estoque[0].estoque += 5
            self.assertEqual(roupa_estoque[0].estoque, 35)
            # /-----------------------------------------------------------/
            Roupas.query.filter_by(nome_roupa='SHORT DE PRAIA').delete()
            database.session.commit()
    def test_diminuir_estoque01(self):
        with app.app_context():
            gerenciamento = Roupas(nome_roupa='SHORT DE PRAIA', categoria='SHORT', tamanho='P', estoque='30',valor='45.00')
            database.session.add(gerenciamento)
            database.session.commit()
            # /-----------------------------------------------------------/
            roupa_estoque = Roupas.query.filter_by(nome_roupa='SHORT DE PRAIA').first()
            roupa_estoque.estoque -= 5
            self.assertEqual(roupa_estoque.estoque, 25)
            # /-----------------------------------------------------------/
            Roupas.query.filter_by(nome_roupa='SHORT DE PRAIA').delete()
            database.session.commit()
    def test_diminuir_estoque02(self):
        with app.app_context():

            gerenciamento = Roupas(nome_roupa='SHORT DE PRAIA',  categoria='SHORT', tamanho='P', estoque='30', valor='45.00')
            database.session.add(gerenciamento)
            database.session.commit()
            roupa_estoque = Roupas.query.filter_by(nome_roupa='SHORT DE PRAIA').first()
            # /-----------------------------------------------------------/
            input_do_usuario = 35
            if roupa_estoque.estoque - input_do_usuario > 0:
                roupa_estoque.estoque -= input_do_usuario
            else:
                roupa_estoque.estoque = 0
            self.assertNotEqual(roupa_estoque.estoque, -5)
            self.assertEqual(roupa_estoque.estoque, 0)
            # /-----------------------------------------------------------/
            Roupas.query.filter_by(nome_roupa='SHORT DE PRAIA').delete()
            database.session.commit()





if __name__ == '__main__':
    unittest.main()