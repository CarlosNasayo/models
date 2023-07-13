import unittest
from mongoengine import connect, disconnect
import sys
import os

# Asegúrate de tener las rutas correctas para importar los módulos
dir_path = os.path.dirname(os.path.realpath(__file__))
orm_dir_path = os.path.abspath(os.path.join(dir_path, '..'))
sys.path.append(orm_dir_path)

from ormWP.models.watershed import Watershed
from ormWP.models.adm1 import Adm1
from ormWP.models.adm2 import Adm2
from ormWP.models.adm3 import Adm3

# Conectarse a la base de datos de prueba

class TestWatershed(unittest.TestCase):

    def setUp(self):
        disconnect()  # Desconectarse de cualquier conexión existente
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

        self.adm3 = Adm3(
            name='subsubzona prueba',
            ext_id='789',
            traced=['created_time', 'updated', 'active'],
            adm2=self.adm2,
            aclimate_id='64ad5835515640e690d80dba'
        )
        self.adm3.save()

        # Crea un objeto Watershed de prueba con referencia a Adm2
        self.watershed = Watershed(
            area=100.0,
            name='watershed prueba',
            traced=['created_time', 'updated', 'active'],
            adm3=self.adm3
        )

    def tearDown(self):
        # Limpia la base de datos eliminando los objetos creados durante las pruebas
        self.watershed.delete()
        self.adm2.delete()
        self.adm1.delete()

    def test_create_watershed(self):
        # Guarda el objeto Watershed
        self.watershed.save()
        self.assertIsNotNone(self.watershed.id)

        # Verifica que el Watershed haya sido creado exitosamente
        watershed = Watershed.objects(id=self.watershed.id).first()
        self.assertEqual(watershed.area, 100.0)
        self.assertEqual(watershed.name, 'watershed prueba')
        self.assertEqual(watershed.traced, ['created_time', 'updated', 'active'])
        self.assertEqual(watershed.adm3, self.adm3)

if __name__ == '__main__':
    unittest.main()
