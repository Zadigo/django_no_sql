import os
import unittest

from django_no_sql.db.database import Database
from django_no_sql.db.errors import DatabaseError
from django_no_sql.db.managers import Manager

PATH = 'C:\\Users\\Pende\\Documents\\myapps\\django_no_sql\\db\\database.json'

class TestInlineCreation(unittest.TestCase):
    def setUp(self):
        self.database = Database(path_or_url=PATH)
    
    def test_create_database(self):
        self.database.load_database()
        self.assertTrue(os.path.exists(PATH))

    def test_load_database(self):
        all_data = self.database.load_database()
        self.assertIsInstance(all_data, dict)

        # self.assertIsInstance(self.database.model_fields, dict)
        # self.assertIsInstance(self.database.field_names, dict)

        self.assertIn('age', self.database.model_fields)
        self.assertIn('age', self.database.field_names)

        self.assertEqual('Celebrity', self.database.model_name)

    @unittest.expectedFailure
    def test_loading_manager(self):
        # The manager can only be loaded when the .load_datbase()
        # function is called
        self.database.manager


class TestData(unittest.TestCase):
    def setUp(self):
        self.database = Database(path_or_url=PATH)
        self.database.load_database()

    # def test_database_name(self):
    #     self.assertEqual(self.database.db_data, 'database.json')
    
    def test_database_loaded_data(self):
        loaded_data = self.database.loaded_json_data
        self.assertTrue(self.database.database_loaded)
        self.assertIsInstance(loaded_data, list)
        
        first_record = loaded_data[0]
        self.assertIn('name', first_record)
        self.assertIn('surname', first_record)

        self.assertEqual(first_record['name'], 'Kendall')

    def test_manager_data_is_correctly_instanciated(self):
        # Expected: that the manager
        # contains the same data as
        # the database
        self.assertEqual(self.database.manager.functions.db_data, self.database.loaded_json_data)
        self.assertIsInstance(self.database.manager, Manager)

    def test_fields(self):
        self.assertEqual(len(self.database.field_names), 5)
        self.assertIn('name', self.database.field_names)

    @unittest.expectedFailure
    def test_field_not_exists(self):
        self.assertIn('address', self.database.model_fields)

    def test_has_required_fields(self):
        self.assertIsNotNone(self.database.required_fields)
        self.assertIn('name', self.database.required_fields)
        self.assertEqual(len(self.database.required_fields), 7)

    def test_database_not_exists(self):
        with self.assertRaises(DatabaseError):
            Database(path_or_url=__file__)

if __name__ == "__main__":
    unittest.main()
