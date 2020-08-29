import unittest

from django_no_sql.db import aggregates
from django_no_sql.db.database import Database
from django_no_sql.db.managers import Manager


class TestManager(unittest.TestCase):
    def setUp(self):
        self.db = Database(import_name=__file__)
        self.db.load_database()

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
        record = self.db.manager.get(location__state__contains='Cali')
        record_dict = record[0]
        self.assertEqual(record_dict['location']['state'], 'California')

    def test_complex_get_gt(self):
        # FIXME: should return only on record
        record = self.db.manager.get(location__state__contains='Cali')
        record_dict = record[0]
        self.assertEqual(record_dict['location']['state'], 'California')

    def test_filter(self):
        records = self.db.manager.filter(surname='Jenner')
        self.assertEqual(len(records), 2)
        
        for record in records:
            self.assertEqual(record['surname'], 'Jenner')

    def test_filter_eq(self):
        records = self.db.manager.filter(age=24)
        self.assertEqual(records[0]['age'], 24)

    def test_filter_gt(self):
        records = self.db.manager.filter(age__gt=23)
        # self.assertEqual(len(records), 1)
        self.assertGreater(records[0]['age'], 23)

    def test_filter_aggregate_sum(self):
        total = self.db.manager.all().aggregate(aggregates.Sum('age'))
        self.assertIn('age__sum', total)
        self.assertEqual(total['age__sum'], 92)
        
    def test_filter_aggregate_min(self):
        total = self.db.manager.all().aggregate(aggregates.Min('age'))
        self.assertIn('age__min', total)
        self.assertEqual(total['age__min'], 22)

    def test_filter_aggregate_max(self):
        total = self.db.manager.all().aggregate(aggregates.Max('height'))
        self.assertIn('height__max', total)
        self.assertEqual(total['height__max'], 178)

    def test_filter_last(self):
        record = self.db.manager.last()
        expected = {
            "name": "Kylie",
            "surname": "Jenner",
            "age": 22,
            "height": 168,
            "location": {
                "country": "USA",
                "state": "California",
                "city": "Los Angeles"
            }
        }
        self.assertEqual(expected, record)

    def test_filter_first(self):
        record = self.db.manager.first()
        expected = {
            "name": "Kendall",
            "surname": "Jenner",
            "age": 24,
            "height": 178,
            "location": {
                "country": "USA",
                "state": "California",
                "city": "Los Angeles"
            }
        }
        self.assertEqual(expected, record)

    def test_filter_annotate(self):
        pass

    def test_filter_values_list(self):
        pass



if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTests([TestManager])
