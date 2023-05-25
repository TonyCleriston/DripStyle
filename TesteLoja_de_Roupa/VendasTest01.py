import unittest
from loja_de_roupa import app, database
from loja_de_roupa.models import Usuario, Roupas, Categoria , Promocao,Vendas

class VendasTest(unittest.TestCase):
    def test_venda(self):
        with app.app_context():
            roupa1 = Roupas(nome_roupa='SHORT DE PRAIA', categoria='SHORT', tamanho='P', estoque='30',valor='60.00')
            roupa2 = Roupas(nome_roupa='SUNGA DO KRATOS', categoria='SUNGAS', tamanho='PP', estoque='60',valor='15.00')
            venda1 = Vendas(roupas_fk='SUNGA DO KRATOS', nome_cliente='TICO', endereco='MORRO DO DENDE', valor_venda='30.00')
            venda2 = Vendas(roupas_fk='SHORT DE PRAIA', nome_cliente='TICO', endereco='MORRO DA DENDE', valor_venda='180.00')
            database.session.add(roupa1)
            database.session.add(roupa2)
            database.session.add(venda1)
            database.session.add(venda2)
            database.session.commit()
            # /-----------------------------------------------------------/
            # A quantidade de sungas foram duas (R$ 30) e de SHORTS 3 (R$ 180)
            cliente_total_compras = Vendas.query.filter_by(nome_cliente='TICO').all()
            total_vendas = 0
            for i,total in enumerate(cliente_total_compras):
                total_vendas += float(cliente_total_compras[i].valor_venda)
            self.assertEqual(total_vendas,210.00)
            roupa3 = Roupas(nome_roupa='BOINA CINZA', categoria='CHAPEU', tamanho='28', estoque='10', valor='40.00')
            venda3 = Vendas(roupas_fk='BOINA CINZA', nome_cliente='TICO', endereco='MORRO DA DENDE',valor_venda='40.00')
            database.session.add(roupa3)
            database.session.add(venda3)
            database.session.commit()
            cliente_total_compras = Vendas.query.filter_by(nome_cliente='TICO').all()
            total_vendas = 0
            for i, total in enumerate(cliente_total_compras):
                total_vendas += float(cliente_total_compras[i].valor_venda)
            self.assertEqual(total_vendas, 250.00)
            # /-----------------------------------------------------------/
            Roupas.query.filter_by(nome_roupa='SHORT DE PRAIA').delete()
            database.session.commit()
            Roupas.query.filter_by(nome_roupa='SUNGA DO KRATOS').delete()
            database.session.commit()
            Roupas.query.filter_by(nome_roupa='BOINA CINZA').delete()
            database.session.commit()
            Vendas.query.filter_by(roupas_fk='SHORT DE PRAIA').delete()
            database.session.commit()
            Vendas.query.filter_by(roupas_fk='SUNGA DO KRATOS').delete()
            database.session.commit()
            Vendas.query.filter_by(roupas_fk='BOINA CINZA').delete()
            database.session.commit()

    def test_venda(self):
        with app.app_context():
            roupa1 = Roupas(nome_roupa='CAMISA DE CHURRASCO', categoria='CAMISA', tamanho='G', estoque='30', valor='60.00')
            roupa2 = Roupas(nome_roupa='LUVA DE BOXE', categoria='ACESSORIO', tamanho='M', estoque='60', valor='15.00')
            venda1 = Vendas(roupas_fk='CAMISA DE CHURRASCO', nome_cliente='TICO', endereco='MORRO DO DENDE',valor_venda='30.00')
            venda2 = Vendas(roupas_fk='LUVA DE BOXE', nome_cliente='TICO', endereco='MORRO DA DENDE',valor_venda='180.00')
            database.session.add(roupa1)
            database.session.add(roupa2)
            database.session.add(venda1)
            database.session.add(venda2)
            database.session.commit()
            # /-----------------------------------------------------------/
            # Confirmar se as informação não estão trocadas
            cliente_total_compras = Vendas.query.filter_by(nome_cliente='TICO').all()
            self.assertFalse(cliente_total_compras[0].roupas_fk == 'LUVA DE BOXE','Não pode trazer a Luva')
            self.assertNotEqual(cliente_total_compras[1].valor_venda,30.0)
            self.assertEqual(cliente_total_compras[1].valor_venda,180.0)

            # /-----------------------------------------------------------/
            Roupas.query.filter_by(nome_roupa='LUVA DE BOXE').delete()
            database.session.commit()
            Roupas.query.filter_by(nome_roupa='CAMISA DE CHURRASCO').delete()
            database.session.commit()
            Vendas.query.filter_by(roupas_fk='LUVA DE BOXE').delete()
            database.session.commit()
            Vendas.query.filter_by(roupas_fk='CAMISA DE CHURRASCO').delete()
            database.session.commit()
if __name__ == '__main__':
    unittest.main()