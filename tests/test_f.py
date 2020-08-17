from django_no_sql.db.operators import F
import unittest

TESTDATA = [
    {"age": 15, "attributes": {"height": 187}},
    {"age": 19, "attributes": {"height": 159}},
]


class TestF(unittest.TestCase):
    def setUp(self):
        self.age = F('age')
        self.attributes = F('attributes__height')

    def test_field(self):
        self.assertEqual(self.age.field, 'age')
        self.assertEqual(self.attributes.field, 'attributes__height')

    def test_resolve_values(self):
        self.age.resolve(data=TESTDATA)
        self.assertIsInstance(self.age.resolved_values, list)

    def test_resolve_data(self):
        age = self.age.resolve(data=TESTDATA)
        self.assertIsInstance(age, list)
        self.assertEqual(15, age[0])

        attributes = self.attributes.resolve(data=TESTDATA)
        self.assertIsInstance(attributes, list)
        self.assertEqual(187, attributes[0])

    def test_length(self):
        self.age.resolve(data=TESTDATA)
        self.assertEqual(self.age.__len__(), 2)
        self.assertEqual(len(self.age), 2)

    def test_add_one(self):
        # Testing the fact of adding one
        # to the F function instance:
        # f = F(age) -> f + 1
        self.age.resolve(data=TESTDATA)
        new_values = self.age + 1
        self.assertEqual(new_values, [16, 20])

        # Adding two F functions together
        # new_value = self.age + self.age
        # self.assertEqual(new_value, 34)

    def test_comparision(self):
        # self.age.resolve(data=TESTDATA)
        # FIXME: This is a false comparision. Asserts that
        # the array exists but not that the functions in the
        # array are actually greater than x value
        # self.assertTrue(self.age > 17)
        # print(self.age > 17)

        # & operator
        lea = F('age')
        camille = F('age')
        lea.resolve(data=TESTDATA)
        camille.resolve(data=TESTDATA)
        # self.assertTrue(lea & camille, True)
        print(lea.resolved_values)

if __name__ == "__main__":
    unittest.main()
