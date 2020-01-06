from django_no_sql.db.functions import Functions
import unittest

TESTDATA = {
    'name': 'Kendall',
    'surname': 'Jenner',
    'age': 24,
    'height': 178,
    'location': {
        'country': 'USA',
        'state': 'California',
        'city': 'Los Angeles'
    },
    'related': []
}

class TestFunctions(unittest.TestCase):
    def setUp(self):
        self.functions = Functions()
        self.functions.db_data = TESTDATA

    def test_available_keys(self):
        self.assertIsInstance(self.functions.available_keys(), list)
        self.assertIn('name', self.functions.available_keys())

        self.assertIs(True, self.functions.available_keys(check_key='name'))

    def test_simple_decompose(self):
        expressions = self.functions.simple_decompose('location__address')
        self.assertIsInstance(expressions, list)
        self.assertEqual(len(expressions), 2)
        self.assertIn('location', expressions)

        expressions = self.functions.simple_decompose('age')
        self.assertIsInstance(expressions, list)
        self.assertEqual(len(expressions), 1)
        self.assertIn('age', expressions)



    

if __name__ == "__main__":
    unittest.main()