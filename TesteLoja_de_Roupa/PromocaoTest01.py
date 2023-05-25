import unittest
from loja_de_roupa import app, database
from loja_de_roupa.models import Usuario, Roupas, Categoria , Promocao

class PromocaoTest(unittest.TestCase):
    def test_calculo_dinheiro(self):
        with app.app_context():
            gerenciamento = Roupas(nome_roupa='SHORT DE PRAIA', categoria='SHORT', tamanho='P', estoque='30',valor='50.00')
            database.session.add(gerenciamento)
            database.session.commit()
            # /-----------------------------------------------------------/
            # O pagamento em dinheiro desconta 10% (0.1)
            roupa_sem_promocao = Roupas.query.filter_by(nome_roupa='SHORT DE PRAIA').first()
            promocao = Promocao.query.filter_by(tipo_pagamento='Dinheiro').first()
            valorTotalCalculado = (float(roupa_sem_promocao.valor) * 1) * (1 - float(promocao.porcentagem));
            self.assertTrue(valorTotalCalculado == 45, "Confirma se a conta está correta")
            roupa_sem_promocao.valor = 50.50
            valorTotalCalculado = (float(roupa_sem_promocao.valor) * 1) * (1 - float(promocao.porcentagem));
            self.assertEqual(valorTotalCalculado,45.45)
            # /-----------------------------------------------------------/
            Roupas.query.filter_by(nome_roupa='SHORT DE PRAIA').delete()
            database.session.commit()
    def test_calculo_debito(self):
        with app.app_context():
            gerenciamento = Roupas(nome_roupa='SHORT DE PRAIA', categoria='SHORT', tamanho='P', estoque='30',valor='50.00')
            database.session.add(gerenciamento)
            database.session.commit()
            # /-----------------------------------------------------------/
            # O pagamento em debito desconta 5% (0.05)
            roupa_sem_promocao = Roupas.query.filter_by(nome_roupa='SHORT DE PRAIA').first()
            promocao = Promocao.query.filter_by(tipo_pagamento='Débito').first()
            valorTotalCalculado = (float(roupa_sem_promocao.valor) * 1) * (1 - float(promocao.porcentagem));
            self.assertTrue(valorTotalCalculado == 47.50, "Confirma se a conta está correta")
            roupa_sem_promocao.valor = 50.50
            valorTotalCalculado = (float(roupa_sem_promocao.valor) * 1) * (1 - float(promocao.porcentagem));
            # Essa conta dá 47.9749
            num_arredondado = round(valorTotalCalculado, 2)
            self.assertEqual(num_arredondado, 47.97)
            # /-----------------------------------------------------------/
            Roupas.query.filter_by(nome_roupa='SHORT DE PRAIA').delete()
            database.session.commit()
if __name__ == '__main__':
    unittest.main()