import unittest
from CategoriaTest01 import CategoriaTest
from RoupaTest01 import RoupaTest
from UsuarioTest01 import UsuarioTest
from PromocaoTest01 import PromocaoTest
from VendasTest01 import VendasTest

def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(CategoriaTest))
    test_suite.addTest(unittest.makeSuite(RoupaTest))
    test_suite.addTest(unittest.makeSuite(UsuarioTest))
    test_suite.addTest(unittest.makeSuite(PromocaoTest))
    test_suite.addTest(unittest.makeSuite(VendasTest))
    return test_suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())