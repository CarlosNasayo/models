import unittest
from mongoengine import connect, disconnect
import sys
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
orm_dir_path = os.path.abspath(os.path.join(dir_path, '..'))
sys.path.append(orm_dir_path)
from ormWP.models.adm1 import Adm1

# Conectarse a la base de datos de prueba


class Testadm1(unittest.TestCase):

    def setUp(self):
        connect('test_water_points', host='mongomock://localhost')
        self.adm1 = Adm1(
            name='zona prueba',
            ext_id='1132',
            traced=['created_time', 'updated', 'active']
        )

    def test_create_adm1(self):
        # Crea un nuevo adm1
        self.adm1.save()
        self.assertIsNotNone(self.adm1.id)

        print(self.adm1)

        # Verifica que el adm1 haya sido creado exitosamente
        adm1 = Adm1.objects(id=self.adm1.id).first()
        self.assertEqual(adm1.name, 'zona prueba')
        self.assertEqual(adm1.ext_id, '1132')

if __name__ == '__main__':
    unittest.main()
