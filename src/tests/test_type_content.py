import unittest
from mongoengine import connect, disconnect
import sys
import os

# Asegúrate de tener las rutas correctas para importar los módulos
dir_path = os.path.dirname(os.path.realpath(__file__))
orm_dir_path = os.path.abspath(os.path.join(dir_path, '..'))
sys.path.append(orm_dir_path)

from ormWP.models.type_content import Typecontent

# Conectarse a la base de datos de prueba

class TestTypeContent(unittest.TestCase):

    def setUp(self):
        disconnect()  # Desconectarse de cualquier conexión existente
        connect('test_gap_analysis', host='mongomock://localhost')

        # Crea un objeto TypeContent de prueba
        self.typecontent = Typecontent(
            name='Livehood'
        )

    def tearDown(self):
        # Limpia la base de datos eliminando los objetos creados durante las pruebas
        self.typecontent.delete()

    def test_name_required(self):
        # Intenta guardar el objeto TypeContent sin el campo name
        self.typecontent.name = None
        with self.assertRaises(Exception):
            self.typecontent.save()

    def test_name_max_length(self):
        # Intenta guardar el objeto TypeContent con un valor de name que excede la longitud máxima permitida
        self.typecontent.name = 'a' * 101
        with self.assertRaises(Exception):
            self.typecontent.save()

    def test_create_typecontent(self):
        # Guarda el objeto TypeContent
        self.typecontent.save()
        self.assertIsNotNone(self.typecontent.id)

        # Verifica que el TypeContent haya sido creado exitosamente
        typecontent = Typecontent.objects(id=self.typecontent.id).first()
        self.assertEqual(typecontent.name, 'Livehood')

if __name__ == '__main__':
    unittest.main()
