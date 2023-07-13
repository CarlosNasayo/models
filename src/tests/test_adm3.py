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
from ormWP.models.adm3 import Adm3

# Conectarse a la base de datos de prueba


class TestAdm3(unittest.TestCase):

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
        self.adm2.save()

        # Crea un objeto Adm3 de prueba con referencia a Adm2
        self.adm3 = Adm3(
            name='subsubzona prueba',
            ext_id='789',
            traced=['created_time', 'updated', 'active'],
            adm2=self.adm2,
            aclimate_id='64ad5835515640e690d80dba'
        )

    def tearDown(self):
        # Limpia la base de datos eliminando los objetos creados durante las pruebas
        self.adm1.delete()
        self.adm2.delete()
        self.adm3.delete()

    def test_create_adm3(self):
        # Guarda el objeto Adm3
        self.adm3.save()
        self.assertIsNotNone(self.adm3.id)

        # Verifica que el Adm3 haya sido creado exitosamente
        adm3 = Adm3.objects(id=self.adm3.id).first()
        self.assertEqual(adm3.name, 'subsubzona prueba')
        self.assertEqual(adm3.ext_id, '789')
        self.assertEqual(adm3.adm2, self.adm2)

if __name__ == '__main__':
    unittest.main()
