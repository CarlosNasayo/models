import unittest
from mongoengine import connect, disconnect
import sys
import os

# Asegúrate de tener las rutas correctas para importar los módulos
dir_path = os.path.dirname(os.path.realpath(__file__))
orm_dir_path = os.path.abspath(os.path.join(dir_path, '..'))
sys.path.append(orm_dir_path)

from ormWP.models.adm1 import Adm1
from ormWP.models.adm2 import Adm2

# Conectarse a la base de datos de prueba


class TestAdm2(unittest.TestCase):

    def setUp(self):
          
        connect('test_water_points', host='mongomock://localhost')
        
        # Crea un objeto Adm1 de prueba
        self.adm1 = Adm1(
            name='zona prueba',
            ext_id='1132',
            traced=['created_time', 'updated', 'active']
        )
        self.adm1.save()

        # Crea un objeto Adm2 de prueba con referencia a Adm1
        self.adm2 = Adm2(
            name='subzona prueba',
            ext_id='456',
            traced=['created_time', 'updated', 'active'],
            adm1=self.adm1
        )

    def tearDown(self):
        # Limpia la base de datos eliminando los objetos creados durante las pruebas
        self.adm1.delete()
        self.adm2.delete()

    def test_create_adm2(self):
        # Guarda el objeto Adm2
        self.adm2.save()
        self.assertIsNotNone(self.adm2.id)

        # Verifica que el Adm2 haya sido creado exitosamente
        adm2 = Adm2.objects(id=self.adm2.id).first()
        self.assertEqual(adm2.name, 'subzona prueba')
        self.assertEqual(adm2.ext_id, '456')
        self.assertEqual(adm2.adm1, self.adm1)

if __name__ == '__main__':
    unittest.main()
