import unittest
from django_no_sql.db.database import Database

PATH = 'C:\\Users\\Pende\\Documents\\myapps\\django_no_sql\\db\\database.json'

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.database = Database(path_or_url=PATH)

    def test_database_name(self):
        self.assertEqual(self.database.db_name, 'database')
    
    def test_database_data(self):
        # Expected: dictionnary of values
        self.assertIsInstance(self.database.db_data, dict)
        
        first_value = self.database.db_data['1']
        self.assertIn('name', first_value)
        self.assertIn('surname', first_value)

    def test_manager_istanciated(self):
        # Expected: that the manager
        # contains the same data as
        # the database
        self.assertEqual(self.database.manager.db_data, self.database.db_data)

if __name__ == "__main__":
    unittest.main()