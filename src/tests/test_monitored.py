import unittest
from unittest.mock import MagicMock
from mongoengine import connect, disconnect
import sys
import os

# Asegúrate de tener las rutas correctas para importar los módulos
dir_path = os.path.dirname(os.path.realpath(__file__))
orm_dir_path = os.path.abspath(os.path.join(dir_path, '..'))
sys.path.append(orm_dir_path)

from ormWP.models.monitored import Monitored
from ormWP.models.waterpoint import Waterpoint
from ormWP.models.watershed import Watershed
from ormWP.models.adm1 import Adm1 
from ormWP.models.adm2 import Adm2 
from ormWP.models.adm3 import Adm3 

# Conectarse a la base de datos de prueba


class TestMonitored(unittest.TestCase):

    def setUp(self):
 # Desconectarse de cualquier conexión existente
        connect('test_water_points', host='mongomock://localhost')

        # Mock el objeto Waterpoint
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
        self.watershed.save()
        # Crea un objeto Waterpoint de prueba con referencia a Watershed
        self.waterpoint = Waterpoint(
            lat=1.2345,
            lon=2.3456,
            name='waterpoint prueba',
            area=100.0,
            climatology=['climate1', 'climate2'],
            other_attributes=['attr1', 'attr2'],
            watershed=self.watershed
        )
        self.waterpoint.save()
        # Crea un objeto DataEntry de prueba con referencia al objeto Waterpoint mockeado
        self.monitored = Monitored(
            date='2022-01-01 12:00:00',
            values = [{'mediandeep': 12.3}, {'waterlevel': 12.3}],
            waterpoint=self.waterpoint
        )

    def tearDown(self):
        # Limpia la base de datos eliminando los objetos creados durante las pruebas
        self.monitored.delete()

    def test_create_data_entry(self):
        # Guarda el objeto DataEntry
        self.monitored.save()
        self.assertIsNotNone(self.monitored.id)

        # Verifica que el DataEntry haya sido creado exitosamente
        monitored = Monitored.objects(id=self.monitored.id).first()
        self.assertEqual(monitored['values'], [{'mediandeep': 12.3}, {'waterlevel': 12.3}])
        self.assertEqual(monitored.waterpoint, self.waterpoint)

if __name__ == '__main__':
    unittest.main()
