import unittest

from django_no_sql.db.database import Database
from django_no_sql.db.errors import DatabaseError

PATH = 'C:\\Users\\Pende\\Documents\\myapps\\django_no_sql\\db\\database.json'

class TestInlineCreation(unittest.TestCase):
    def setUp(self):
        self.database = Database(path_or_url=PATH)
        
    def test_create_database(self):
        was_created = self.database.create('Celebrity', [])
        self.assertFalse(was_created)
        # self.assertTrue(was_created)

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
        self.assertIsInstance(self.database.manager, Database)

# class TestDatabase(unittest.TestCase):
#     def setUp(self):
#         self.database = Database(path_or_url=PATH)

#     def test_database_name(self):
#         self.assertEqual(self.database.db_data, 'database.json')
    
#     def test_database_data(self):
#         # Expected: dictionnary of values
#         self.assertIsInstance(self.database.db_data, dict)
        
#         first_value = self.database.db_data['1']
#         self.assertIn('name', first_value)
#         self.assertIn('surname', first_value)

#     def test_manager_istanciated(self):
#         # Expected: that the manager
#         # contains the same data as
#         # the database
#         self.assertEqual(self.database.manager.db_data, self.database.db_data)

#     def test_fields(self):
#         self.assertIn('name', self.database.field_names)

#     @unittest.expectedFailure
#     def test_field_not_exists(self):
#         self.assertIn('surname', self.database.field_names)

#     def test_database_not_exists(self):
#         with self.assertRaises(DatabaseError):
#             Database(path_or_url='C:\\Users\\Pende\\Documents\\myapps\\django_no_sql\\db\\test.json')

if __name__ == "__main__":
    unittest.main()
