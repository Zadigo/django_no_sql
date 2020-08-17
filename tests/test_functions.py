from django_no_sql.db.functions import Functions
import unittest
from django_no_sql.db import errors

TEST_DATA = [{
    'name': 'Kendall',
    'surname': 'Jenner',
    'age': 24,
    'height': 178,
    'location': {
        'country': 'USA',
        'state': 'California',
        'city': 'Los Angeles'
    }
}]

MULTIPLE_TEST_DATA = [
    {
        'name': 'Kendall',
        'surname': 'Jenner',
        'age': 24,
        'height': 178,
        'location': {
            'country': 'USA',
            'state': 'California',
            'city': 'Los Angeles'
        }
    },
    {
        'name': 'Kylie',
        'surname': 'Jenner',
        'age': 21,
        'height': 170,
        'location': {
            'country': 'USA',
            'state': 'California',
            'city': 'Los Angeles'
        }
    }
]

class TestFunctions(unittest.TestCase):
    def setUp(self):
        self.functions = Functions()
        self.functions.db_data = TEST_DATA

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

    def test_can_iterate(self):
        result = self.functions.iterator(name='Kendall')
        self.assertIsInstance(result[0], dict)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], TEST_DATA[0])
        self.assertEqual(result[0]['name'], 'Kendall')

    def test_cannot_handle_dict(self):
        self.functions.db_data = {'name': 'Kendall'}
        # To prevent the iterator from breaking we should not
        # be able to pass a dict but a list of dicts
        with self.assertRaises(errors.QueryTypeError):
            self.functions.iterator(name='Kendall')

    def test_cannot_handle_empty_dict(self):
        # When using empty dicts, for whatever
        # reason this passes as opposed to the
        # definition above which raises a QueryTypeError
        self.functions.db_data = {}
        with self.assertRaises(errors.QueryTypeError):
            pass

    def test_right_hand(self):
        result = self.functions.right_hand_filter('name__exact', {'name': 'Kendall'})
        self.assertIsInstance(result, tuple)
        self.assertIn('Kendall', result)
        self.assertIn('exact', result)
        self.assertEqual(len(result), 2)

        result = self.functions.right_hand_filter('name', {'name': 'Kendall'})
        self.assertIsInstance(result, tuple)
        # ..When there's no special filter,
        # the second part of the tuple is none.
        # We can fix that? 
        self.assertIsNone(result[1])
        self.assertIn('Kendall', result)
        self.assertEqual(len(result), 2)

    @unittest.expectedFailure
    def test_bad_right_hand(self):
        self.functions.right_hand_filter('name__surname', {'name': 'Kendall'})

    def test_last_id(self):
        last_id = self.functions.last_id()
        self.assertIsInstance(last_id, int)
        self.assertEqual(last_id, 1)

    def test_has_no_new_queryset(self):
        self.assertFalse(self.functions.has_new_queryset)

    def test_reset_already_empty_queryset(self):
        self.assertFalse(self.functions.reset_new_queryset())

    def test_query_accuracy(self):
        expected = MULTIPLE_TEST_DATA[1]
        self.assertEqual(self.functions.iterator(query=MULTIPLE_TEST_DATA, name='Kylie'), expected)
    
    def test_query_visually(self):
        print(self.functions.iterator(query=MULTIPLE_TEST_DATA, name='Kylie'))

if __name__ == "__main__":
    unittest.main()
