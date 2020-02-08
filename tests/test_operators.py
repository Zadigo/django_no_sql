import unittest
from django_no_sql.db.operators import Avg, Sum, Min, Max, Aggregate, Variance, STDeviation

TESTDATA = [
    {"age": 15, "attributes": {"height": 187}},
    {"age": 19, "attributes": {"height": 159}},
]

class TestAggregate(unittest.TestCase):
    def setUp(self):
        self.operator = Aggregate('age')

class TestAvg(unittest.TestCase):
    def setUp(self):
        self.operator = Avg('age')

    def test_result(self):
        self.operator.resolve(TESTDATA)
        self.assertEqual(self.operator.result, 17)

class TestSum(unittest.TestCase):
    def setUp(self):
        self.operator = Sum('age')

    def test_result(self):
        self.operator.resolve(TESTDATA)
        self.assertEqual(self.operator.result, 34)

class TestMin(unittest.TestCase):
    def setUp(self):
        self.operator = Min('age')

    def test_result(self):
        self.operator.resolve(TESTDATA)
        self.assertEqual(self.operator.result, 15)

class TestMax(unittest.TestCase):
    def setUp(self):
        self.operator = Max('age')

    def test_result(self):
        self.operator.resolve(TESTDATA)
        self.assertEqual(self.operator.result, 19)

class TestVariance(unittest.TestCase):
    def setUp(self):
        self.operator = Variance('age')

    def test_result(self):
        self.operator.resolve(TESTDATA)
        print(self.operator.result)
        self.assertEqual(self.operator.result, 15)



if __name__ == "__main__":
    unittest.main()