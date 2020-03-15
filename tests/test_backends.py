from django_no_sql.db import backends
import unittest
from django_no_sql.db.errors import DatabaseError

class TestBackends(unittest.TestCase):
    def test_can_read_file(self):
        f = backends.file_reader('C:\\Users\\Pende\\Documents\\myapps\\django_no_sql\\db\\database.json')
        self.assertIsInstance(f, dict)

    def test_database_exists(self):
        with self.assertRaises(DatabaseError):
            backends.file_reader('C:\\Users\\Pende\\Documents\\myapps\\django_no_sql\\db\\databases.json')
        

if __name__ == "__main__":
    unittest.main()