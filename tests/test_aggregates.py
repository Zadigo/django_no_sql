import unittest

from django_no_sql.db.aggregates import (Avg, Max, Min, Spread, STDeviation,
                                         Sum, Variance, Count)


class TestAggregates(unittest.TestCase):
    def test_sum(self):
        self.assertEqual(Sum('age').result['age__sum'], 59)

    def test_is_dict(self):
        result = Sum('age').result
        self.assertIsInstance(result, dict)

        self.assertIn('age__sum', result)
        self.assertIsInstance(result['age__sum'], (float, int))

    def test_count(self):
        self.assertEqual(Count('age').result['age__count'], 3)

    def test_average(self):
        self.assertEqual(Avg('age').result['age__avg'], 19.666666666666668)

    def test_max(self):
        self.assertEqual(Max('age').result['age__max'], 22)

    def test_min(self):
        self.assertEqual(Min('age').result['age__min'], 15)

    def test_st_dev(self):
        self.assertEqual(STDeviation('age').result['age__stdev'], 0)

    def test_variance(self):
        self.assertEqual(Variance('age').result['age__variance'], 0)

if __name__ == "__main__":
    unittest.main()
