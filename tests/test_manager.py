from django_no_sql.db.managers import Manager
from django_no_sql.db.database import Database
import unittest

PATH = 'C:\\Users\\Pende\\Documents\\myapps\\django_no_sql\\db\\database.json'

class TestManager(unittest.TestCase):
    def setUp(self):
        self.db = Database(path_or_url=PATH)

    def test_get(self):
        record = self.db.manager.get(name='Kendall')
        self.assertIsInstance(record, list)
        # Expected: one record where the name
        # is equals to Kendall
        record_dict = record[0]
        self.assertEqual(record_dict['name'], 'Kendall')

    def test_complex_get(self):
        record = self.db.manager.get(location__state='Arizona')
        self.assertIsInstance(record, list)
        # Expected: one record where the state
        # within location is equals to Arizona
        record_dict = record[0]
        self.assertEqual(record_dict['location']['state'], 'Arizona')

    def test_complex_get_exact(self):
        record = self.db.manager.get(location__state__exact='Arizona')
        record_dict = record[0]
        self.assertEqual(record_dict['location']['state'], 'Arizona')

    def test_complex_get_contains(self):
        # FIXME: should return only on record
        record = self.db.manager.get(location__state__contains='Cali')
        record_dict = record[0]
        self.assertEqual(record_dict['location']['state'], 'California')

    def test_complex_get_gt(self):
        # FIXME: should return only on record
        record = self.db.manager.get(location__state__contains='Cali')
        record_dict = record[0]
        self.assertEqual(record_dict['location']['state'], 'California')

    def test_filter(self):
        records = self.db.manager._filter(surname='Jenner')
        # FIXME: cannot call len() on QuerySet
        self.assertEqual(len(records), 2)
        
        for record in records:
            self.assertEqual(record['surname'], 'Jenner')

    def test_filter_eq(self):
        records = self.db.manager._filter(age=24)
        # self.assertEqual(len(records), 1)
        self.assertEqual(records[0]['age'], 24)

    def test_filter_gt(self):
        records = self.db.manager._filter(age__gt=23)
        # self.assertEqual(len(records), 1)
        self.assertGreater(records[0]['age'], 23)

# class TestFilters():
#     pass

if __name__ == "__main__":
    # unittest.main()

    suite = unittest.TestSuite()
    suite.addTests([TestManager])
    